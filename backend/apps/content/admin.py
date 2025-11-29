"""
Admin configuration for content app.
"""
from django.contrib import admin
from .models import (
    StreamingPlatform, Genre, Movie, TVShow,
    SportsEvent, TVChannel, TVProgram
)


@admin.register(StreamingPlatform)
class StreamingPlatformAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'rating', 'created_at')
    list_filter = ('release_date', 'genres', 'platforms')
    search_fields = ('title', 'original_title', 'imdb_id')
    filter_horizontal = ('genres', 'platforms')


@admin.register(TVShow)
class TVShowAdmin(admin.ModelAdmin):
    list_display = ('title', 'first_air_date', 'status', 'number_of_seasons', 'rating')
    list_filter = ('status', 'first_air_date', 'genres', 'platforms')
    search_fields = ('title', 'original_title', 'imdb_id')
    filter_horizontal = ('genres', 'platforms')


@admin.register(SportsEvent)
class SportsEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'sport_type', 'event_date', 'status', 'league')
    list_filter = ('sport_type', 'status', 'event_date', 'league')
    search_fields = ('title', 'home_team', 'away_team', 'league')
    filter_horizontal = ('streaming_platforms',)


@admin.register(TVChannel)
class TVChannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'channel_number', 'country', 'is_active')
    list_filter = ('country', 'is_active')
    search_fields = ('name', 'channel_number')


@admin.register(TVProgram)
class TVProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'channel', 'start_time', 'end_time')
    list_filter = ('channel', 'start_time', 'category')
    search_fields = ('title', 'description')
