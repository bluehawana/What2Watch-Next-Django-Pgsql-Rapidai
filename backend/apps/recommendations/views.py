"""
Views for recommendations app.
"""
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from apps.content.models import Movie, TVShow, SportsEvent
from apps.content.serializers import MovieSerializer, TVShowSerializer, SportsEventSerializer
from apps.users.models import UserProfile
from apps.preferences.models import FavoriteGenre, SportsPreference


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_recommendations(request):
    """
    Get personalized recommendations for the authenticated user.
    """
    user = request.user
    profile = UserProfile.objects.get(user=user)

    # Get user's favorite genres
    favorite_genres = FavoriteGenre.objects.filter(user=user).values_list('genre', flat=True)

    # Get user's subscribed platforms
    subscribed_platforms = []
    if profile.has_netflix:
        subscribed_platforms.append('netflix')
    if profile.has_prime_video:
        subscribed_platforms.append('prime-video')
    if profile.has_disney_plus:
        subscribed_platforms.append('disney-plus')
    # ... add more platforms

    # Recommend movies
    movies = Movie.objects.filter(
        genres__in=favorite_genres
    ).distinct()[:10]

    # Recommend TV shows
    tv_shows = TVShow.objects.filter(
        genres__in=favorite_genres
    ).distinct()[:10]

    # Recommend sports events
    sports_preferences = SportsPreference.objects.filter(user=user)
    sports_types = sports_preferences.values_list('sport_type', flat=True)
    sports_events = SportsEvent.objects.filter(
        sport_type__in=sports_types,
        status='SCHEDULED'
    )[:10]

    return Response({
        'movies': MovieSerializer(movies, many=True).data,
        'tv_shows': TVShowSerializer(tv_shows, many=True).data,
        'sports_events': SportsEventSerializer(sports_events, many=True).data,
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_daily_picks(request):
    """
    Get daily personalized content picks.
    """
    user = request.user

    # Logic for daily picks based on user profile type
    # This will be enhanced with more sophisticated algorithms

    return Response({
        'message': 'Daily picks feature coming soon!',
    })
