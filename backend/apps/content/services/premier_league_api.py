"""
Premier League API Client using RapidAPI.
Fetches upcoming matches, not historical data.
"""
import requests
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache import cache

from .time_converter import TimeConverter
from .broadcast_service import BroadcastService

logger = logging.getLogger(__name__)


class PremierLeagueAPI:
    """Client for English Premier League RapidAPI."""

    BASE_URL = "https://english-premiere-league1.p.rapidapi.com"
    LEAGUE_ID = 39  # Premier League ID for broadcast mapping

    def __init__(self):
        self.api_key = settings.RAPIDAPI_KEY
        self.headers = {
            'x-rapidapi-host': 'english-premiere-league1.p.rapidapi.com',
            'x-rapidapi-key': self.api_key
        }

    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Make request to Premier League API."""
        url = f"{self.BASE_URL}{endpoint}"

        try:
            logger.info(f"Making request to Premier League API: {endpoint}")
            response = requests.get(
                url, headers=self.headers, params=params, timeout=15)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Premier League API: {str(e)}")
            return None

    def get_upcoming_matches(self, days_ahead: int = 7) -> Dict:
        """
        Get upcoming Premier League matches.

        Args:
            days_ahead: Number of days to look ahead

        Returns:
            Dict with upcoming matches in Swedish time
        """
        now = datetime.now()
        year = now.year
        month = now.month

        cache_key = f"pl_upcoming_{year}_{month}_{days_ahead}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        # Fetch schedule for current month
        data = self._make_request("/schedule", {"year": year, "month": month})

        if not data:
            return {"count": 0, "matches": [], "error": "Failed to fetch data"}

        # Extract schedule from response
        schedule = data.get('schedule', data)

        # Also fetch next month if we're near end of month
        if now.day > 20:
            next_month = month + 1 if month < 12 else 1
            next_year = year if month < 12 else year + 1
            next_data = self._make_request(
                "/schedule", {"year": next_year, "month": next_month})
            if next_data:
                next_schedule = next_data.get('schedule', next_data)
                schedule.update(next_schedule)

        matches = self._filter_upcoming_matches(schedule, days_ahead)

        result = {
            "count": len(matches),
            "league": "Premier League",
            "matches": matches
        }

        # Cache for 1 hour
        cache.set(cache_key, result, 60 * 60)
        return result

    def get_todays_matches(self) -> Dict:
        """Get today's Premier League matches."""
        return self.get_upcoming_matches(days_ahead=1)

    def get_this_weeks_matches(self) -> Dict:
        """Get this week's Premier League matches."""
        return self.get_upcoming_matches(days_ahead=7)

    def _filter_upcoming_matches(self, data: Dict, days_ahead: int) -> List[Dict]:
        """Filter and format upcoming matches only."""
        matches = []
        now = datetime.now()
        cutoff = now + timedelta(days=days_ahead)

        for date_key, day_matches in data.items():
            if not isinstance(day_matches, list):
                continue

            for match in day_matches:
                # Skip completed matches
                status = match.get('status', {})
                if status.get('state') == 'post' or status.get('detail') == 'FT':
                    continue

                # Parse match date
                match_date_str = match.get('date', '')
                if not match_date_str:
                    continue

                try:
                    match_date = datetime.fromisoformat(
                        match_date_str.replace('Z', '+00:00'))
                    # Skip past matches
                    if match_date.replace(tzinfo=None) < now:
                        continue
                    # Skip matches beyond our window
                    if match_date.replace(tzinfo=None) > cutoff:
                        continue
                except (ValueError, TypeError):
                    continue

                formatted = self._format_match(match)
                if formatted:
                    matches.append(formatted)

        # Sort by kickoff time
        matches.sort(key=lambda x: x.get('kickoff', {}).get('utc', ''))
        return matches

    def _format_match(self, match: Dict) -> Optional[Dict]:
        """Format match data with Swedish time and broadcast info."""
        try:
            teams = match.get('teams', [])
            if len(teams) < 2:
                return None

            home_team = next((t for t in teams if t.get('isHome')), teams[1])
            away_team = next(
                (t for t in teams if not t.get('isHome')), teams[0])

            utc_time = match.get('date', '')
            swedish_time = TimeConverter.utc_to_swedish_full(utc_time)
            broadcast_channels = BroadcastService.get_broadcast_channels(
                self.LEAGUE_ID)

            venue = match.get('venue', {})
            status = match.get('status', {})

            return {
                'id': match.get('id'),
                'league': {
                    'id': self.LEAGUE_ID,
                    'name': 'Premier League',
                    'country': 'England'
                },
                'home_team': {
                    'id': home_team.get('id'),
                    'name': home_team.get('displayName', ''),
                    'short_name': home_team.get('shortName', ''),
                    'logo': home_team.get('logo', '')
                },
                'away_team': {
                    'id': away_team.get('id'),
                    'name': away_team.get('displayName', ''),
                    'short_name': away_team.get('shortName', ''),
                    'logo': away_team.get('logo', '')
                },
                'kickoff': {
                    'utc': utc_time,
                    'swedish_time': swedish_time.get('time', ''),
                    'swedish_date': swedish_time.get('date', ''),
                    'day_of_week': swedish_time.get('day_of_week', ''),
                    'timezone': swedish_time.get('timezone', 'CET')
                },
                'venue': {
                    'name': venue.get('fullName', ''),
                    'city': venue.get('address', {}).get('city', '')
                },
                'status': status.get('detail', 'Scheduled'),
                'broadcast_channels': broadcast_channels
            }
        except Exception as e:
            logger.error(f"Error formatting match: {e}")
            return None
