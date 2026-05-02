#!/usr/bin/env python3
"""
Worth2Watch — Catalog builder.

Build a static `public/movies.json` from TMDB + IMDb without needing a
running backend. Run locally; commit the JSON. Frontend reads it at
load time.

Sources
-------
- TMDB API
  - /movie/top_rated      (highest IMDB-equivalent voted)
  - /movie/popular        (current popularity)
  - /discover/movie       (year/region sweeps for breadth)
  - /movie/{id}           (per-title detail: runtime, overview, genres)
  - /movie/{id}/external_ids   (gives IMDb tt id for cross-ref)
  - /movie/{id}/watch/providers (TR streaming availability)
  - /movie/{id}/videos    (best YouTube trailer)
- IMDb non-commercial dataset
  - title.ratings.tsv.gz  (avg rating + vote count, keyed by tt id)

Output shape (per movie):
{
  "tmdbId":      603,
  "imdbId":      "tt0133093",
  "title":       "The Matrix",
  "year":        "1999",
  "releaseDate": "1999-03-30",
  "genres":      ["Action", "Sci-Fi"],
  "runtime":     136,
  "overview":    "A computer hacker learns…",
  "poster":      "https://image.tmdb.org/t/p/w500/...jpg",
  "backdrop":    "https://image.tmdb.org/t/p/original/...jpg",
  "tmdbRating":  8.2,
  "tmdbVotes":   25000,
  "imdbRating":  8.7,
  "imdbVotes":   1900000,
  "providers":   [{"id": 8, "name": "Netflix", "logo": "/...jpg"}],
  "trailerYoutubeId": "vKQi3bBA1y8",
  "popularity":  124.5
}

Run:
    TMDB_API_KEY=... python3 scripts/build_catalog.py
"""

from __future__ import annotations

import gzip
import io
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
MAX_PAGES_PER_LIST = int(os.environ.get("MAX_PAGES", "50"))  # 50 pages × 20 = 1000 per list

TMDB = "https://api.themoviedb.org/3"
IMDB_RATINGS_URL = "https://datasets.imdbws.com/title.ratings.tsv.gz"

