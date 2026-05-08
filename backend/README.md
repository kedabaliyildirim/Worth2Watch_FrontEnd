# Worth2Watch Backend (Django + DRF)

A Django REST Framework backend that mirrors the v1 Express+MongoDB API
surface (`/auth`, `/movie`, `/settings`) one-for-one. Real, runnable,
JWT-secured.

The static `movies.json` catalog still drives the v2 frontend's
"is it worth watching?" reads — this backend is for the parts the
static file can't do: user accounts, admin-curated content, and
anything that needs persistence beyond a build.

## Quick start

### Option A — Docker (zero local Python needed)

```bash
cd backend
docker compose up --build
```

That brings up Postgres + Django, runs migrations, and serves on
[http://localhost:8000](http://localhost:8000).

### Option B — Local Python venv (SQLite, no Docker)

```bash
cd backend
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

Visit [http://localhost:8000/health/](http://localhost:8000/health/) —
should return `{"status": "ok"}`.

## Endpoints

Mirrors `begumis/Movie_App` exactly (modulo trailing slashes that DRF
prefers):

| Method | Path                              | Auth     | Notes |
|--------|-----------------------------------|----------|-------|
| GET    | `/health/`                        | —        | Liveness probe |
| POST   | `/auth/register`                  | —        | Body: `email`, `password`, `name`, `surname`, `gender?`, `birth_date?` |
| POST   | `/auth/login`                     | —        | Returns `{user, token, access, refresh}` |
| GET    | `/movie/?page=1&genre=Drama`      | —        | Paginated list, page size 6 |
| GET    | `/movie/<id>/`                    | —        | Single |
| POST   | `/movie/`                         | admin    | Create |
| PATCH  | `/movie/<id>/`                    | admin    | Update |
| DELETE | `/movie/<id>/`                    | admin    | Delete |
| PATCH  | `/settings/profile-picture`       | user     | Update own profile picture |
| PATCH  | `/settings/email`                 | user     | Update own email |
| PATCH  | `/settings/password`              | user     | Update own password |
| GET    | `/admin/`                         | admin    | Django admin UI |

All authenticated routes use `Authorization: Bearer <token>` with the
JWT returned from `/auth/login`. The token includes a `role` claim;
`role=admin` is required for movie mutations.

### Curl examples

```bash
# Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"hunter2","name":"Alice","surname":"Cooper"}'

# Login → grab a token
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"hunter2"}' | jq -r .token)

# List movies
curl http://localhost:8000/movie/

# Update own profile picture
curl -X PATCH http://localhost:8000/settings/profile-picture \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"profile_picture":"https://example.com/avatar.jpg"}'
```

### Creating an admin

```bash
python manage.py createsuperuser
```

Or in code:

```python
from accounts.models import User
User.objects.create_superuser(
    email="admin@worth2watch.dev", password="admin123",
    name="Admin", surname="Root",
)
```

## What v1 had that v2 doesn't (yet)

- The v1 NLP / sentiment-analysis pipeline (Python comment scrapers
  feeding a custom model). v2 replaces this entirely with the static
  Letterboxd / IMDb / TMDB → LLM verdict bake — see
  `scripts/build_worth_summaries.py` in the repo root.
- v1 also stored a curated movie list directly in the DB. v2 mostly
  reads movies from `public/movies.json` instead, so this backend's
  movie table is more of an admin-curation surface than the primary
  catalog. Both can coexist.

## Lineage

The schema, route layout, and JWT shape are a one-to-one port of
[begumis/Movie_App](https://github.com/begumis/Movie_App), originally
written in 2023 by **@kedabaliyildirim**, **@begumis**,
**@vakkaskarakurt**, **@aysegulcagli**, and **klavas35** as part of
their Adıyaman University team project.

The Express → Django port was done in 2026 to bring the v1 backend
philosophy back into the v2 repo without dragging Node + Mongoose along
for the ride. Field names, validation rules, response shapes, and the
admin/user permission split are unchanged from the original.
