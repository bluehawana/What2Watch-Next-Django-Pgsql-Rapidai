"""
Admin configuration for preferences app.
"""
from django.contrib import admin
from .models import WatchlistItem, FavoriteGenre, SportsPreference


@admin.register(WatchlistItem)
class WatchlistItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'get_title', 'priority', 'added_at')
    list_filter = ('content_type', 'priority')
    search_fields = ('user__email', 'movie__title', 'tv_show__title')

    def get_title(self, obj):
        if obj.content_type == 'MOVIE' and obj.movie:
            return obj.movie.title
        elif obj.content_type == 'TV_SHOW' and obj.tv_show:
            return obj.tv_show.title
        return 'N/A'
    get_title.short_description = 'Title'


@admin.register(FavoriteGenre)
class FavoriteGenreAdmin(admin.ModelAdmin):
    list_display = ('user', 'genre', 'preference_level')
    list_filter = ('genre', 'preference_level')
    search_fields = ('user__email', 'genre__name')


@admin.register(SportsPreference)
class SportsPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'sport_type', 'notify_on_matches')
    list_filter = ('sport_type', 'notify_on_matches')
    search_fields = ('user__email', 'sport_type')
