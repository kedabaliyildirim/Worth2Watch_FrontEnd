# Worth2Watch

> _Is it worth watching?_ — a curated film & series discovery app that
> answers the only question that matters before you press play.

Worth2Watch surfaces 1500+ hand-ranked movies and TV shows, each with a
plain-language **Worth Watching** verdict synthesised from real user
reviews on Letterboxd, IMDb, MyAnimeList, and TMDB. No fan-service, no
score worship, just an honest read on how audiences actually felt.

## Architecture

The current build is a **fully static SPA** — no backend, no database,
no runtime API. Everything lives in a single `public/movies.json`
(~3.6 MB) baked at build time and served from a CDN edge.

```
build_catalog.py    →  TMDB + IMDb dumps + Letterboxd/MAL  →  movies.json
build_worth_summaries.py  →  Groq Llama + Gemini  →  worth verdicts (cached)
Vue 3 + Vite + Tailwind 4  →  reads movies.json once, renders 1500 cards
```

The verdict pipeline rotates across 14 LLM backend slots (Groq Llama
70B + 8B, six Gemini API keys × two models) so it can fan a free-tier
budget across thousands of items without hitting any single quota wall.

**Why no backend?** Earlier iterations of this project ran a Node/Express
server with a database for auth, content moderation, and Reddit +
YouTube comment scraping pipelines (see _Project History_ below). That
architecture solved real problems for the v1 product, but the v2
product — "is it worth watching, in one paragraph" — needs none of it.
A static catalog refreshed weekly by a cron job is faster, cheaper,
and has zero cold-start risk.

## Stack

- **Frontend:** Vue 3.5, Vite 7, Tailwind 4, vue-router, lucide-vue-next
- **Data pipeline:** Python 3 (urllib, ThreadPoolExecutor, cloudscraper)
- **LLM backends:** Groq (Llama 3.3 70B + 3.1 8B), Google Gemini 2.5 Flash + Flash Lite
- **Sources:** TMDB API, IMDb GraphQL, IMDb non-commercial datasets, Letterboxd, MyAnimeList (Jikan)
- **Hosting:** Netlify / Vercel (static SPA + edge caching)

## Setup

```bash
npm install
npm run dev
```

To rebuild the catalog from scratch:

```bash
TMDB_API_KEY=...                                       \
GROQ_API_KEY=...                                       \
GEMINI_API_KEYS=key1,key2,key3,key4,key5,key6          \
python3 scripts/build_catalog.py                       # ~10 min
python3 scripts/build_worth_summaries.py               # ~hours, free-tier paced
python3 scripts/backfill_overviews_en.py               # English synopses
```

## Project History

Worth2Watch began life in **December 2023** as a five-person student
team project at Adıyaman University. The original ambition was bigger
than the current static surface suggests — a full-stack web app with
auth, content moderation, NLP-driven sentiment analysis on YouTube and
Reddit comments, and a curated database that admins could grow over
time.

### v1 (2023-2024) — Full-stack prototype

The first iteration shipped:

- **Frontend** _(this repo)_ — Vue 3.3 + Vuex + Vue Router, hand-styled
  CSS, admin panel for content moderation, search + sort + sentiment
  views.
- **Backend** _(see [`begumis/Movie_App`](https://github.com/begumis/Movie_App))_ —
  Node/Express server with `auth.js`, `movie.js`, and `user.js` routes,
  Mongoose models, and a Python comment-scraping pipeline that pulled
  YouTube and Reddit threads through a sentiment analyzer to feed the
  per-movie "audience mood" view.

The team behind v1:

- **[@kedabaliyildirim](https://github.com/kedabaliyildirim)** — Backend
  architecture, auth, NLP pipeline, content-moderation system, project
  lead. The bulk of the v1 server-side code is his.
- **[@begumis](https://github.com/begumis)** — Search, recommendation,
  and movie components; backend repo owner.
- **[@vakkaskarakurt](https://github.com/vakkaskarakurt)** — Singular
  movie view + TMDB integration scaffolding.
- **aysegulcagli** — App shell + navigation.
- **klavas35** — Cross-component wiring + state plumbing.

### v2 (2026) — Static rewrite, "is it worth watching?" angle

In May 2026 the project was modernised end-to-end and re-scoped around
a single, sharper question: _is this worth my evening?_

- **[@EmrahFidan](https://github.com/EmrahFidan)** — Frontend overhaul,
  catalog pipeline, LLM verdict pipeline, English-first UX, Netlify
  deploy config, and assorted bugfixes.
- **[@kedabaliyildirim](https://github.com/kedabaliyildirim)** — Final
  consolidation merge to `master`, re-scoped the project's identity
  around static delivery.

**What v2 kept from v1:** the team's original instinct that the value
isn't in the score number — it's in synthesised audience sentiment. v1
tried to do this with home-grown scrapers and a custom sentiment model;
v2 replaces that with LLMs reading real Letterboxd / IMDb / MAL reviews,
but the underlying philosophy is unchanged.

**What v2 dropped:** the live backend, the database, auth, the admin
panel, the comment-scraping cron. None of them were _wrong_ — they were
load-bearing for v1's product. But the v2 surface (browse → see a
verdict → decide) doesn't justify their operational cost.

If you're spelunking through git history, the commits before
`feature/modernize-emrah` (May 2026) are the v1 frontend; the v1
backend is preserved as-is at [`begumis/Movie_App`](https://github.com/begumis/Movie_App)
for posterity.

## License

See [LICENSE](./LICENSE).
