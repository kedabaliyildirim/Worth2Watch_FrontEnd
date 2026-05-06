#!/usr/bin/env python3
"""
Worth2Watch — Catalog builder (movies + TV shows).

Pulls a unified catalog of movies and TV shows from TMDB, enriches each
with IMDb ratings, TR streaming providers, and a YouTube trailer, then
writes a single static JSON the frontend reads at boot. No backend.

Sources
-------
- TMDB API
  - /movie/top_rated, /movie/popular, /discover/movie
  - /tv/top_rated,    /tv/popular,    /discover/tv
  - /movie/{id} or /tv/{id} with append_to_response for detail,
    external_ids, watch/providers, videos
- IMDb non-commercial dataset
  - title.ratings.tsv.gz

Run
---
    TMDB_API_KEY=... python3 scripts/build_catalog.py
    # optional knobs
    TMDB_REGION=TR TMDB_LANGUAGE=tr-TR MAX_PAGES=50 BUILD_WORKERS=16
"""

from __future__ import annotations

import gzip
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
PUBLIC_DIR = ROOT / "public"
CACHE_DIR = ROOT / ".catalog_cache"
CACHE_DIR.mkdir(exist_ok=True)

API_KEY = os.environ.get("TMDB_API_KEY", "").strip()
if not API_KEY:
    sys.exit("TMDB_API_KEY env var is required")

REGION = os.environ.get("TMDB_REGION", "TR").strip().upper()
LANGUAGE = os.environ.get("TMDB_LANGUAGE", "tr-TR").strip()
WORKERS = int(os.environ.get("BUILD_WORKERS", "16"))
MAX_PAGES_PER_LIST = int(os.environ.get("MAX_PAGES", "50"))

TMDB = "https://api.themoviedb.org/3"
IMDB_RATINGS_URL = "https://datasets.imdbws.com/title.ratings.tsv.gz"
IMDB_EPISODE_URL = "https://datasets.imdbws.com/title.episode.tsv.gz"

# Discover sweeps run for each kind to widen the catalog past what
# top_rated/popular cover. Note: TMDB's discover/tv supports the same
# sort_by + vote_count keys as discover/movie, so the sweep specs are
# kind-agnostic. The only kind-specific param is the date field
# (primary_release_date for movies, first_air_date for tv) — patched in
# `discover_params`.
DISCOVER_SWEEPS = [
    {"sort_by": "vote_count.desc", "vote_count_gte": 5000},
    {"sort_by": "popularity.desc", "release_date_gte": "2024-01-01"},
    {"sort_by": "popularity.desc", "release_date_gte": "2023-01-01"},
    {"sort_by": "vote_average.desc", "vote_count_gte": 1000, "with_original_language": "en"},
]


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------


def _tmdb_get(path: str, params: dict | None = None, retries: int = 4) -> dict:
    p = {"api_key": API_KEY, "language": LANGUAGE}
    if params:
        p.update(params)
    url = f"{TMDB}{path}?{urlencode(p)}"
    delay = 1.0
    for _ in range(retries):
        try:
            req = Request(url, headers={"Accept": "application/json"})
            with urlopen(req, timeout=20) as r:
                return json.loads(r.read().decode("utf-8"))
        except HTTPError as e:
            if e.code == 429 or 500 <= e.code < 600:
                time.sleep(delay)
                delay *= 2
                continue
            raise
        except URLError:
            time.sleep(delay)
            delay *= 2
    raise RuntimeError(f"TMDB GET failed: {url}")


# ---------------------------------------------------------------------------
# IMDb ratings
# ---------------------------------------------------------------------------


def load_imdb_ratings() -> dict[str, tuple[float, int]]:
    cache = CACHE_DIR / "title.ratings.tsv.gz"
    if not cache.exists() or cache.stat().st_size < 1000:
        print("  ↓ downloading IMDb ratings dump …", flush=True)
        with urlopen(IMDB_RATINGS_URL, timeout=120) as r:
            cache.write_bytes(r.read())

    ratings: dict[str, tuple[float, int]] = {}
    with gzip.open(cache, "rt", encoding="utf-8") as f:
        next(f)
        for line in f:
            tconst, avg, votes = line.rstrip("\n").split("\t")
            try:
                ratings[tconst] = (float(avg), int(votes))
            except ValueError:
                continue
    print(f"  ✓ {len(ratings):,} IMDb rating rows loaded")
    return ratings


