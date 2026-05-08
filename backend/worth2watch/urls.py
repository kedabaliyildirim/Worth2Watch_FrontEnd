"""Top-level URL routing.

Mirrors the v1 Express prefixes:
  /auth     → register / login
  /movie    → CRUD + listing
  /settings → profile picture / email / password
"""

from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def health(_request):
    """Cheap liveness probe — useful for keep-alive cron pings."""
    return JsonResponse({"status": "ok", "service": "worth2watch-backend"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", health),
    path("health/", health),
    path("auth/", include("accounts.urls")),
    path("movie/", include("movies.urls")),
    path("settings/", include("settings_app.urls")),
]
