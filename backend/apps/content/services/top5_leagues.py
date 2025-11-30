"""
Top 5 European Leagues Service.
Provides filtered football data for Premier League, La Liga, Bundesliga, Serie A, and Ligue 1.
"""
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from django.core.cache import cache

from .football_api import FootballAPI
from .time_converter import TimeConverter
from .broadcast_service import BroadcastService

logger = logging.getLogger(__name__)


class Top5LeaguesService:
    """Service for fetching and filtering top 5 European league matches."""

    # League IDs for top 5 European leagues
    LEAGUE_IDS = {
        'premier_league': 39,
        'la_liga': 140,
        'bundesliga': 78,
        'serie_a': 135,
        'ligue_1': 61
    }

    # Reverse mapping for league names
    LEAGUE_NAMES = {
        39: {'name': 'Premier League', 'country': 'England'},
        140: {'name': 'La Liga', 'country': 'Spain'},
        78: {'name': 'Bundesliga', 'country': 'Germany'},
        135: {'name': 'Serie A', 'country': 'Italy'},
        61: {'name': 'Ligue 1', 'country': 'France'},
    }

    def __init__(self):
        self.football_api = FootballAPI()

    def get_matches(
        self,
        date: Optional[str] = None,
        league: Optional[str] = None,
        days_ahead: int = 7
    ) -> Dict:
        """
        Get matches from top 5 leagues.

        Args:
            date: Specific date (YYYY-MM-DD)
            league: League key filter (e.g., 'premier_league')
            days_ahead: Number of days to look ahead (default 7)

        Returns:
            Dict with matches and metadata
        """
        # Validate league filter
        if league and league not in self.LEAGUE_IDS:
            return {
                'error': f'Invalid league filter. Valid options: {list(self.LEAGUE_IDS.keys())}',
                'matches': []
            }

        all_matches = []

        if date:
            # Fetch for specific date
            all_matches = self._fetch_matches_for_date(date, league)
        else:
            # Fetch for date range
            all_matches = self._fetch_matches_for_range(days_ahead, league)

        return {
            'count': len(all_matches),
            'filters': {
                'date': date,
                'league': league,
                'days_ahead': days_ahead if not date else None
            },
            'matches': all_matches
        }

    def get_todays_matches(self, league: Optional[str] = None) -> Dict:
        """
        Get today's matches from top 5 leagues.

        Args:
            league: Optional league filter

        Returns:
            Dict with today's matches
        """
        today = datetime.now().strftime('%Y-%m-%d')
        return self.get_matches(date=today, league=league)

    def get_live_matches(self) -> Dict:
        """
        Get currently live matches from top 5 leagues.

        Returns:
            Dict with live matches
        """
        cache_key = "top5_live_matches"
        cached = cache.get(cache_key)
        if cached:
            return cached

        all_live = []

        for league_key, league_id in self.LEAGUE_IDS.items():
            response = self.football_api.get_live_matches(league_id=league_id)
            if response and 'response' in response:
                for fixture in response['response']:
                    enriched = self._enrich_match_data(fixture)
                    if enriched:
                        all_live.append(enriched)

        result = {
            'count': len(all_live),
            'matches': all_live
        }

        # Cache for 1 minute (live data changes frequently)
        cache.set(cache_key, result, 60)
        return result

    def _get_current_season(self) -> int:
        """
        Get the current football season year.
        Football seasons span two years (e.g., 2024-2025 season starts in 2024).
        """
        now = datetime.now()
        # If we're in Jan-July, the season started last year
        # If we're in Aug-Dec, the season started this year
        if now.month < 8:
            return now.year - 1
        return now.year

    def _fetch_matches_for_date(self, date: str, league: Optional[str] = None) -> List[Dict]:
        """Fetch matches for a specific date."""
        matches = []
        current_season = self._get_current_season()

        league_ids = [self.LEAGUE_IDS[league]] if league else list(
            self.LEAGUE_IDS.values())

        for league_id in league_ids:
            cache_key = f"top5_matches_{league_id}_{date}"
            cached = cache.get(cache_key)

            if cached:
                matches.extend(cached)
                continue

            response = self.football_api.get_fixtures(
                league_id=league_id,
                season=current_season,
                date=date
            )

            if response and 'response' in response:
                league_matches = []
                for fixture in response['response']:
                    enriched = self._enrich_match_data(fixture)
                    if enriched:
                        league_matches.append(enriched)

                # Cache for 1 hour
                cache.set(cache_key, league_matches, 60 * 60)
                matches.extend(league_matches)

        # Sort by kickoff time
        matches.sort(key=lambda x: x.get('kickoff', {}).get('utc', ''))
        return matches

    def _fetch_matches_for_range(self, days_ahead: int, league: Optional[str] = None) -> List[Dict]:
        """Fetch matches for a date range."""
        matches = []
        today = datetime.now()

        for i in range(days_ahead):
            date = (today + timedelta(days=i)).strftime('%Y-%m-%d')
            day_matches = self._fetch_matches_for_date(date, league)
            matches.extend(day_matches)

        return matches

    def _filter_top5_leagues(self, fixtures: List[Dict]) -> List[Dict]:
        """
        Filter fixtures to only include top 5 leagues.

        Args:
            fixtures: List of fixture dictionaries from API

        Returns:
            Filtered list containing only top 5 league matches
        """
        top5_ids = set(self.LEAGUE_IDS.values())
        return [
            f for f in fixtures
            if f.get('league', {}).get('id') in top5_ids
        ]

    def _enrich_match_data(self, fixture: Dict) -> Optional[Dict]:
        """
        Add Swedish time and broadcast info to match.

        Args:
            fixture: Raw fixture data from API

        Returns:
            Enriched match dictionary or None if invalid
        """
        try:
            league_data = fixture.get('league', {})
            league_id = league_data.get('id')

            # Verify it's a top 5 league
            if league_id not in self.LEAGUE_IDS.values():
                return None

            fixture_data = fixture.get('fixture', {})
            teams = fixture.get('teams', {})
            goals = fixture.get('goals', {})

            # Get UTC timestamp
            utc_timestamp = fixture_data.get('date', '')

            # Convert to Swedish time
            swedish_time_info = TimeConverter.utc_to_swedish_full(
                utc_timestamp)

            # Get broadcast channels
            broadcast_channels = BroadcastService.get_broadcast_channels(
                league_id)

            # Get league info from our mapping (ensures consistency)
            league_info = self.LEAGUE_NAMES.get(league_id, {})

            return {
                'id': fixture_data.get('id'),
                'league': {
                    'id': league_id,
                    'name': league_info.get('name', league_data.get('name', '')),
                    'country': league_info.get('country', league_data.get('country', '')),
                    'logo': league_data.get('logo', '')
                },
                'home_team': {
                    'id': teams.get('home', {}).get('id'),
                    'name': teams.get('home', {}).get('name', ''),
                    'logo': teams.get('home', {}).get('logo', '')
                },
                'away_team': {
                    'id': teams.get('away', {}).get('id'),
                    'name': teams.get('away', {}).get('name', ''),
                    'logo': teams.get('away', {}).get('logo', '')
                },
                'kickoff': {
                    'utc': utc_timestamp,
                    'swedish_time': swedish_time_info.get('time', ''),
                    'swedish_date': swedish_time_info.get('date', ''),
                    'day_of_week': swedish_time_info.get('day_of_week', ''),
                    'timezone': swedish_time_info.get('timezone', 'CET')
                },
                'status': fixture_data.get('status', {}).get('short', 'NS'),
                'score': {
                    'home': goals.get('home'),
                    'away': goals.get('away')
                },
                'broadcast_channels': broadcast_channels
            }
        except Exception as e:
            logger.error(f"Error enriching match data: {e}")
            return None

    @classmethod
    def get_valid_league_filters(cls) -> List[str]:
        """Get list of valid league filter keys."""
        return list(cls.LEAGUE_IDS.keys())