def load_show_episodes(
    parent_tt_ids: set[str], imdb: dict[str, tuple[float, int]]
) -> dict[str, list[dict]]:
    """Per-episode ratings keyed by parent series tt id.

    Streams title.episode.tsv.gz once and only keeps episodes whose
    parent series is in `parent_tt_ids`. Episodes without a published
    rating are dropped — heatmap squares would have nothing to colour.
    """
    cache = CACHE_DIR / "title.episode.tsv.gz"
    if not cache.exists() or cache.stat().st_size < 10_000_000:
        print("  ↓ downloading IMDb episodes dump (~150 MB) …", flush=True)
        with urlopen(IMDB_EPISODE_URL, timeout=300) as r:
            cache.write_bytes(r.read())

    by_parent: dict[str, list[dict]] = {}
    rows = 0
    with gzip.open(cache, "rt", encoding="utf-8") as f:
        next(f)  # header
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 4:
                continue
            ep_tt, parent_tt, season, episode = parts[0], parts[1], parts[2], parts[3]
            if parent_tt not in parent_tt_ids:
                continue
            if season == "\\N" or episode == "\\N":
                continue
            try:
                s, e = int(season), int(episode)
            except ValueError:
                continue
            r_v = imdb.get(ep_tt)
            if not r_v:
                continue
            by_parent.setdefault(parent_tt, []).append(
                {"s": s, "e": e, "r": r_v[0], "v": r_v[1]}
            )
            rows += 1
    for k in by_parent:
        by_parent[k].sort(key=lambda x: (x["s"], x["e"]))
    print(f"  ✓ {rows:,} episode ratings across {len(by_parent):,} shows")
    return by_parent


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------


def discover_params(kind: str, sweep: dict) -> dict:
    """Map the kind-agnostic sweep spec to the right TMDB query keys."""
    out: dict = {}
    for k, v in sweep.items():
        if k.startswith("release_date_"):
            field = "primary_release_date" if kind == "movie" else "first_air_date"
            out[k.replace("release_date", field).replace("_gte", ".gte").replace("_lte", ".lte")] = v
        else:
            out[k.replace("_gte", ".gte").replace("_lte", ".lte")] = v
    return out


def collect_ids(kind: str) -> set[int]:
    """Gather candidate TMDB ids for either 'movie' or 'tv'."""
    ids: set[int] = set()

    def page_iter(path: str, label: str, max_pages: int, base_params: dict | None = None):
        for page in range(1, max_pages + 1):
            params = {"page": page}
            if base_params:
                params.update(base_params)
            try:
                data = _tmdb_get(path, params)
            except Exception as exc:
                print(f"    ! {label} page {page} failed: {exc}", flush=True)
                break
            results = data.get("results") or []
            if not results:
                break
            ids.update(m["id"] for m in results if m.get("id"))
            if page == data.get("total_pages"):
                break
        print(f"  ✓ {label}: cumulative {len(ids):,} ids", flush=True)

    print(f"\n→ {kind}/top_rated …", flush=True)
    page_iter(f"/{kind}/top_rated", f"{kind}/top_rated", MAX_PAGES_PER_LIST)

    print(f"→ {kind}/popular …", flush=True)
    page_iter(f"/{kind}/popular", f"{kind}/popular", MAX_PAGES_PER_LIST)

    for i, sweep in enumerate(DISCOVER_SWEEPS, 1):
        params = discover_params(kind, sweep)
        print(f"→ discover/{kind} sweep {i}: {sweep}", flush=True)
        page_iter(f"/discover/{kind}", f"discover/{kind}#{i}", MAX_PAGES_PER_LIST, params)

    return ids


# ---------------------------------------------------------------------------
# Enrichment
# ---------------------------------------------------------------------------


