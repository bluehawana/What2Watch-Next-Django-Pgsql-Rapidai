"""
Views for preferences app.
"""
from rest_framework import generics, permissions
from .models import WatchlistItem, FavoriteGenre, SportsPreference
from .serializers import (
    WatchlistItemSerializer,
    FavoriteGenreSerializer,
    SportsPreferenceSerializer
)


class WatchlistListCreateView(generics.ListCreateAPIView):
    """List or create watchlist items for the authenticated user."""
    serializer_class = WatchlistItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WatchlistItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WatchlistDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a watchlist item."""
    serializer_class = WatchlistItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WatchlistItem.objects.filter(user=self.request.user)


class FavoriteGenreListCreateView(generics.ListCreateAPIView):
    """List or create favorite genres for the authenticated user."""
    serializer_class = FavoriteGenreSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FavoriteGenre.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteGenreDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a favorite genre."""
    serializer_class = FavoriteGenreSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FavoriteGenre.objects.filter(user=self.request.user)


class SportsPreferenceListCreateView(generics.ListCreateAPIView):
    """List or create sports preferences for the authenticated user."""
    serializer_class = SportsPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SportsPreference.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SportsPreferenceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a sports preference."""
    serializer_class = SportsPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SportsPreference.objects.filter(user=self.request.user)
