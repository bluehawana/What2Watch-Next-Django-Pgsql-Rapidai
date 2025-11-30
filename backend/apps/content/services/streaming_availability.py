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
            logger.info(
                f"Making request to Streaming Availability API: {endpoint}")
            response = requests.get(
                url, headers=self.headers, params=params, timeout=10)
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

    def get_show_by_id(
        self,
        show_id: str,
        country: str = "us",
        series_granularity: str = "episode",
        output_language: str = "en"
    ) -> Optional[Dict]:
        """
        Get show details by ID with episode-level granularity.

        Args:
            show_id: Show ID (internal ID or IMDB ID like 'tt10919420')
            country: Country code (default: 'us')
            series_granularity: Level of detail for series - 'show', 'season', or 'episode'
            output_language: Output language code (default: 'en')

        Returns:
            Show details with episodes if series_granularity is 'episode'
        """
        cache_key = f"show_detail_{show_id}_{country}_{series_granularity}"
        cached_data = cache.get(cache_key)

        if cached_data:
            logger.info(f"Returning cached data for show {show_id}")
            return cached_data

        endpoint = f"/shows/{show_id}"
        params = {
            "country": country,
            "series_granularity": series_granularity,
            "output_language": output_language
        }

        data = self._make_request(endpoint, params)

        if data:
            # Cache for 1 hour (episodes may update)
            cache.set(cache_key, data, 60 * 60)

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

    def search_by_filters(
        self,
        country: str = "us",
        catalogs: Optional[List[str]] = None,
        show_type: Optional[str] = None,
        genres: Optional[List[str]] = None,
        order_by: str = "popularity_1year",
        order_direction: str = "desc",
        year_min: Optional[int] = None,
        year_max: Optional[int] = None,
        rating_min: Optional[int] = None,
        rating_max: Optional[int] = None,
        keyword: Optional[str] = None,
        cursor: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Search shows with advanced filters and sorting by popularity.

        Args:
            country: Country code (e.g., 'us', 'gb')
            catalogs: List of streaming service catalogs (e.g., ['netflix', 'prime', 'apple', 'hbo', 'disney', 'hulu'])
            show_type: Type filter ('movie' or 'series')
            genres: List of genre filters (e.g., ['action', 'comedy', 'drama'])
            order_by: Sort field - Options:
                - 'original_title': Sort by title
                - 'release_year': Sort by release year
                - 'popularity_1day': Popularity in last 1 day
                - 'popularity_1week': Popularity in last 7 days
                - 'popularity_1month': Popularity in last 30 days
                - 'popularity_1year': Popularity in last year (default)
                - 'popularity_alltime': All-time popularity
            order_direction: 'asc' or 'desc' (default: 'desc')
            year_min: Minimum release year
            year_max: Maximum release year
            rating_min: Minimum rating (0-100)
            rating_max: Maximum rating (0-100)
            keyword: Keyword to search in title/description
            cursor: Pagination cursor for next page

        Returns:
            Search results with shows sorted by specified criteria

        Examples:
            # Get most popular movies on Netflix US (all time)
            search_by_filters(country='us', catalogs=['netflix'], show_type='movie', order_by='popularity_alltime')

            # Get trending series on Prime & Disney+ UK (last 7 days)
            search_by_filters(country='gb', catalogs=['prime', 'disney'], show_type='series', order_by='popularity_1week')

            # Get popular Apple TV+ shows (last month)
            search_by_filters(country='us', catalogs=['apple'], order_by='popularity_1month')
        """
        endpoint = "/shows/search/filters"
        params = {
            "country": country,
            "order_by": order_by,
            "order_direction": order_direction,
            "output_language": "en"
        }

        if catalogs:
            params["catalogs"] = ",".join(catalogs)
        if show_type:
            params["show_type"] = show_type
        if genres:
            params["genres"] = ",".join(genres)
        if year_min:
            params["year_min"] = year_min
        if year_max:
            params["year_max"] = year_max
        if rating_min:
            params["rating_min"] = rating_min
        if rating_max:
            params["rating_max"] = rating_max
        if keyword:
            params["keyword"] = keyword
        if cursor:
            params["cursor"] = cursor

        # Cache key based on all params
        cache_key = f"search_filters_{hash(frozenset(params.items()))}"
        cached_data = cache.get(cache_key)

        if cached_data:
            logger.info(f"Returning cached search results")
            return cached_data

        data = self._make_request(endpoint, params)

        if data:
            # Cache for 30 minutes (popularity changes)
            cache.set(cache_key, data, 60 * 30)

        return data

    def get_trending(
        self,
        country: str = "us",
        catalogs: Optional[List[str]] = None,
        show_type: Optional[str] = None,
        time_period: str = "1week"
    ) -> Optional[Dict]:
        """
        Get trending shows on streaming platforms.

        Args:
            country: Country code
            catalogs: List of streaming services (e.g., ['netflix', 'prime', 'apple', 'hbo', 'disney', 'hulu'])
            show_type: 'movie' or 'series' (None for both)
            time_period: '1day', '1week', '1month', '1year', or 'alltime'

        Returns:
            Trending shows sorted by popularity
        """
        order_by_map = {
            '1day': 'popularity_1day',
            '1week': 'popularity_1week',
            '1month': 'popularity_1month',
            '1year': 'popularity_1year',
            'alltime': 'popularity_alltime'
        }

        order_by = order_by_map.get(time_period, 'popularity_1week')

        return self.search_by_filters(
            country=country,
            catalogs=catalogs,
            show_type=show_type,
            order_by=order_by,
            order_direction='desc'
        )