def best_trailer_id(videos: list[dict]) -> str | None:
    if not videos:
        return None
    candidates = [
        v for v in videos
        if v.get("site") == "YouTube" and v.get("type") == "Trailer"
    ]
    if not candidates:
        candidates = [v for v in videos if v.get("site") == "YouTube"]
    if not candidates:
        return None
    candidates.sort(key=lambda v: (
        not v.get("official", False),
        -(v.get("size") or 0),
    ))
    return candidates[0].get("key")


def extract_providers(detail: dict) -> list[dict]:
    block = (detail.get("watch/providers") or {}).get("results") or {}
    region = block.get(REGION) or block.get("US") or {}
    out: list[dict] = []
    seen: set[int] = set()
    for bucket in ("flatrate", "ads", "free"):
        for p in region.get(bucket) or []:
            pid = p.get("provider_id")
            if not pid or pid in seen:
                continue
            seen.add(pid)
            out.append({"id": pid, "name": p.get("provider_name"), "logo": p.get("logo_path")})
    return out


def fetch_movie(tmdb_id: int, imdb: dict[str, tuple[float, int]]) -> dict | None:
    try:
        d = _tmdb_get(
            f"/movie/{tmdb_id}",
            {"append_to_response": "external_ids,watch/providers,videos"},
        )
    except Exception:
        return None
    if d.get("adult"):
        return None
    title = d.get("title")
    poster = d.get("poster_path")
    if not title or not poster:
        return None

    imdb_id = (d.get("external_ids") or {}).get("imdb_id")
    imdb_rating = imdb_votes = None
    if imdb_id and imdb_id in imdb:
        imdb_rating, imdb_votes = imdb[imdb_id]

    release_date = d.get("release_date") or ""
    return {
        "mediaType": "movie",
        "tmdbId": d.get("id"),
        "imdbId": imdb_id,
        "title": title,
        "originalTitle": d.get("original_title"),
        "year": release_date[:4] if len(release_date) >= 4 else "",
        "releaseDate": release_date,
        "genres": [g.get("name") for g in d.get("genres") or [] if g.get("name")],
        "runtime": d.get("runtime") or None,
        "overview": (d.get("overview") or "").strip() or None,
        "poster": f"https://image.tmdb.org/t/p/w500{poster}",
        "backdrop": (
            f"https://image.tmdb.org/t/p/original{d['backdrop_path']}"
            if d.get("backdrop_path") else None
        ),
        "tmdbRating": d.get("vote_average") or None,
        "tmdbVotes": d.get("vote_count") or 0,
        "imdbRating": imdb_rating,
        "imdbVotes": imdb_votes,
        "providers": extract_providers(d),
        "trailerYoutubeId": best_trailer_id((d.get("videos") or {}).get("results") or []),
        "popularity": d.get("popularity") or 0,
        "seasons": None,
        "episodes": None,
    }


def fetch_tv(tmdb_id: int, imdb: dict[str, tuple[float, int]]) -> dict | None:
    try:
        d = _tmdb_get(
            f"/tv/{tmdb_id}",
            {"append_to_response": "external_ids,watch/providers,videos"},
        )
    except Exception:
        return None
    if d.get("adult"):
        return None
    name = d.get("name")
    poster = d.get("poster_path")
    if not name or not poster:
        return None

    imdb_id = (d.get("external_ids") or {}).get("imdb_id")
    imdb_rating = imdb_votes = None
    if imdb_id and imdb_id in imdb:
        imdb_rating, imdb_votes = imdb[imdb_id]

    runtimes = d.get("episode_run_time") or []
    avg_runtime = round(sum(runtimes) / len(runtimes)) if runtimes else None

    first_air = d.get("first_air_date") or ""
    return {
        "mediaType": "tv",
        "tmdbId": d.get("id"),
        "imdbId": imdb_id,
        "title": name,
        "originalTitle": d.get("original_name"),
        "year": first_air[:4] if len(first_air) >= 4 else "",
        "releaseDate": first_air,
        "genres": [g.get("name") for g in d.get("genres") or [] if g.get("name")],
        "runtime": avg_runtime,
        "overview": (d.get("overview") or "").strip() or None,
        "poster": f"https://image.tmdb.org/t/p/w500{poster}",
        "backdrop": (
            f"https://image.tmdb.org/t/p/original{d['backdrop_path']}"
            if d.get("backdrop_path") else None
        ),
        "tmdbRating": d.get("vote_average") or None,
        "tmdbVotes": d.get("vote_count") or 0,
        "imdbRating": imdb_rating,
        "imdbVotes": imdb_votes,
        "providers": extract_providers(d),
        "trailerYoutubeId": best_trailer_id((d.get("videos") or {}).get("results") or []),
        "popularity": d.get("popularity") or 0,
        "seasons": d.get("number_of_seasons") or None,
        "episodes": d.get("number_of_episodes") or None,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def enrich_set(kind: str, ids: set[int], imdb: dict, fetch_fn) -> list[dict]:
    out: list[dict] = []
    done = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(fetch_fn, i, imdb): i for i in ids}
        for fut in as_completed(futures):
            done += 1
            if done % 100 == 0:
                print(f"    {kind}: {done}/{len(futures)}", flush=True)
            try:
                m = fut.result()
            except Exception:
                continue
            if m:
                out.append(m)
    return out


