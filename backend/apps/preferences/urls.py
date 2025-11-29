"""
URL configuration for preferences app.
"""
from django.urls import path
from .views import (
    WatchlistListCreateView, WatchlistDetailView,
    FavoriteGenreListCreateView, FavoriteGenreDetailView,
    SportsPreferenceListCreateView, SportsPreferenceDetailView
)

app_name = 'preferences'

urlpatterns = [
    # Watchlist
    path('watchlist/', WatchlistListCreateView.as_view(), name='watchlist'),
    path('watchlist/<int:pk>/', WatchlistDetailView.as_view(), name='watchlist_detail'),

    # Favorite Genres
    path('favorite-genres/', FavoriteGenreListCreateView.as_view(), name='favorite_genres'),
    path('favorite-genres/<int:pk>/', FavoriteGenreDetailView.as_view(), name='favorite_genre_detail'),

    # Sports Preferences
    path('sports/', SportsPreferenceListCreateView.as_view(), name='sports_preferences'),
    path('sports/<int:pk>/', SportsPreferenceDetailView.as_view(), name='sports_preference_detail'),
]
