"""
Streaming Availability API Client for RapidAPI
Documentation: https://rapidapi.com/movie-of-the-night-movie-of-the-night-default/api/streaming-availability
"""
import requests
import logging
from typing import Dict, List, Optional
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)


class StreamingAvailabilityAPI:
    """Client for Streaming Availability API via RapidAPI."""

    BASE_URL = "https://streaming-availability.p.rapidapi.com"

    def __init__(self):
        self.api_key = settings.RAPIDAPI_KEY
        self.headers = {
            'x-rapidapi-host': 'streaming-availability.p.rapidapi.com',
            'x-rapidapi-key': self.api_key
        }

    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """
        Make a request to the Streaming Availability API.

        Args:
            endpoint: API endpoint path
            params: Query parameters

        Returns:
            API response as dictionary or None if error
        """
        url = f"{self.BASE_URL}{endpoint}"

        try:
            logger.info(f"Making request to Streaming Availability API: {endpoint}")
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Successfully fetched data from {endpoint}")
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Streaming Availability API: {str(e)}")
            if hasattr(e.response, 'text'):
                logger.error(f"Response: {e.response.text}")
            return None

    def get_show_details(self, show_type: str, show_id: str, country: str = "us") -> Optional[Dict]:
        """
        Get details for a specific show.

        Args:
            show_type: Type of show ('movie' or 'series')
            show_id: IMDB ID (e.g., 'tt0111161')
            country: Country code (default: 'us')

        Returns:
            Show details including streaming availability
        """
        cache_key = f"show_{show_type}_{show_id}_{country}"
        cached_data = cache.get(cache_key)

        if cached_data:
            logger.info(f"Returning cached data for {show_id}")
            return cached_data

        endpoint = f"/shows/{show_type}/{show_id}"
        params = {"country": country}
        data = self._make_request(endpoint, params)

        if data:
            # Cache for 24 hours
            cache.set(cache_key, data, 60 * 60 * 24)

        return data

    def search_shows(
        self,
        title: Optional[str] = None,
        country: str = "us",
        show_type: Optional[str] = None,
        genres: Optional[List[str]] = None,
        order_by: str = "original_title"
    ) -> Optional[Dict]:
        """
        Search for shows by various criteria.

        Args:
            title: Show title to search for
            country: Country code
            show_type: Type filter ('movie', 'series', or None for both)
            genres: List of genre filters
            order_by: Sort order

        Returns:
            Search results
        """
        endpoint = "/shows/search/title"
        params = {
            "country": country,
            "order_by": order_by
        }

        if title:
            params["title"] = title
        if show_type:
            params["show_type"] = show_type
        if genres:
            params["genres"] = ",".join(genres)

        return self._make_request(endpoint, params)

    def get_changes(self, country: str = "us", change_type: str = "new", item_type: str = "show") -> Optional[Dict]:
        """
        Get new shows or updates.

        Args:
            country: Country code
            change_type: Type of change ('new', 'removed', 'updated')
            item_type: Item type ('show' or 'addon')

        Returns:
            List of changes
        """
        endpoint = "/changes"
        params = {
            "country": country,
            "change_type": change_type,
            "item_type": item_type
        }

        return self._make_request(endpoint, params)

    def get_countries(self) -> Optional[List[Dict]]:
        """
        Get list of supported countries.

        Returns:
            List of country codes and names
        """
        cache_key = "streaming_countries"
        cached_data = cache.get(cache_key)

        if cached_data:
            return cached_data

        endpoint = "/countries"
        data = self._make_request(endpoint)

        if data:
            # Cache for 7 days (countries don't change often)
            cache.set(cache_key, data, 60 * 60 * 24 * 7)

        return data

    def get_services(self, country: str = "us") -> Optional[List[Dict]]:
        """
        Get list of available streaming services for a country.

        Args:
            country: Country code

        Returns:
            List of streaming services
        """
        cache_key = f"streaming_services_{country}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return cached_data

        endpoint = "/services"
        params = {"country": country}
        data = self._make_request(endpoint, params)

        if data:
            # Cache for 7 days
            cache.set(cache_key, data, 60 * 60 * 24 * 7)

        return data

    def get_genres(self) -> Optional[List[str]]:
        """
        Get list of available genres.

        Returns:
            List of genre names
        """
        cache_key = "streaming_genres"
        cached_data = cache.get(cache_key)

        if cached_data:
            return cached_data

        endpoint = "/genres"
        data = self._make_request(endpoint)

        if data:
            # Cache for 7 days
            cache.set(cache_key, data, 60 * 60 * 24 * 7)

        return data
