"""
AI Movie Recommender API Client
Documentation: https://rapidapi.com/
"""
import requests
import logging
from typing import Dict, List, Optional
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)


class MovieRecommenderAPI:
    """Client for AI Movie Recommender API via RapidAPI."""

    BASE_URL = "https://ai-movie-recommender.p.rapidapi.com"

    def __init__(self):
        self.api_key = settings.RAPIDAPI_KEY
        self.headers = {
            'x-rapidapi-host': 'ai-movie-recommender.p.rapidapi.com',
            'x-rapidapi-key': self.api_key,
            'User-Agent': 'Mozilla/5.0'
        }
        # Create a new session for each instance to avoid connection pooling issues
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """
        Make a request to the Movie Recommender API.

        Args:
            endpoint: API endpoint path
            params: Query parameters

        Returns:
            API response as dictionary or None if error
        """
        url = f"{self.BASE_URL}{endpoint}"

        try:
            logger.info(f"Making request to Movie Recommender API: {endpoint}")
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Successfully fetched data from {endpoint}")
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Movie Recommender API: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response: {e.response.text}")
            return None

    def search_movies(self, query: str) -> Optional[Dict]:
        """
        Search for movie recommendations based on a query.

        Args:
            query: Search query (e.g., "10s sad movies", "action movies", "romantic comedy")

        Returns:
            Movie recommendations
        """
        cache_key = f"movie_rec_{query.lower().replace(' ', '_')}"
        cached_data = cache.get(cache_key)

        if cached_data:
            logger.info(f"Returning cached movie recommendations for: {query}")
            return cached_data

        endpoint = "/api/search"
        params = {'q': query}
        data = self._make_request(endpoint, params)

        if data:
            # Cache for 6 hours
            cache.set(cache_key, data, 60 * 60 * 6)

        return data

    def get_recommendations_by_mood(self, mood: str, decade: Optional[str] = None) -> Optional[Dict]:
        """
        Get movie recommendations by mood.

        Args:
            mood: Mood/genre (e.g., "sad", "happy", "scary", "romantic")
            decade: Optional decade filter (e.g., "10s", "90s", "80s")

        Returns:
            Movie recommendations
        """
        if decade:
            query = f"{decade} {mood} movies"
        else:
            query = f"{mood} movies"

        return self.search_movies(query)

    def get_recommendations_by_genre(self, genre: str, year: Optional[int] = None) -> Optional[Dict]:
        """
        Get movie recommendations by genre.

        Args:
            genre: Movie genre (e.g., "action", "comedy", "thriller")
            year: Optional year filter

        Returns:
            Movie recommendations
        """
        if year:
            query = f"{year} {genre} movies"
        else:
            query = f"{genre} movies"

        return self.search_movies(query)

    def get_family_recommendations(self) -> Optional[Dict]:
        """
        Get family-friendly movie recommendations.

        Returns:
            Family movie recommendations
        """
        return self.search_movies("family friendly movies")

    def get_kids_recommendations(self) -> Optional[Dict]:
        """
        Get kids movie recommendations.

        Returns:
            Kids movie recommendations
        """
        return self.search_movies("kids movies")

    def get_movie_id(self, title: str) -> Optional[Dict]:
        """
        Get TMDB and IMDb IDs for a movie by title.

        Args:
            title: Movie title

        Returns:
            Dictionary with title, tmdb, and imdb IDs
        """
        cache_key = f"movie_id_{title.lower().replace(' ', '_')}"
        cached_data = cache.get(cache_key)

        if cached_data:
            logger.info(f"Returning cached movie ID for: {title}")
            return cached_data

        endpoint = "/api/getID"
        params = {'title': title}
        data = self._make_request(endpoint, params)

        if data:
            # Cache for 24 hours (movie IDs don't change)
            cache.set(cache_key, data, 60 * 60 * 24)

        return data
