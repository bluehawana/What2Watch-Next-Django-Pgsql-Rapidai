"""
Models for user content preferences.
"""
from django.db import models
from django.conf import settings
from apps.content.models import Genre, Movie, TVShow, SportsEvent


class WatchlistItem(models.Model):
    """User's watchlist for movies and TV shows."""
    CONTENT_TYPES = [
        ('MOVIE', 'Movie'),
        ('TV_SHOW', 'TV Show'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='watchlist'
    )
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES)
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='in_watchlists'
    )
    tv_show = models.ForeignKey(
        TVShow,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='in_watchlists'
    )
    added_at = models.DateTimeField(auto_now_add=True)
    priority = models.IntegerField(default=0)

    class Meta:
        unique_together = [['user', 'movie'], ['user', 'tv_show']]
        ordering = ['-priority', '-added_at']

    def __str__(self):
        if self.content_type == 'MOVIE' and self.movie:
            return f"{self.user.email}'s watchlist: {self.movie.title}"
        return f"{self.user.email}'s watchlist: {self.tv_show.title}"


class FavoriteGenre(models.Model):
    """User's favorite genres."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorite_genres'
    )
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    preference_level = models.IntegerField(default=5)  # 1-10 scale

    class Meta:
        unique_together = ['user', 'genre']
        ordering = ['-preference_level']

    def __str__(self):
        return f"{self.user.email} - {self.genre.name}"


class SportsPreference(models.Model):
    """User's sports preferences."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sports_preferences'
    )
    sport_type = models.CharField(max_length=50)
    favorite_teams = models.TextField(blank=True)  # Comma-separated list
    favorite_leagues = models.TextField(blank=True)  # Comma-separated list
    notify_on_matches = models.BooleanField(default=True)

    class Meta:
        unique_together = ['user', 'sport_type']

    def __str__(self):
        return f"{self.user.email} - {self.sport_type}"


