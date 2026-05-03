#!/usr/bin/env python3
"""
Quick backfill: pull English `overview` for every catalog item from TMDB
and overwrite the Turkish one in public/movies.json. Posters/genres etc.
stay as-is — only the synopsis text is touched.

Run:
    TMDB_API_KEY=... python3 scripts/backfill_overviews_en.py
"""

from __future__ import annotations

import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public" / "movies.json"

KEY = os.environ.get("TMDB_API_KEY", "").strip()
if not KEY:
    sys.exit("TMDB_API_KEY required")


def fetch_overview(item: dict) -> tuple[int, str | None]:
    kind = item["mediaType"]
    tid = item["tmdbId"]
    url = (
        f"https://api.themoviedb.org/3/{kind}/{tid}"
        f"?{urlencode({'api_key': KEY, 'language': 'en-US'})}"
    )
    try:
        req = Request(url, headers={"Accept": "application/json"})
        with urlopen(req, timeout=20) as r:
            data = json.loads(r.read().decode("utf-8"))
        ov = (data.get("overview") or "").strip()
        return tid, ov or None
    except Exception:
        return tid, None


def main() -> None:
    catalog = json.loads(PUBLIC.read_text())
    print(f"Loaded {len(catalog):,} items")

    by_id: dict[tuple[str, int], dict] = {(m["mediaType"], m["tmdbId"]): m for m in catalog}

    done = 0
    updated = 0
    with ThreadPoolExecutor(max_workers=12) as pool:
        futures = {pool.submit(fetch_overview, m): (m["mediaType"], m["tmdbId"]) for m in catalog}
        for fut in as_completed(futures):
            done += 1
            mt_tid = futures[fut]
            try:
                _, overview = fut.result()
            except Exception:
                continue
            if overview:
                by_id[mt_tid]["overview"] = overview
                updated += 1
            if done % 100 == 0:
                print(f"  {done}/{len(catalog)} (updated {updated})", flush=True)

    PUBLIC.write_text(json.dumps(catalog, ensure_ascii=False, separators=(",", ":")))
    print(f"\n✓ done: {updated:,}/{len(catalog):,} overviews refreshed in English")


if __name__ == "__main__":
    main()
