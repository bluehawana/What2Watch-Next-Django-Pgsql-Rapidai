"""
Views for content app.
"""
from rest_framework import generics, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    StreamingPlatform, Genre, Movie, TVShow,
    SportsEvent, TVChannel, TVProgram
)
from .serializers import (
    StreamingPlatformSerializer, GenreSerializer, MovieSerializer,
    TVShowSerializer, SportsEventSerializer, TVChannelSerializer,
    TVProgramSerializer
)
from .services.streaming_availability import StreamingAvailabilityAPI
from .services.football_api import FootballAPI
from .services.movie_recommender import MovieRecommenderAPI


class StreamingPlatformListView(generics.ListAPIView):
    """List all streaming platforms."""
    queryset = StreamingPlatform.objects.filter(is_active=True)
    serializer_class = StreamingPlatformSerializer
    permission_classes = [AllowAny]


class GenreListView(generics.ListAPIView):
    """List all genres."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AllowAny]


class MovieListView(generics.ListAPIView):
    """List movies with filtering and search."""
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['genres', 'platforms', 'release_date']
    search_fields = ['title', 'original_title', 'description']
    ordering_fields = ['release_date', 'rating', 'title']
    ordering = ['-release_date']


class MovieDetailView(generics.RetrieveAPIView):
    """Get movie details."""
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]


class TVShowListView(generics.ListAPIView):
    """List TV shows with filtering and search."""
    queryset = TVShow.objects.all()
    serializer_class = TVShowSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['genres', 'platforms', 'status']
    search_fields = ['title', 'original_title', 'description']
    ordering_fields = ['first_air_date', 'rating', 'title']
    ordering = ['-first_air_date']


class TVShowDetailView(generics.RetrieveAPIView):
    """Get TV show details."""
    queryset = TVShow.objects.all()
    serializer_class = TVShowSerializer
    permission_classes = [AllowAny]


class SportsEventListView(generics.ListAPIView):
    """List sports events with filtering."""
    queryset = SportsEvent.objects.all()
    serializer_class = SportsEventSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['sport_type', 'league', 'status']
    search_fields = ['title', 'home_team', 'away_team', 'league']
    ordering_fields = ['event_date']
    ordering = ['event_date']


class SportsEventDetailView(generics.RetrieveAPIView):
    """Get sports event details."""
    queryset = SportsEvent.objects.all()
    serializer_class = SportsEventSerializer
    permission_classes = [AllowAny]


class TVChannelListView(generics.ListAPIView):
    """List TV channels."""
    queryset = TVChannel.objects.filter(is_active=True)
    serializer_class = TVChannelSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'channel_number']


class TVProgramListView(generics.ListAPIView):
    """List TV programs."""
    queryset = TVProgram.objects.all()
    serializer_class = TVProgramSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['channel', 'category']
    ordering_fields = ['start_time']
    ordering = ['start_time']


# Streaming Availability API Views

@api_view(['GET'])
@permission_classes([AllowAny])
def test_streaming_api(request):
    """
    Test endpoint for Streaming Availability API.
    """
    api = StreamingAvailabilityAPI()

    # Test fetching available countries
    countries = api.get_countries()

    if countries:
        return Response({
            'status': 'success',
            'message': 'Successfully connected to Streaming Availability API!',
            'countries_count': len(countries) if isinstance(countries, list) else None,
            'sample_countries': countries[:5] if isinstance(countries, list) else countries
        })
    else:
        return Response({
            'status': 'error',
            'message': 'Failed to connect to Streaming Availability API'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_streaming_services(request):
    """
    Get available streaming services for a country.
    Query params: country (default: 'us')
    """
    country = request.query_params.get('country', 'us')
    api = StreamingAvailabilityAPI()
    services = api.get_services(country)

    if services:
        return Response({
            'country': country,
            'services': services
        })
    else:
        return Response({
            'error': 'Failed to fetch streaming services'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['GET'])
@permission_classes([AllowAny])
def search_streaming_shows(request):
    """
    Search for shows on streaming platforms.
    Query params: title, country (default: 'us'), show_type ('movie' or 'series')
    """
    title = request.query_params.get('title')
    country = request.query_params.get('country', 'us')
    show_type = request.query_params.get('show_type')

    if not title:
        return Response({
            'error': 'Title parameter is required'
        }, status=status.HTTP_400_BAD_REQUEST)

    api = StreamingAvailabilityAPI()
    results = api.search_shows(
        title=title,
        country=country,
        show_type=show_type
    )

    if results:
        return Response(results)
    else:
        return Response({
            'error': 'Failed to search shows'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_show_by_id(request, show_type, show_id):
    """
    Get details for a specific show by IMDB ID.
    URL params: show_type ('movie' or 'series'), show_id (IMDB ID like 'tt0111161')
    Query params: country (default: 'us')
    """
    country = request.query_params.get('country', 'us')
    api = StreamingAvailabilityAPI()
    show = api.get_show_details(show_type, show_id, country)

    if show:
        return Response(show)
    else:
        return Response({
            'error': f'Failed to fetch {show_type} with ID {show_id}'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_new_shows(request):
    """
    Get newly added shows to streaming services.
    Query params: country (default: 'us')
    """
    country = request.query_params.get('country', 'us')
    api = StreamingAvailabilityAPI()
    changes = api.get_changes(country=country, change_type='new')

    if changes:
        return Response({
            'country': country,
            'changes': changes
        })
    else:
        return Response({
            'error': 'Failed to fetch new shows'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


# Football API Views

@api_view(['GET'])
@permission_classes([AllowAny])
def test_football_api(request):
    """
    Test endpoint for Football API.
    """
    api = FootballAPI()

    # Test by fetching today's Premier League fixtures
    fixtures = api.get_premier_league_fixtures()

    if fixtures:
        return Response({
            'status': 'success',
            'message': 'Successfully connected to Football API!',
            'data': fixtures
        })
    else:
        return Response({
            'status': 'error',
            'message': 'Failed to connect to Football API'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_premier_league_matches(request):
    """
    Get Premier League matches.
    Query params:
    - date (YYYY-MM-DD)
    - next (number of upcoming matches)
    - season (year)
    """
    date = request.query_params.get('date')
    next_matches = request.query_params.get('next')
    season = request.query_params.get('season')

    api = FootballAPI()

    if next_matches:
        fixtures = api.get_premier_league_fixtures(next_matches=int(next_matches))
    elif date:
        fixtures = api.get_premier_league_fixtures(date=date)
    elif season:
        fixtures = api.get_premier_league_fixtures(season=int(season))
    else:
        # Default: today's matches
        fixtures = api.get_premier_league_fixtures()

    if fixtures:
        return Response(fixtures)
    else:
        return Response({
            'error': 'Failed to fetch Premier League fixtures'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_live_football(request):
    """
    Get live football matches.
    Query params: league_id (optional)
    """
    league_id = request.query_params.get('league_id')

    api = FootballAPI()
    fixtures = api.get_live_matches(league_id=int(league_id) if league_id else None)

    if fixtures:
        return Response(fixtures)
    else:
        return Response({
            'error': 'Failed to fetch live matches'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_todays_football(request):
    """
    Get today's football matches.
    Query params: league_id (optional, e.g., 39 for Premier League)
    """
    league_id = request.query_params.get('league_id')

    api = FootballAPI()
    fixtures = api.get_todays_fixtures(league_id=int(league_id) if league_id else None)

    if fixtures:
        return Response(fixtures)
    else:
        return Response({
            'error': 'Failed to fetch today\'s matches'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['GET'])
@permission_classes([AllowAny])
def search_football_team(request):
    """
    Search for a football team.
    Query params: name (required)
    """
    team_name = request.query_params.get('name')

    if not team_name:
        return Response({
            'error': 'Team name is required'
        }, status=status.HTTP_400_BAD_REQUEST)

    api = FootballAPI()
    teams = api.search_team(team_name)

    if teams:
        return Response(teams)
    else:
        return Response({
            'error': 'Failed to search teams'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


# AI Movie Recommender API Views

@api_view(['GET'])
@permission_classes([AllowAny])
def test_movie_recommender(request):
    """
    Test endpoint for AI Movie Recommender API.
    """
    api = MovieRecommenderAPI()

    # Test with a simple query
    recommendations = api.search_movies("action movies")

    if recommendations:
        return Response({
            'status': 'success',
            'message': 'Successfully connected to AI Movie Recommender API!',
            'data': recommendations
        })
    else:
        return Response({
            'status': 'error',
            'message': 'Failed to connect to AI Movie Recommender API'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['GET'])
@permission_classes([AllowAny])
def search_movie_recommendations(request):
    """
    Search for movie recommendations.
    Query params: q (required) - search query like "10s sad movies", "action thriller"
    """
    query = request.query_params.get('q')

    if not query:
        return Response({
            'error': 'Query parameter "q" is required'
        }, status=status.HTTP_400_BAD_REQUEST)

    api = MovieRecommenderAPI()
    recommendations = api.search_movies(query)

    if recommendations:
        return Response(recommendations)
    else:
        return Response({
            'error': 'Failed to fetch movie recommendations'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_recommendations_by_mood(request):
    """
    Get movie recommendations by mood.
    Query params:
    - mood (required): e.g., "sad", "happy", "scary", "romantic"
    - decade (optional): e.g., "10s", "90s", "80s"
    """
    mood = request.query_params.get('mood')
    decade = request.query_params.get('decade')

    if not mood:
        return Response({
            'error': 'Mood parameter is required'
        }, status=status.HTTP_400_BAD_REQUEST)

    api = MovieRecommenderAPI()
    recommendations = api.get_recommendations_by_mood(mood, decade)

    if recommendations:
        return Response(recommendations)
    else:
        return Response({
            'error': 'Failed to fetch recommendations'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_recommendations_by_genre(request):
    """
    Get movie recommendations by genre.
    Query params:
    - genre (required): e.g., "action", "comedy", "thriller"
    - year (optional): specific year
    """
    genre = request.query_params.get('genre')
    year = request.query_params.get('year')

    if not genre:
        return Response({
            'error': 'Genre parameter is required'
        }, status=status.HTTP_400_BAD_REQUEST)

    api = MovieRecommenderAPI()
    recommendations = api.get_recommendations_by_genre(
        genre,
        int(year) if year else None
    )

    if recommendations:
        return Response(recommendations)
    else:
        return Response({
            'error': 'Failed to fetch recommendations'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_family_recommendations(request):
    """
    Get family-friendly movie recommendations.
    """
    api = MovieRecommenderAPI()
    recommendations = api.get_family_recommendations()

    if recommendations:
        return Response(recommendations)
    else:
        return Response({
            'error': 'Failed to fetch family recommendations'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_kids_recommendations(request):
    """
    Get kids movie recommendations.
    """
    api = MovieRecommenderAPI()
    recommendations = api.get_kids_recommendations()

    if recommendations:
        return Response(recommendations)
    else:
        return Response({
            'error': 'Failed to fetch kids recommendations'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_movie_id(request):
    """
    Get TMDB and IMDb IDs for a movie by title.
    Query params: title (required)
    """
    title = request.query_params.get('title')

    if not title:
        return Response({
            'error': 'Title parameter is required'
        }, status=status.HTTP_400_BAD_REQUEST)

    api = MovieRecommenderAPI()
    movie_data = api.get_movie_id(title)

    if movie_data:
        return Response(movie_data)
    else:
        return Response({
            'error': f'Failed to fetch movie ID for: {title}'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
