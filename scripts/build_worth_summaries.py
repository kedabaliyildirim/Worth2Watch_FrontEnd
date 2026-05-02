#!/usr/bin/env python3
"""
Worth2Watch — "izlenir mi?" özet üretici.

Reddit'teki canlı film/dizi tartışmalarını çek, Gemini'a verdir, her item
için tek-paragraflık verdict + 3 maddelik artı/eksi + 0-100 worthScore
üret. Çıktı public/movies.json'a in-place merge edilir.

Ücretsiz pipeline:
- Reddit JSON endpoint'i (anonim, user-agent zorunlu, rate ~60 rpm)
- Gemini 2.5 Flash free tier (15 RPM, 1500 RPD, 1M TPM)

Run:
    GEMINI_API_KEY=... python3 scripts/build_worth_summaries.py [--limit 50]
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public" / "movies.json"
CACHE_DIR = ROOT / ".worth_cache"
CACHE_DIR.mkdir(exist_ok=True)
REDDIT_CACHE = CACHE_DIR / "reddit"
REDDIT_CACHE.mkdir(exist_ok=True)
GEMINI_CACHE = CACHE_DIR / "gemini"
GEMINI_CACHE.mkdir(exist_ok=True)

GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
if not GEMINI_KEY:
    sys.exit("GEMINI_API_KEY env var is required")

UA = "Worth2Watch-research/0.1 (single-user; non-commercial)"

# Free tier: 15 RPM. We pad to 4.5s between calls so 60s window holds 13.
GEMINI_MIN_INTERVAL_S = 4.5
_last_gemini_t = [0.0]


# ---------------------------------------------------------------------------
# Reddit
# ---------------------------------------------------------------------------


def reddit_get(url: str, retries: int = 3) -> dict | None:
    delay = 2.0
    for _ in range(retries):
        try:
            req = Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
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


def harvest_reddit(item: dict, max_threads: int = 4, max_comments_per: int = 8) -> list[str]:
    """Return a list of comment bodies (raw text) for the item.

    Tries the originalTitle (English most of the time) first since Reddit's
    English-speaking community uses original titles. Falls back to the
    Turkish title if the original returns nothing.
    """
    cache_key = f"{item['mediaType']}_{item['tmdbId']}.json"
    cache_path = REDDIT_CACHE / cache_key
    if cache_path.exists():
        try:
            return json.loads(cache_path.read_text())
        except Exception:
            pass

    year = item.get("year") or ""
    is_tv = item["mediaType"] == "tv"
    sub = "television" if is_tv else "movies"

    queries: list[str] = []
    original = (item.get("originalTitle") or "").strip()
    title = (item.get("title") or "").strip()
    if original:
        queries.append(original)
    if title and title != original:
        queries.append(title)

    threads: list[str] = []
    for q_title in queries:
        q = f'"{q_title}"'
        if year:
            q += f" {year}"
        search_url = (
            f"https://www.reddit.com/r/{sub}/search.json?"
            f"q={quote_plus(q)}&restrict_sr=1&sort=top&limit={max_threads}"
        )
        search = reddit_get(search_url)
        if not search:
            continue
        for child in (search.get("data") or {}).get("children") or []:
            d = child.get("data") or {}
            permalink = d.get("permalink")
            if permalink and permalink not in threads:
                threads.append(permalink)
        if len(threads) >= max_threads:
            break

    if not threads:
        # Last-ditch: search across all of reddit (no subreddit restriction)
        kind_word = "tv" if is_tv else "movie"
        q = f'"{(original or title)}" {kind_word}'
        url = (
            f"https://www.reddit.com/search.json?"
            f"q={quote_plus(q)}&sort=top&limit={max_threads}&t=all"
        )
        search = reddit_get(url)
        if search:
            for child in (search.get("data") or {}).get("children") or []:
                d = child.get("data") or {}
                permalink = d.get("permalink")
                if permalink and permalink not in threads:
                    threads.append(permalink)

    if not threads:
        cache_path.write_text("[]")
        return []

    comments: list[str] = []
    for permalink in threads[:max_threads]:
        time.sleep(1.0)  # be polite
        thread_url = f"https://www.reddit.com{permalink}.json?limit={max_comments_per}&sort=top"
        thread = reddit_get(thread_url)
        if not thread or not isinstance(thread, list) or len(thread) < 2:
            continue
        for child in (thread[1].get("data") or {}).get("children") or []:
            body = (child.get("data") or {}).get("body") or ""
            body = body.strip()
            if not body or body == "[deleted]" or body == "[removed]":
                continue
            if len(body) < 30:
                continue
            comments.append(body[:1500])  # cap individual comment length

    cache_path.write_text(json.dumps(comments, ensure_ascii=False))
    return comments


# ---------------------------------------------------------------------------
# Gemini
# ---------------------------------------------------------------------------


GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash:generateContent"
)


def gemini_summarize(item: dict, comments: list[str]) -> dict | None:
    if not comments:
        return {
            "worthVerdict": "yetersiz_veri",
            "worthSummary": "Bu içerik hakkında yeterli halk yorumu bulunamadı.",
            "worthScore": None,
            "worthHighlights": [],
            "worthLowlights": [],
            "worthSourceCount": 0,
        }

    cache_key = f"{item['mediaType']}_{item['tmdbId']}.json"
    cache_path = GEMINI_CACHE / cache_key
    if cache_path.exists():
        try:
            return json.loads(cache_path.read_text())
        except Exception:
            pass

    title = item["title"]
    year = item.get("year") or "?"
    kind = "dizisini" if item["mediaType"] == "tv" else "filmini"

    joined = "\n\n---\n\n".join(comments[:30])
    if len(joined) > 18000:
        joined = joined[:18000]

    prompt = f"""Sen tarafsız bir film/dizi eleştirmenisin. Aşağıda Reddit'ten alınmış gerçek
