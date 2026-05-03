#!/usr/bin/env python3
"""
Worth2Watch — "izlenir mi?" özet üretici.

Her item için TMDB'nin user reviews endpoint'inden gerçek kullanıcı
yorumlarını çek, ücretsiz LLM'larla özetle, verdict + 3 maddelik
artı/eksi + 0-100 worthScore üret. Çıktı public/movies.json'a
in-place merge edilir.

Neden TMDB? Daha önce Reddit JSON kullanılıyordu ama Reddit User-Agent
bazlı anonymous scraping'i agresif şekilde 403 ile bloklamaya başladı.
TMDB'nin /reviews endpoint'i ise TMDB API key ile her zaman çalışıyor
(zaten katalog için kullanıyoruz) ve /reviews kullanıcıların yazdığı
gerçek essay-stili eleştiriler döndürüyor — Reddit kadar "konuşmalı"
değil ama verdict çıkarımı için yeterli kalitede.

Ücretsiz LLM pipeline (sırayla denenir, biri tükendiğinde diğerine düşer):
- Groq llama-3.3-70b-versatile  (1000 RPD, en kaliteli)
- Groq llama-3.1-8b-instant     (14400 RPD, hızlı yedek)
- Gemini 2.5 Flash              (~250 RPD)
- Gemini 2.5 Flash Lite         (~250 RPD)

Optimizasyonlar:
- Yorum yoksa LLM'e hiç gitme (yetersiz_veri olarak işaretle)
- Top 6 yorum × 800 char ile input'u trim et (token tasarrufu)

Run:
    TMDB_API_KEY=... GROQ_API_KEY=... GEMINI_API_KEY=... \
    python3 scripts/build_worth_summaries.py [--limit 1500]
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus, urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public" / "movies.json"
CACHE_DIR = ROOT / ".worth_cache"
CACHE_DIR.mkdir(exist_ok=True)
REVIEWS_CACHE = CACHE_DIR / "reviews"
REVIEWS_CACHE.mkdir(exist_ok=True)
IMDB_CACHE = CACHE_DIR / "imdb"
IMDB_CACHE.mkdir(exist_ok=True)
LETTERBOXD_CACHE = CACHE_DIR / "letterboxd"
LETTERBOXD_CACHE.mkdir(exist_ok=True)
JIKAN_CACHE = CACHE_DIR / "jikan"
JIKAN_CACHE.mkdir(exist_ok=True)
LLM_CACHE = CACHE_DIR / "llm"
LLM_CACHE.mkdir(exist_ok=True)

TMDB_KEY = os.environ.get("TMDB_API_KEY", "").strip()
GROQ_KEY = os.environ.get("GROQ_API_KEY", "").strip()

# Gemini supports multi-key rotation. Each Google AI project gets its own
# free-tier daily quota, so 6 project keys ≈ 6× the daily ceiling.
# Either GEMINI_API_KEYS=k1,k2,... or single GEMINI_API_KEY works.
_gemini_env = os.environ.get("GEMINI_API_KEYS", "").strip()
if _gemini_env:
    GEMINI_KEYS: list[str] = [k.strip() for k in _gemini_env.split(",") if k.strip()]
elif os.environ.get("GEMINI_API_KEY", "").strip():
    GEMINI_KEYS = [os.environ["GEMINI_API_KEY"].strip()]
else:
    GEMINI_KEYS = []

if not TMDB_KEY:
    sys.exit("TMDB_API_KEY env var is required")
if not GROQ_KEY and not GEMINI_KEYS:
    sys.exit("Need at least one of GROQ_API_KEY or GEMINI_API_KEY[S]")

# Backend rotation: tuples of (provider, model, min_interval_s, key_index).
# Gemini is preferred (multi-key gives the most aggregate quota); Groq
# is the fallback. When one slot's daily quota hits we mark it exhausted
# and the loop moves on to the next.
BACKENDS: list[tuple[str, str, float, int]] = []
for i in range(len(GEMINI_KEYS)):
    BACKENDS.append(("gemini", "gemini-2.5-flash", 5.0, i))
    BACKENDS.append(("gemini", "gemini-2.5-flash-lite", 4.0, i))
if GROQ_KEY:
    BACKENDS.append(("groq", "llama-3.3-70b-versatile", 2.5, 0))
    BACKENDS.append(("groq", "llama-3.1-8b-instant", 1.5, 0))

_exhausted: set[str] = set()  # backend keys ("provider:model:keyidx")
_last_call_t: dict[str, float] = {}


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------


def http_post(url: str, headers: dict, body: dict, timeout: int = 30) -> tuple[int, str]:
    # Override the default urllib UA — Cloudflare in front of Groq returns
    # 1010 (banned browser signature) for the bare "Python-urllib/3.x" UA.
    # Catch URLError/socket.timeout broadly: when a Gemini key is freshly
    # exhausted the connection sometimes hangs instead of returning 429,
    # so we synthesise a fake 503 to make the caller back off and rotate.
    full_headers = {"User-Agent": "Worth2Watch-build/1.0 (curl-equivalent)"}
    full_headers.update(headers)
    req = Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers=full_headers,
        method="POST",
    )
    try:
        with urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8")
    except HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="ignore")
    except (URLError, OSError, ConnectionError) as e:
        return 503, f"transport: {e}"


# ---------------------------------------------------------------------------
# TMDB review harvest
# ---------------------------------------------------------------------------


def tmdb_get(path: str, params: dict | None = None, retries: int = 3) -> dict | None:
    p = {"api_key": TMDB_KEY}
    if params:
        p.update(params)
    url = f"https://api.themoviedb.org/3{path}?{urlencode(p)}"
    delay = 2.0
    for _ in range(retries):
        try:
            req = Request(url, headers={"Accept": "application/json"})
            with urlopen(req, timeout=20) as r:
                return json.loads(r.read().decode("utf-8"))
        except HTTPError as e:
            if e.code in (429, 500, 502, 503):
                time.sleep(delay)
                delay *= 2
                continue
            return None
        except (URLError, json.JSONDecodeError):
            time.sleep(delay)
            delay *= 2
    return None


def harvest_letterboxd_reviews(item: dict, max_reviews: int = 15) -> list[str]:
    """Films only — pull popular Letterboxd reviews via TMDB-id redirect.

    Letterboxd's `tmdb/{id}` URL 302-redirects to `/film/{slug}/`, so we
    don't need to derive the slug ourselves. Cloudflare blocks plain
    requests but cloudscraper's browser-like fingerprint gets through.
    """
    if item.get("mediaType") != "movie":
        return []
    tmdb_id = item.get("tmdbId")
    if not tmdb_id:
        return []

    cache_path = LETTERBOXD_CACHE / f"{tmdb_id}.json"
    if cache_path.exists():
        try:
            return json.loads(cache_path.read_text())
        except Exception:
            pass

    try:
        import cloudscraper  # local import — only needed for movies
    except ImportError:
        return []

    scraper = cloudscraper.create_scraper()
    out: list[str] = []
    try:
        # Step 1: GET /tmdb/{id}/ to find the canonical slug. The /tmdb/
        # path only redirects the BASE film URL — appending /reviews/
        # gives a 404. So we resolve the slug first, then fetch reviews.
        import re
        head = scraper.get(
            f"https://letterboxd.com/tmdb/{tmdb_id}/",
            timeout=15,
            allow_redirects=False,
        )
        if head.status_code not in (301, 302, 303, 307, 308):
            cache_path.write_text("[]")
            return []
        loc = head.headers.get("Location") or ""
        slug_match = re.search(r"/film/([^/]+)/", loc)
        if not slug_match:
            cache_path.write_text("[]")
            return []
        slug = slug_match.group(1)

        # Step 2: pull popular reviews on the actual film page
        time.sleep(0.4)
        url = f"https://letterboxd.com/film/{slug}/reviews/by/activity/"
        r = scraper.get(url, timeout=20)
        if r.status_code != 200:
            cache_path.write_text("[]")
            return []
        # Capture each review block (paragraph by paragraph)
        blocks = re.findall(
            r'<div class="body-text[^"]*"[^>]*>(.+?)</div>',
            r.text,
            re.DOTALL,
        )
        # Also grab star rating per review if present (in attached attribute)
        ratings = re.findall(
            r'data-original-title="([★½]+)"',
            r.text,
        )
        for i, b in enumerate(blocks):
            paragraphs = re.findall(r"<p>(.+?)</p>", b, re.DOTALL)
            text = "\n\n".join(paragraphs)
            text = re.sub(r"<[^>]+>", "", text)
            text = re.sub(r"&nbsp;", " ", text)
            text = re.sub(r"&amp;", "&", text)
            text = re.sub(r"&#x27;", "'", text)
            text = text.strip()
            if len(text) < 60:
                continue
            prefix = ""
            if i < len(ratings):
                stars = ratings[i].count("★") + (0.5 if "½" in ratings[i] else 0)
                prefix = f"[Letterboxd: {stars}/5 ★] "
            out.append(f"{prefix}{text}"[:1500])
            if len(out) >= max_reviews:
                break
    except Exception:
        pass

    cache_path.write_text(json.dumps(out, ensure_ascii=False))
    return out


def harvest_jikan_reviews(item: dict, max_reviews: int = 15) -> list[str]:
    """Anime only — search MyAnimeList via Jikan, then pull reviews.

    We treat any item whose genres include 'Animasyon' or 'Animation'
    AND whose original title contains non-ASCII / Japanese as anime.
    Conservative: a Pixar film won't return useful results, but the
    search will silently fail and we'll just not get extra reviews.
    """
    genres = item.get("genres") or []
    is_animation = any(g in ("Animasyon", "Animation") for g in genres)
    if not is_animation:
        return []

    cache_path = JIKAN_CACHE / f"{item['mediaType']}_{item['tmdbId']}.json"
    if cache_path.exists():
        try:
            return json.loads(cache_path.read_text())
        except Exception:
            pass

    title_query = (item.get("originalTitle") or item.get("title") or "").strip()
    if not title_query:
        cache_path.write_text("[]")
        return []

    # Jikan: free, no auth, ~3 RPS rate limit. Returns 504 when MAL is
    # itself slow — we retry a couple of times. Catch broadly because
    # socket.timeout, ssl errors, etc. all show up here under load.
    def _jikan_get(url: str) -> dict | None:
        for attempt in range(2):
            time.sleep(1.0 + attempt)
            try:
                req = Request(url, headers={"Accept": "application/json"})
                with urlopen(req, timeout=10) as r:
                    body = r.read().decode("utf-8")
                payload = json.loads(body)
                if payload.get("status") in (502, 503, 504):
                    continue
                return payload
            except Exception:
                continue
        return None

    out: list[str] = []
    try:
        # Step 1: search for the MAL id
        search = _jikan_get(
            f"https://api.jikan.moe/v4/anime?q={quote_plus(title_query)}&limit=3"
        )
        if not search or not (search.get("data") or []):
            cache_path.write_text("[]")
            return []
        mal_id = (search["data"][0] or {}).get("mal_id")
        if not mal_id:
            cache_path.write_text("[]")
            return []
        # Step 2: pull reviews
        data = _jikan_get(
            f"https://api.jikan.moe/v4/anime/{mal_id}/reviews?limit={max_reviews}"
        )
        if data:
            for r in data.get("data") or []:
                body = (r.get("review") or "").strip()
                score = r.get("score")
                if len(body) < 80:
                    continue
                prefix = f"[MAL: {score}/10] " if score is not None else ""
                out.append(f"{prefix}{body}"[:1500])
    except Exception:
        # Belt-and-braces — swallow any other exception so the main loop
        # keeps moving even if Jikan goes weird.
        pass

    cache_path.write_text(json.dumps(out, ensure_ascii=False))
    return out


def harvest_imdb_reviews(item: dict, max_reviews: int = 50) -> list[str]:
    """Pull user reviews via IMDb's public GraphQL endpoint.

    Why GraphQL when we couldn't scrape the HTML page: imdb.com/.../reviews
    serves a JS-rendered shell that returns HTTP 202 to plain HTTP clients.
    api.graphql.imdb.com is what their own SPA calls — no auth, no anti-
    scraping, returns structured JSON. Disclaimer in the response says
    'non-commercial only' which fits this project.

    We sort by helpfulness so we get reviews the IMDb community has
    upvoted, not random first-page essays.
    """
    imdb_id = item.get("imdbId")
    if not imdb_id:
        return []

    cache_key = f"{imdb_id}.json"
    cache_path = IMDB_CACHE / cache_key
    if cache_path.exists():
        try:
            return json.loads(cache_path.read_text())
        except Exception:
            pass

    query = """
    query R($id: ID!, $first: Int!) {
      title(id: $id) {
        reviews(first: $first, sort: { by: HELPFULNESS_SCORE, order: DESC }) {
          edges {
            node {
              authorRating
              summary { originalText }
              text { originalText { plainText } }
              helpfulness { upVotes downVotes }
            }
          }
        }
      }
    }
    """
    body = {"query": query, "variables": {"id": imdb_id, "first": max_reviews}}
    headers = {
        "Content-Type": "application/json",
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/17.0 Safari/605.1.15"
        ),
    }
    status, text = http_post(
        "https://api.graphql.imdb.com/", headers, body, timeout=30
    )
    if status != 200:
        cache_path.write_text("[]")
        return []
    try:
        data = json.loads(text)
        edges = (
            ((data.get("data") or {}).get("title") or {}).get("reviews") or {}
        ).get("edges") or []
    except (json.JSONDecodeError, AttributeError):
        cache_path.write_text("[]")
        return []

    out: list[str] = []
    for e in edges:
        n = e.get("node") or {}
        body_text = (
            ((n.get("text") or {}).get("originalText") or {}).get("plainText")
            or ""
        ).strip()
        summary = ((n.get("summary") or {}).get("originalText") or "").strip()
        rating = n.get("authorRating")
        helpful = (n.get("helpfulness") or {}).get("upVotes") or 0
        if len(body_text) < 80:
            continue
        # Prefix with structured signal so the LLM can weight it
        prefix_parts = []
        if rating is not None:
            prefix_parts.append(f"[Rating: {rating}/10]")
        if helpful:
            prefix_parts.append(f"[{helpful} found helpful]")
        prefix = " ".join(prefix_parts)
        if summary and summary.lower() not in body_text.lower()[:200]:
            content = f"{prefix} {summary}\n\n{body_text}".strip()
        else:
            content = f"{prefix} {body_text}".strip()
        out.append(content[:1500])

    cache_path.write_text(json.dumps(out, ensure_ascii=False))
    return out


def harvest_tmdb_reviews(item: dict, max_reviews: int = 12) -> list[str]:
    """Return a list of TMDB user review bodies for the item.

    TMDB returns reviews paginated, but for our use case the first page
    (~20 reviews max) is plenty — anything past that has even less
    signal. We pull a couple of pages if available.
    """
    cache_key = f"{item['mediaType']}_{item['tmdbId']}.json"
    cache_path = REVIEWS_CACHE / cache_key
    if cache_path.exists():
        try:
            return json.loads(cache_path.read_text())
        except Exception:
            pass

    kind = item["mediaType"]
    tid = item["tmdbId"]
    reviews: list[str] = []

    for page in (1, 2):
        data = tmdb_get(f"/{kind}/{tid}/reviews", {"language": "en-US", "page": page})
        if not data:
            break
        for r in data.get("results") or []:
            content = (r.get("content") or "").strip()
            if len(content) < 80:
                continue
            reviews.append(content)
        if page >= (data.get("total_pages") or 1):
            break
        if len(reviews) >= max_reviews * 2:
            break

    cache_path.write_text(json.dumps(reviews, ensure_ascii=False))
    return reviews[:max_reviews]


# ---------------------------------------------------------------------------
# Prompt construction (kept identical across providers so cache is portable)
# ---------------------------------------------------------------------------


def build_prompt(item: dict, comments: list[str]) -> str:
    title = item["title"]
    year = item.get("year") or "?"
    kind = "series" if item["mediaType"] == "tv" else "film"

    # Trim hard for token budget: top 6 reviews × 400 chars max.
    # Each item costs ~1.5K input tokens this way — fits comfortably
    # inside Gemini free-tier per-minute token windows so we can fan
    # 6 keys × 250 daily req = 1500 calls/day cleanly.
    trimmed = [c[:400] for c in comments[:6]]
    joined = "\n\n---\n\n".join(trimmed)
    if len(joined) > 3000:
        joined = joined[:3000]

    return f"""You are an impartial film/TV critic. Below are real user reviews
