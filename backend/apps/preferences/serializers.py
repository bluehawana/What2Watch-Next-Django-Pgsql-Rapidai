"""
Serializers for preferences app.
"""
from rest_framework import serializers
from .models import WatchlistItem, FavoriteGenre, SportsPreference
from apps.content.serializers import MovieSerializer, TVShowSerializer, GenreSerializer


class WatchlistItemSerializer(serializers.ModelSerializer):
    movie_detail = MovieSerializer(source='movie', read_only=True)
    tv_show_detail = TVShowSerializer(source='tv_show', read_only=True)

    class Meta:
        model = WatchlistItem
        fields = [
            'id', 'content_type', 'movie', 'tv_show',
            'movie_detail', 'tv_show_detail', 'priority', 'added_at'
        ]
        read_only_fields = ['added_at']


class FavoriteGenreSerializer(serializers.ModelSerializer):
    genre_detail = GenreSerializer(source='genre', read_only=True)

    class Meta:
        model = FavoriteGenre
        fields = ['id', 'genre', 'genre_detail', 'preference_level']


class SportsPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportsPreference
        fields = [
            'id', 'sport_type', 'favorite_teams', 'favorite_leagues',
            'notify_on_matches'
        ]
