"""Movie endpoints — same surface as v1 routes/movie.js.

  GET    /movie/?page=1&sort=releaseDate&genre=Drama  → paginated list
  GET    /movie/<id>/                                  → single
  POST   /movie/                       (admin only)    → create
  PATCH  /movie/<id>/                  (admin only)    → update
  DELETE /movie/<id>/                  (admin only)    → delete
"""

from rest_framework import viewsets

from .models import Movie
from .permissions import IsAdminOrReadOnly
from .serializers import MovieSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_fields = ("genre",)
    ordering_fields = ("release_date", "movie_title", "created_at")
    ordering = ("-release_date",)
