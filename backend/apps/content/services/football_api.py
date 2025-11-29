"""
API-Football Client for football/soccer data
Documentation: https://www.api-football.com/documentation-v3
"""
import requests
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)


class FootballAPI:
    """Client for API-Football."""

    BASE_URL = "https://v3.football.api-sports.io"

    def __init__(self):
        self.api_key = settings.API_FOOTBALL_KEY
        self.headers = {
            'x-rapidapi-host': 'v3.football.api-sports.io',
            'x-rapidapi-key': self.api_key
        }

    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """
        Make a request to the Football API.

        Args:
            endpoint: API endpoint path
            params: Query parameters

        Returns:
            API response as dictionary or None if error
        """
        url = f"{self.BASE_URL}{endpoint}"

        try:
            logger.info(f"Making request to Football API: {endpoint}")
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Successfully fetched data from {endpoint}")
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Football API: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response: {e.response.text}")
            return None

    def get_leagues(self, country: Optional[str] = None, season: Optional[int] = None) -> Optional[Dict]:
        """
        Get list of leagues.

        Args:
            country: Filter by country name
            season: Filter by season year

        Returns:
            List of leagues
        """
        cache_key = f"football_leagues_{country}_{season}"
        cached_data = cache.get(cache_key)

        if cached_data:
            logger.info(f"Returning cached leagues data")
            return cached_data

        endpoint = "/leagues"
        params = {}
        if country:
            params['country'] = country
        if season:
            params['season'] = season

        data = self._make_request(endpoint, params)

        if data:
            # Cache for 7 days
            cache.set(cache_key, data, 60 * 60 * 24 * 7)

        return data

    def get_fixtures(
        self,
        league_id: Optional[int] = None,
        season: Optional[int] = None,
        date: Optional[str] = None,
        team_id: Optional[int] = None,
        status: Optional[str] = None,
        next: Optional[int] = None
    ) -> Optional[Dict]:
        """
        Get fixtures/matches.

        Args:
            league_id: League ID (e.g., 39 for Premier League)
            season: Season year
            date: Date in YYYY-MM-DD format
            team_id: Team ID
            status: Match status (NS, LIVE, FT, etc.)
            next: Get next N matches for a team

        Returns:
            Fixtures data
        """
        endpoint = "/fixtures"
        params = {}

        if league_id:
            params['league'] = league_id
        if season:
            params['season'] = season
        if date:
            params['date'] = date
        if team_id:
            params['team'] = team_id
        if status:
            params['status'] = status
        if next:
            params['next'] = next

        return self._make_request(endpoint, params)

    def get_todays_fixtures(self, league_id: Optional[int] = None) -> Optional[Dict]:
        """
        Get today's fixtures.

        Args:
            league_id: Optional league ID to filter

        Returns:
            Today's fixtures
        """
        today = datetime.now().strftime('%Y-%m-%d')
        cache_key = f"football_today_{league_id}_{today}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return cached_data

        data = self.get_fixtures(league_id=league_id, date=today)

        if data:
            # Cache for 1 hour
            cache.set(cache_key, data, 60 * 60)

        return data

    def get_premier_league_fixtures(
        self,
        season: Optional[int] = None,
        date: Optional[str] = None,
        next_matches: Optional[int] = None
    ) -> Optional[Dict]:
        """
        Get Premier League fixtures.
        Premier League ID: 39

        Args:
            season: Season year (e.g., 2024)
            date: Specific date
            next_matches: Get next N matches

        Returns:
            Premier League fixtures
        """
        PREMIER_LEAGUE_ID = 39
        current_season = season or datetime.now().year

        if next_matches:
            # Get next N matches
            return self.get_fixtures(
                league_id=PREMIER_LEAGUE_ID,
                season=current_season,
                next=next_matches
            )
        elif date:
            return self.get_fixtures(
                league_id=PREMIER_LEAGUE_ID,
                season=current_season,
                date=date
            )
        else:
            # Get today's matches
            return self.get_todays_fixtures(league_id=PREMIER_LEAGUE_ID)

    def get_live_matches(self, league_id: Optional[int] = None) -> Optional[Dict]:
        """
        Get live matches.

        Args:
            league_id: Optional league ID to filter

        Returns:
            Live matches
        """
        return self.get_fixtures(league_id=league_id, status='LIVE')

    def get_team_info(self, team_id: int) -> Optional[Dict]:
        """
        Get team information.

        Args:
            team_id: Team ID

        Returns:
            Team data
        """
        cache_key = f"football_team_{team_id}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return cached_data

        endpoint = "/teams"
        params = {'id': team_id}
        data = self._make_request(endpoint, params)

        if data:
            # Cache for 7 days
            cache.set(cache_key, data, 60 * 60 * 24 * 7)

        return data

    def search_team(self, team_name: str) -> Optional[Dict]:
        """
        Search for a team by name.

        Args:
            team_name: Team name to search

        Returns:
            Search results
        """
        endpoint = "/teams"
        params = {'search': team_name}
        return self._make_request(endpoint, params)

    def get_standings(self, league_id: int, season: int) -> Optional[Dict]:
        """
        Get league standings.

        Args:
            league_id: League ID
            season: Season year

        Returns:
            League standings
        """
        cache_key = f"football_standings_{league_id}_{season}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return cached_data

        endpoint = "/standings"
        params = {
            'league': league_id,
            'season': season
        }
        data = self._make_request(endpoint, params)

        if data:
            # Cache for 6 hours
            cache.set(cache_key, data, 60 * 60 * 6)

        return data
