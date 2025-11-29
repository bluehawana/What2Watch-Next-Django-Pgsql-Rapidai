"""
Serializers for content app.
"""
from rest_framework import serializers
from .models import (
    StreamingPlatform, Genre, Movie, TVShow,
    SportsEvent, TVChannel, TVProgram
)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'slug']


class StreamingPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreamingPlatform
        fields = ['id', 'name', 'slug', 'logo', 'website_url', 'is_active']


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    platforms = StreamingPlatformSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'original_title', 'description', 'release_date',
            'duration_minutes', 'rating', 'poster_url', 'backdrop_url',
            'trailer_url', 'imdb_id', 'tmdb_id', 'genres', 'platforms',
            'created_at', 'updated_at'
        ]


class TVShowSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    platforms = StreamingPlatformSerializer(many=True, read_only=True)

    class Meta:
        model = TVShow
        fields = [
            'id', 'title', 'original_title', 'description', 'first_air_date',
            'last_air_date', 'number_of_seasons', 'number_of_episodes',
            'episode_duration', 'rating', 'poster_url', 'backdrop_url',
            'trailer_url', 'status', 'imdb_id', 'tmdb_id', 'genres',
            'platforms', 'created_at', 'updated_at'
        ]


class SportsEventSerializer(serializers.ModelSerializer):
    streaming_platforms = StreamingPlatformSerializer(many=True, read_only=True)

    class Meta:
        model = SportsEvent
        fields = [
            'id', 'title', 'sport_type', 'league', 'home_team', 'away_team',
            'event_date', 'venue', 'description', 'tv_channel',
            'streaming_platforms', 'status', 'external_id',
            'created_at', 'updated_at'
        ]


class TVChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TVChannel
        fields = [
            'id', 'name', 'channel_number', 'logo_url', 'website_url',
            'country', 'is_active', 'created_at', 'updated_at'
        ]


class TVProgramSerializer(serializers.ModelSerializer):
    channel = TVChannelSerializer(read_only=True)

    class Meta:
        model = TVProgram
        fields = [
            'id', 'channel', 'title', 'description', 'start_time',
            'end_time', 'category', 'created_at', 'updated_at'
        ]