collected from Letterboxd, MyAnimeList, IMDb, and TMDB. Some carry tags like
[Rating: X/10], [N found helpful], or [stars] — these signal how much the
community valued each review. Take the spread of opinions seriously.

CONTENT: "{title}" ({year})

REVIEWS:
{joined}

TASK: Read these reviews and answer impartially and honestly:
"Is this {kind} worth watching?"

RULES:
- Don't be a fan. If reviews contain criticism, reflect it.
- One paragraph summary (max 3-4 sentences, in English).
- Produce a 0-100 worthScore (how positive the reviews are overall).
- Verdict: one of "izlemeye_değer", "tartışmalı", "izleme" (these are
  enum keys — keep them in this exact form, the UI translates them).
- Short (4-6 word) highlight / lowlight bullets in English.
- No spoilers.

Respond ONLY in this JSON format, nothing else:
{{"worthVerdict": "izlemeye_değer|tartışmalı|izleme", "worthScore": <0-100>, "worthSummary": "...", "worthHighlights": ["...", "..."], "worthLowlights": ["...", "..."]}}"""


# ---------------------------------------------------------------------------
# LLM backends
# ---------------------------------------------------------------------------


def throttle(backend_key: str, min_interval: float) -> None:
    last = _last_call_t.get(backend_key, 0.0)
    elapsed = time.time() - last
    if elapsed < min_interval:
        time.sleep(min_interval - elapsed)


def call_groq(model: str, prompt: str, min_interval: float) -> tuple[dict | None, str | None]:
    """Returns (parsed_result, exhaustion_reason). On daily quota the
    reason string is non-None and the caller can mark this backend
    exhausted for the rest of the run."""
    backend_key = f"groq:{model}"
    throttle(backend_key, min_interval)
    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 800,
        "response_format": {"type": "json_object"},
    }
    delay = 4.0
    for _ in range(3):
        status, text = http_post(
            "https://api.groq.com/openai/v1/chat/completions",
            {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"},
            body,
        )
        _last_call_t[backend_key] = time.time()
        if status == 200:
            try:
                payload = json.loads(text)
                content = payload["choices"][0]["message"]["content"]
                return json.loads(content), None
            except (json.JSONDecodeError, KeyError, IndexError):
                return None, None
        if status == 429:
            # Distinguish per-minute (retry quickly) from per-day (give up)
            if "rate_limit_exceeded" in text and "minute" in text.lower():
                time.sleep(delay)
                delay *= 1.7
                continue
            if "daily" in text.lower() or "tokens per day" in text.lower() or "requests per day" in text.lower():
                return None, "daily_quota"
            # Unknown 429 — back off once, then move on
            time.sleep(delay)
            delay *= 1.7
            continue
        if status in (500, 502, 503):
            time.sleep(delay)
            delay *= 1.7
            continue
        # 400/401/403 etc — bail, don't waste retries
        print(f"    ! groq/{model} {status}: {text[:160]}", flush=True)
        return None, None
    return None, None


def call_gemini(
    model: str, prompt: str, min_interval: float, key_idx: int = 0
) -> tuple[dict | None, str | None]:
    """Hit Gemini with the key at GEMINI_KEYS[key_idx]. Daily quota
    here means *that key* is exhausted — caller marks just that slot."""
    backend_key = f"gemini:{model}:{key_idx}"
    throttle(backend_key, min_interval)
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.3,
            "responseMimeType": "application/json",
        },
    }
    api_key = GEMINI_KEYS[key_idx]
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent?key={api_key}"
    )
    delay = 5.0
    for _ in range(3):
        status, text = http_post(url, {"Content-Type": "application/json"}, body)
        _last_call_t[backend_key] = time.time()
        if status == 200:
            try:
                payload = json.loads(text)
                content = payload["candidates"][0]["content"]["parts"][0]["text"]
                return json.loads(content), None
            except (json.JSONDecodeError, KeyError, IndexError):
                return None, None
        if status == 429:
            if "PerDay" in text:
                return None, "daily_quota"
            time.sleep(delay)
            delay *= 1.7
            continue
        if status in (500, 502, 503):
            time.sleep(delay)
            delay *= 1.7
            continue
        print(f"    ! gemini/{model}#{key_idx} {status}: {text[:160]}", flush=True)
        return None, None
    return None, None


def metrics_verdict(item: dict) -> dict:
    """Verdict from raw stats when no review text is available.

    The reasoning: if a million people voted Breaking Bad 9.5 on IMDb,
    that itself is a tarafsız community judgment. We don't need essays
    to say "izlenir." Score weights rating by log(votes) so a 9.5 with
    20 votes can't outrank an 8.7 with 500K votes.
    """
    import math

    imdb_r = item.get("imdbRating") or 0
    imdb_v = item.get("imdbVotes") or 0
    tmdb_r = item.get("tmdbRating") or 0
    tmdb_v = item.get("tmdbVotes") or 0

    # Pick the better-attested signal
    if imdb_v >= 5000:
        rating, votes, source = imdb_r, imdb_v, "IMDb"
    elif tmdb_v >= 200:
        rating, votes, source = tmdb_r, tmdb_v, "TMDB"
    elif imdb_v > 0:
        rating, votes, source = imdb_r, imdb_v, "IMDb"
    else:
        rating, votes, source = tmdb_r, tmdb_v, "TMDB"

    # Vote weight: 0..1 across log10 scale (10..1M votes)
    if votes > 0:
        weight = max(0.0, min(1.0, (math.log10(max(votes, 10)) - 1) / 5))
    else:
        weight = 0.0
    confidence = "yüksek" if weight > 0.7 else "orta" if weight > 0.4 else "düşük"

    if rating >= 8.0 and weight >= 0.5:
        verdict = "izlemeye_değer"
        score = int(round(min(95, 70 + (rating - 8) * 12 + weight * 8)))
    elif rating >= 7.0 and weight >= 0.3:
        verdict = "izlemeye_değer" if rating >= 7.5 else "tartışmalı"
        score = int(round(min(85, 55 + (rating - 7) * 12 + weight * 8)))
    elif rating >= 6.0:
        verdict = "tartışmalı"
        score = int(round(40 + (rating - 6) * 10))
    elif rating > 0:
        verdict = "izleme"
        score = int(round(max(15, 30 - (6 - rating) * 6)))
    else:
        verdict = "tartışmalı"
        score = 50

    votes_str = f"{int(votes):,}" if votes else "a small number of"
    confidence_en = {"yüksek": "high", "orta": "medium", "düşük": "low"}[confidence]
    summary = (
        f"{votes_str} {source} users rated this {rating:.1f}/10 "
        f"({confidence_en} confidence). "
    )
    if verdict == "izlemeye_değer":
        summary += "Broadly loved by audiences — worth a watch."
    elif verdict == "tartışmalı":
        summary += "Audience reception is mixed — comes down to taste."
    else:
        summary += "Generally rated poorly by viewers."

    return {
        "worthVerdict": verdict,
        "worthSummary": summary,
        "worthScore": score,
        "worthHighlights": [],
        "worthLowlights": [],
        "worthSourceCount": int(votes) if votes else 0,
        "worthSource": "metrics",
    }


def llm_summarize(item: dict, comments: list[str]) -> dict | None:
    """Try each non-exhausted backend in order until one returns a result."""
    cache_key = f"{item['mediaType']}_{item['tmdbId']}.json"
    cache_path = LLM_CACHE / cache_key
    if cache_path.exists():
        cached = None
        try:
            cached = json.loads(cache_path.read_text())
        except Exception:
            pass
        # If old cache says yetersiz_veri but we now have a metrics
        # fallback, recompute (don't return the stale "no data" answer)
        if cached and cached.get("worthVerdict") != "yetersiz_veri":
            return cached

    # No review text at all — use stats-only verdict instead of bailing.
    # Even a single review is worth sending to the LLM though, since
    # IMDb GraphQL gives us helpfulness-sorted picks (one well-upvoted
    # essay beats zero data).
    if len(comments) < 1:
        out = metrics_verdict(item)
        cache_path.write_text(json.dumps(out, ensure_ascii=False))
        return out

    prompt = build_prompt(item, comments)

    for provider, model, interval, key_idx in BACKENDS:
        backend_key = f"{provider}:{model}:{key_idx}"
        if backend_key in _exhausted:
            continue
        try:
            if provider == "groq":
                result, reason = call_groq(model, prompt, interval)
            else:
                result, reason = call_gemini(model, prompt, interval, key_idx)
        except Exception as exc:
            # Don't let an uncaught transport error abort the whole run —
            # mark this backend exhausted and try the next one.
            print(f"    ! {backend_key} crashed: {exc}", flush=True)
            _exhausted.add(backend_key)
            continue
        if reason == "daily_quota":
            print(
                f"    ! {backend_key} daily quota exhausted, skipping for rest of run",
                flush=True,
            )
            _exhausted.add(backend_key)
            continue
        if result:
            out = {
                "worthVerdict": result.get("worthVerdict") or "tartışmalı",
                "worthSummary": (result.get("worthSummary") or "").strip(),
                "worthScore": result.get("worthScore"),
                "worthHighlights": result.get("worthHighlights") or [],
                "worthLowlights": result.get("worthLowlights") or [],
                "worthSourceCount": len(comments),
                "worthSource": f"{provider}:{model}",
            }
            cache_path.write_text(json.dumps(out, ensure_ascii=False))
            return out

    # All LLM backends failed — fall through to metrics so the catalog
    # never has empty cells. Cache it so the next run doesn't retry.
    out = metrics_verdict(item)
    cache_path.write_text(json.dumps(out, ensure_ascii=False))
    return out


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0, help="0 = process everything")
    parser.add_argument("--from-rank", type=int, default=0)
    parser.add_argument(
        "--redo-suspicious",
        action="store_true",
        help="Re-process LLM-derived 'tartışmalı' verdicts where IMDb says strong love (≥8.0/50K). Adds IMDb GraphQL reviews to the source pool.",
    )
    args = parser.parse_args()

    catalog = json.loads(PUBLIC.read_text())
    print(f"Loaded {len(catalog):,} items from {PUBLIC}")
    print(f"Backends: {len(BACKENDS)} slots ({sum(1 for b in BACKENDS if b[0]=='gemini')} Gemini × {len(GEMINI_KEYS)} keys, {sum(1 for b in BACKENDS if b[0]=='groq')} Groq)\n")

    if args.redo_suspicious:
        # Drop the suspicious verdicts so the main loop re-runs them. Also
        # purge the LLM cache for those keys (otherwise the cached verdict
        # would short-circuit the re-run).
        targets = []
        for m in catalog:
            if m.get("worthVerdict") != "tartışmalı":
                continue
            src = m.get("worthSource") or ""
            if not (src.startswith("groq:") or src.startswith("gemini:")):
                continue
            if (m.get("imdbRating") or 0) >= 8.0 and (m.get("imdbVotes") or 0) >= 50000:
                targets.append(m)
        for m in targets:
            cache_path = LLM_CACHE / f"{m['mediaType']}_{m['tmdbId']}.json"
            if cache_path.exists():
                cache_path.unlink()
            for k in (
                "worthVerdict", "worthSummary", "worthScore",
                "worthHighlights", "worthLowlights", "worthSourceCount",
                "worthSource",
            ):
                m.pop(k, None)
        print(f"--redo-suspicious: cleared {len(targets)} verdicts for re-run\n")

    # NB: catalog is already sorted by build_catalog.py (and the trim-1500
    # script applied a Bayesian rerank). We process in file order.
    end = len(catalog) if args.limit == 0 else min(len(catalog), args.from_rank + args.limit)
    work = catalog[args.from_rank:end]
    print(f"Processing rank {args.from_rank}..{end} ({len(work)} items)\n")

    succeeded = 0
    skipped_cached = 0
    skipped_no_data = 0
    failed = 0

    for i, item in enumerate(work, 1):
        if item.get("worthSummary"):
            skipped_cached += 1
            continue

        # Combine all sources — order matters because we trim to top 12
        # in build_prompt(). Letterboxd first for movies (cinephile gold
        # standard), Jikan first for anime, then IMDb (helpful-sorted),
        # then TMDB. The LLM sees the strongest community signal first.
        sources = (
            harvest_letterboxd_reviews(item)
            + harvest_jikan_reviews(item)
            + harvest_imdb_reviews(item)
            + harvest_tmdb_reviews(item)
        )
        result = llm_summarize(item, sources)

        if result:
            item.update(result)
            if result["worthVerdict"] == "yetersiz_veri":
                skipped_no_data += 1
            else:
                succeeded += 1
            src = result.get("worthSource", "?")
            verdict = result.get("worthVerdict") or "?"
            score = result.get("worthScore")
            print(
                f"  [{i}/{len(work)}] {item['title'][:46]:46s}  "
                f"{verdict:16s}  score={score!s:4s}  src={result.get('worthSourceCount')}  via={src}",
                flush=True,
            )
        else:
            failed += 1
            print(f"  [{i}/{len(work)}] {item['title'][:46]:46s}  FAILED (all backends)", flush=True)
            # If every backend is exhausted, no point continuing
            if len(_exhausted) == len(BACKENDS):
                print("\n! All backends exhausted for today. Re-run tomorrow.", flush=True)
                break

        # Incremental save every 25 items
        if i % 25 == 0:
            PUBLIC.write_text(json.dumps(catalog, ensure_ascii=False, separators=(",", ":")))

    PUBLIC.write_text(json.dumps(catalog, ensure_ascii=False, separators=(",", ":")))
    print(
        f"\n✓ done — {succeeded} new, {skipped_no_data} yetersiz_veri, "
        f"{skipped_cached} already cached, {failed} failed"
    )
    print(f"  catalog now {PUBLIC.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