# Sweeps to widen the catalog beyond what top_rated/popular cover.
DISCOVER_SWEEPS = [
    {"sort_by": "vote_count.desc", "vote_count_gte": 5000},
    {"sort_by": "popularity.desc", "primary_release_date_gte": "2024-01-01"},
    {"sort_by": "popularity.desc", "primary_release_date_gte": "2023-01-01"},
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
    for attempt in range(retries):
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
    raise RuntimeError(f"TMDB GET failed after {retries} retries: {url}")


# ---------------------------------------------------------------------------
# IMDb ratings lookup
# ---------------------------------------------------------------------------


def load_imdb_ratings() -> dict[str, tuple[float, int]]:
    """Return {tt_id: (avg, votes)} from the IMDb dump."""
    cache = CACHE_DIR / "title.ratings.tsv.gz"
    if not cache.exists() or cache.stat().st_size < 1000:
        print(f"  ↓ downloading IMDb ratings dump …", flush=True)
        with urlopen(IMDB_RATINGS_URL, timeout=60) as r:
            cache.write_bytes(r.read())

    ratings: dict[str, tuple[float, int]] = {}
    with gzip.open(cache, "rt", encoding="utf-8") as f:
        next(f)  # header
        for line in f:
            tconst, avg, votes = line.rstrip("\n").split("\t")
            try:
                ratings[tconst] = (float(avg), int(votes))
            except ValueError:
                continue
    print(f"  ✓ {len(ratings):,} IMDb rating rows loaded")
    return ratings


# ---------------------------------------------------------------------------
# Discovery — gather candidate TMDB IDs
# ---------------------------------------------------------------------------


def collect_ids() -> set[int]:
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

    print("→ Top rated …", flush=True)
    page_iter("/movie/top_rated", "top_rated", MAX_PAGES_PER_LIST)

    print("→ Popular …", flush=True)
    page_iter("/movie/popular", "popular", MAX_PAGES_PER_LIST)

    for i, sweep in enumerate(DISCOVER_SWEEPS, 1):
        # TMDB discover uses dotted query keys (e.g. vote_count.gte)
        params: dict[str, str | int | float] = {}
        for k, v in sweep.items():
            params[k.replace("_gte", ".gte").replace("_lte", ".lte")] = v
        print(f"→ Discover sweep {i}: {sweep}", flush=True)
        page_iter("/discover/movie", f"discover#{i}", MAX_PAGES_PER_LIST, params)

    return ids


# ---------------------------------------------------------------------------
# Per-movie enrichment
# ---------------------------------------------------------------------------


def best_trailer_id(videos: list[dict]) -> str | None:
    if not videos:
        return None
    # Prefer official YouTube trailers
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


def fetch_movie(tmdb_id: int, imdb_ratings: dict[str, tuple[float, int]]) -> dict | None:
    try:
        detail = _tmdb_get(
            f"/movie/{tmdb_id}",
            {"append_to_response": "external_ids,watch/providers,videos"},
        )
    except Exception:
        return None
    if detail.get("adult"):
        return None
    title = detail.get("title")
    poster = detail.get("poster_path")
    if not title or not poster:
        return None

    imdb_id = (detail.get("external_ids") or {}).get("imdb_id")
    imdb_rating = imdb_votes = None
    if imdb_id and imdb_id in imdb_ratings:
        imdb_rating, imdb_votes = imdb_ratings[imdb_id]

    providers_block = (detail.get("watch/providers") or {}).get("results") or {}
    region_block = providers_block.get(REGION) or providers_block.get("US") or {}
    providers: list[dict] = []
    seen_pid: set[int] = set()
    for bucket in ("flatrate", "ads", "free"):
        for p in region_block.get(bucket) or []:
            pid = p.get("provider_id")
            if not pid or pid in seen_pid:
                continue
            seen_pid.add(pid)
            providers.append({
                "id": pid,
                "name": p.get("provider_name"),
                "logo": p.get("logo_path"),
            })

    trailer = best_trailer_id((detail.get("videos") or {}).get("results") or [])

    release_date = detail.get("release_date") or ""
    year = release_date[:4] if len(release_date) >= 4 else ""

    return {
        "tmdbId": detail.get("id"),
        "imdbId": imdb_id,
        "title": title,
        "originalTitle": detail.get("original_title"),
        "year": year,
        "releaseDate": release_date,
        "genres": [g.get("name") for g in detail.get("genres") or [] if g.get("name")],
        "runtime": detail.get("runtime") or None,
        "overview": (detail.get("overview") or "").strip() or None,
        "poster": f"https://image.tmdb.org/t/p/w500{poster}",
        "backdrop": (
            f"https://image.tmdb.org/t/p/original{detail['backdrop_path']}"
            if detail.get("backdrop_path") else None
        ),
        "tmdbRating": detail.get("vote_average") or None,
        "tmdbVotes": detail.get("vote_count") or 0,
        "imdbRating": imdb_rating,
        "imdbVotes": imdb_votes,
        "providers": providers,
        "trailerYoutubeId": trailer,
        "popularity": detail.get("popularity") or 0,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    print("Worth2Watch — building catalog\n")
    print(f"region={REGION} language={LANGUAGE} workers={WORKERS} max_pages={MAX_PAGES_PER_LIST}\n")

    print("Step 1/3 — load IMDb ratings dump")
    imdb_ratings = load_imdb_ratings()

    print("\nStep 2/3 — collect TMDB candidate ids")
    ids = collect_ids()
    print(f"\n  → {len(ids):,} unique candidate ids")

    print("\nStep 3/3 — enrich each title")
    movies: list[dict] = []
    done = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(fetch_movie, mid, imdb_ratings): mid for mid in ids}
        for fut in as_completed(futures):
            done += 1
            if done % 50 == 0:
                print(f"    {done}/{len(futures)}", flush=True)
            try:
                m = fut.result()
            except Exception:
                continue
            if m:
                movies.append(m)

    print(f"\n  ✓ {len(movies):,} movies enriched")

    # Stable sort: IMDb rating desc (when available), TMDB rating desc fallback
    movies.sort(
        key=lambda m: (
            -(m.get("imdbRating") or 0),
            -(m.get("tmdbRating") or 0),
            -(m.get("popularity") or 0),
        )
    )

    out = PUBLIC_DIR / "movies.json"
    PUBLIC_DIR.mkdir(exist_ok=True)
    out.write_text(json.dumps(movies, ensure_ascii=False, separators=(",", ":")))
    print(f"\n✓ wrote {out}  ({out.stat().st_size / 1024:.0f} KB)")

    with_imdb = sum(1 for m in movies if m["imdbRating"] is not None)
    with_provider = sum(1 for m in movies if m["providers"])
    with_trailer = sum(1 for m in movies if m["trailerYoutubeId"])
    print("\nCoverage:")
    print(f"  IMDb rating:  {with_imdb:,} / {len(movies):,} ({100*with_imdb/len(movies):.0f}%)")
    print(f"  TR provider:  {with_provider:,} / {len(movies):,} ({100*with_provider/len(movies):.0f}%)")
    print(f"  Trailer:      {with_trailer:,} / {len(movies):,} ({100*with_trailer/len(movies):.0f}%)")


if __name__ == "__main__":
    main()