def main() -> None:
    print("Worth2Watch — building catalog (movies + TV)\n")
    print(f"region={REGION} language={LANGUAGE} workers={WORKERS} max_pages={MAX_PAGES_PER_LIST}")

    print("\nStep 1 — IMDb ratings dump")
    imdb_ratings = load_imdb_ratings()

    print("\nStep 2 — collect TMDB ids")
    movie_ids = collect_ids("movie")
    tv_ids = collect_ids("tv")
    print(f"\n  → {len(movie_ids):,} movie ids, {len(tv_ids):,} tv ids")

    print("\nStep 3 — enrich")
    movies = enrich_set("movie", movie_ids, imdb_ratings, fetch_movie)
    print(f"  ✓ {len(movies):,} movies enriched")
    shows = enrich_set("tv", tv_ids, imdb_ratings, fetch_tv)
    print(f"  ✓ {len(shows):,} tv shows enriched")

    print("\nStep 4 — episode ratings (heatmap data)")
    parent_tts = {s["imdbId"] for s in shows if s.get("imdbId")}
    print(f"  • lookup window: {len(parent_tts):,} TV shows with IMDb ids")
    ep_map = load_show_episodes(parent_tts, imdb_ratings)
    for s in shows:
        ep = ep_map.get(s.get("imdbId") or "", [])
        s["episodeRatings"] = ep
        if ep:
            ratings_only = [e["r"] for e in ep]
            s["avgEpisodeRating"] = round(
                sum(ratings_only) / len(ratings_only), 1
            )

    catalog = movies + shows
    catalog.sort(
        key=lambda m: (
            -(m.get("imdbRating") or 0),
            -(m.get("tmdbRating") or 0),
            -(m.get("popularity") or 0),
        )
    )

    out = PUBLIC_DIR / "movies.json"
    PUBLIC_DIR.mkdir(exist_ok=True)
    out.write_text(json.dumps(catalog, ensure_ascii=False, separators=(",", ":")))
    print(f"\n✓ wrote {out}  ({out.stat().st_size / 1024:.0f} KB)")

    def coverage(items: list[dict], kind_label: str) -> None:
        if not items:
            return
        wi = sum(1 for m in items if m["imdbRating"] is not None)
        wp = sum(1 for m in items if m["providers"])
        wt = sum(1 for m in items if m["trailerYoutubeId"])
        print(f"\n{kind_label}: {len(items):,}")
        print(f"  IMDb: {wi:,} ({100*wi/len(items):.0f}%)")
        print(f"  TR provider: {wp:,} ({100*wp/len(items):.0f}%)")
        print(f"  Trailer: {wt:,} ({100*wt/len(items):.0f}%)")

    coverage(movies, "Movies")
    coverage(shows, "TV shows")
    print(f"\nTotal: {len(catalog):,}")


if __name__ == "__main__":
    main()