kullanıcı yorumları var (bazıları olumlu, bazıları olumsuz, bazıları spoiler içerebilir).

İÇERİK: "{title}" ({year})

YORUMLAR:
{joined}

GÖREV: Bu yorumları oku ve şu soruya tarafsız + dürüst cevap ver:
"Bu {kind} izlemeye değer mi?"

KURALLAR:
- Yandaş olma. Eğer yorumlarda eleştiri varsa onu da yansıt.
- Tek paragraf özet (en fazla 3-4 cümle, Türkçe).
- 0-100 arası worthScore üret (yorumların geneli ne kadar olumlu).
- Verdict: "izlemeye_değer", "tartışmalı", "izleme" üçünden biri.
- Kısa (4-6 kelime) artı/eksi maddeleri çıkar — her birini izleyicinin sevdiği/eleştirdiği nokta olarak yaz.
- Spoiler verme.

Sadece şu JSON formatında cevap ver, başka hiçbir şey yazma:
{{"worthVerdict": "izlemeye_değer|tartışmalı|izleme", "worthScore": <0-100>, "worthSummary": "...", "worthHighlights": ["...", "..."], "worthLowlights": ["...", "..."]}}"""

    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.3,
            "responseMimeType": "application/json",
        },
    }

    # Throttle for free-tier RPM
    elapsed = time.time() - _last_gemini_t[0]
    if elapsed < GEMINI_MIN_INTERVAL_S:
        time.sleep(GEMINI_MIN_INTERVAL_S - elapsed)

    delay = 5.0
    for attempt in range(4):
        try:
            req = Request(
                f"{GEMINI_URL}?key={GEMINI_KEY}",
                data=json.dumps(body).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urlopen(req, timeout=60) as r:
                _last_gemini_t[0] = time.time()
                payload = json.loads(r.read().decode("utf-8"))
                break
        except HTTPError as e:
            if e.code in (429, 500, 502, 503):
                err_body = e.read().decode("utf-8", errors="ignore")[:200]
                print(f"    ! Gemini {e.code}, retry in {delay}s — {err_body}", flush=True)
                time.sleep(delay)
                delay *= 2
                continue
            print(f"    ! Gemini error {e.code}: {e.read().decode('utf-8', errors='ignore')[:200]}", flush=True)
            return None
        except (URLError, json.JSONDecodeError) as exc:
            print(f"    ! Gemini transport: {exc}", flush=True)
            time.sleep(delay)
            delay *= 2
    else:
        return None

    try:
        text = payload["candidates"][0]["content"]["parts"][0]["text"]
        result = json.loads(text)
    except (KeyError, IndexError, json.JSONDecodeError) as exc:
        print(f"    ! Gemini parse: {exc}", flush=True)
        return None

    out = {
        "worthVerdict": result.get("worthVerdict") or "tartışmalı",
        "worthSummary": (result.get("worthSummary") or "").strip(),
        "worthScore": result.get("worthScore"),
        "worthHighlights": result.get("worthHighlights") or [],
        "worthLowlights": result.get("worthLowlights") or [],
        "worthSourceCount": len(comments),
    }
    cache_path.write_text(json.dumps(out, ensure_ascii=False))
    return out


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="How many top items to process this run (0 = all)",
    )
    parser.add_argument(
        "--from-rank",
        type=int,
        default=0,
        help="Start at the Nth-best item (for resuming a long run)",
    )
    args = parser.parse_args()

    catalog = json.loads(PUBLIC.read_text())
    print(f"Loaded {len(catalog):,} items from {PUBLIC}")

    # Process highest-rated first (the 'izlenmeye değer mi' question matters
    # most for items the user is likely to consider).
    catalog.sort(
        key=lambda m: (
            -(m.get("imdbRating") or 0),
            -(m.get("tmdbRating") or 0),
            -(m.get("popularity") or 0),
        )
    )

    end = len(catalog) if args.limit == 0 else min(len(catalog), args.from_rank + args.limit)
    work = catalog[args.from_rank:end]
    print(f"Processing rank {args.from_rank}..{end} ({len(work)} items)\n")

    succeeded = 0
    skipped = 0
    for i, item in enumerate(work, 1):
        # Skip if already done in a prior run
        if item.get("worthSummary"):
            skipped += 1
            continue

        comments = harvest_reddit(item)
        verdict = gemini_summarize(item, comments)

        if verdict:
            item.update(verdict)
            succeeded += 1
            print(
                f"  [{i}/{len(work)}] {item['title'][:50]:50s}  "
                f"{verdict.get('worthVerdict', '?'):16s}  "
                f"score={verdict.get('worthScore')}  src={verdict.get('worthSourceCount')}",
                flush=True,
            )
        else:
            print(f"  [{i}/{len(work)}] {item['title'][:50]:50s}  FAILED", flush=True)

        # Save incrementally every 10 items so a crash doesn't lose progress
        if i % 10 == 0:
            PUBLIC.write_text(json.dumps(catalog, ensure_ascii=False, separators=(",", ":")))

    PUBLIC.write_text(json.dumps(catalog, ensure_ascii=False, separators=(",", ":")))
    print(f"\n✓ done — {succeeded} new, {skipped} already cached")
    print(f"  catalog now {PUBLIC.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
