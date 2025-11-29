"""
URL configuration for content app.
"""
from django.urls import path
from .views import (
    StreamingPlatformListView, GenreListView,
    MovieListView, MovieDetailView,
    TVShowListView, TVShowDetailView,
    SportsEventListView, SportsEventDetailView,
    TVChannelListView, TVProgramListView,
    # Streaming API views
    test_streaming_api,
    get_streaming_services,
    search_streaming_shows,
    get_show_by_id,
    get_new_shows,
)

app_name = 'content'

urlpatterns = [
    # Streaming platforms and genres
    path('platforms/', StreamingPlatformListView.as_view(), name='platforms'),
    path('genres/', GenreListView.as_view(), name='genres'),

    # Movies
    path('movies/', MovieListView.as_view(), name='movies'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),

    # TV Shows
    path('tv-shows/', TVShowListView.as_view(), name='tv_shows'),
    path('tv-shows/<int:pk>/', TVShowDetailView.as_view(), name='tv_show_detail'),

    # Sports
    path('sports/', SportsEventListView.as_view(), name='sports_events'),
    path('sports/<int:pk>/', SportsEventDetailView.as_view(), name='sports_event_detail'),

    # TV Channels and Programs
    path('tv-channels/', TVChannelListView.as_view(), name='tv_channels'),
    path('tv-programs/', TVProgramListView.as_view(), name='tv_programs'),

    # Streaming Availability API endpoints
    path('api/test/', test_streaming_api, name='test_streaming_api'),
    path('api/services/', get_streaming_services, name='streaming_services'),
    path('api/search/', search_streaming_shows, name='search_shows'),
    path('api/show/<str:show_type>/<str:show_id>/', get_show_by_id, name='show_by_id'),
    path('api/new/', get_new_shows, name='new_shows'),
]
