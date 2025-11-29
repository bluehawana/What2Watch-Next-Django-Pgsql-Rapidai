"""
Views for content app.
"""
from rest_framework import generics, filters
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
