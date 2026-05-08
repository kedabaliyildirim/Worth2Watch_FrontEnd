"""Movie model — v1 Mongoose schema (movieTitle/filmCover/releaseDate/
description/genre) lifted into Django one-to-one."""

from django.db import models


class Movie(models.Model):
    movie_title = models.CharField(max_length=300)
    film_cover = models.URLField(max_length=500)
    release_date = models.DateField()
    description = models.TextField()
    genre = models.CharField(max_length=120, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-release_date",)

    def __str__(self):
        return f"{self.movie_title} ({self.release_date.year})"
