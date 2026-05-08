from rest_framework import serializers

from .models import Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            "id", "movie_title", "film_cover", "release_date",
            "description", "genre", "created_at", "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")
