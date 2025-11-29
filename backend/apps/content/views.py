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
