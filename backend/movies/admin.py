from django.contrib import admin

from .models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("movie_title", "genre", "release_date")
    search_fields = ("movie_title", "description")
    list_filter = ("genre",)
