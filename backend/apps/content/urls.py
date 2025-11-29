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
    # Football API views
    test_football_api,
    get_premier_league_matches,
    get_live_football,
    get_todays_football,
    search_football_team,
    # Movie Recommender API views
    test_movie_recommender,
    search_movie_recommendations,
    get_recommendations_by_mood,
    get_recommendations_by_genre,
    get_family_recommendations,
    get_kids_recommendations,
    get_movie_id,
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

    # Football API endpoints
    path('api/football/test/', test_football_api, name='test_football_api'),
    path('api/football/premier-league/', get_premier_league_matches, name='premier_league_matches'),
    path('api/football/live/', get_live_football, name='live_football'),
    path('api/football/today/', get_todays_football, name='todays_football'),
    path('api/football/search-team/', search_football_team, name='search_football_team'),

    # Movie Recommender API endpoints
    path('api/movies/test/', test_movie_recommender, name='test_movie_recommender'),
    path('api/movies/search/', search_movie_recommendations, name='search_movie_recommendations'),
    path('api/movies/mood/', get_recommendations_by_mood, name='recommendations_by_mood'),
    path('api/movies/genre/', get_recommendations_by_genre, name='recommendations_by_genre'),
    path('api/movies/family/', get_family_recommendations, name='family_recommendations'),
    path('api/movies/kids/', get_kids_recommendations, name='kids_recommendations'),
    path('api/movies/id/', get_movie_id, name='get_movie_id'),
]
