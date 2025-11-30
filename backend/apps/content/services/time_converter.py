"""
Time conversion utility for Swedish local time.
Handles UTC to CET/CEST conversion with DST awareness.
"""
import pytz
from datetime import datetime
from typing import Dict, Optional


class TimeConverter:
    """Utility for converting UTC times to Swedish local time."""

    SWEDEN_TZ = pytz.timezone('Europe/Stockholm')
    UTC_TZ = pytz.UTC

    @staticmethod
    def utc_to_swedish(utc_timestamp: str) -> str:
        """
        Convert UTC timestamp to Swedish local time.

        Args:
            utc_timestamp: ISO format UTC timestamp (e.g., "2024-12-01T15:00:00Z")

        Returns:
            Formatted time string in Swedish local time (HH:MM)
        """
        utc_dt = TimeConverter._parse_utc_timestamp(utc_timestamp)
        if utc_dt is None:
            return "00:00"

        swedish_dt = utc_dt.astimezone(TimeConverter.SWEDEN_TZ)
        return swedish_dt.strftime('%H:%M')

    @staticmethod
    def utc_to_swedish_full(utc_timestamp: str) -> Dict:
        """
        Convert UTC timestamp with full date info.

        Args:
            utc_timestamp: ISO format UTC timestamp

        Returns:
            Dict with date, time, day_of_week, timezone_name
        """
        utc_dt = TimeConverter._parse_utc_timestamp(utc_timestamp)
        if utc_dt is None:
            return {
                'date': None,
                'time': '00:00',
                'day_of_week': None,
                'timezone': 'CET'
            }

        swedish_dt = utc_dt.astimezone(TimeConverter.SWEDEN_TZ)

        # Determine if DST is active
        is_dst = TimeConverter.is_dst_active(swedish_dt)
        timezone_name = 'CEST' if is_dst else 'CET'

        return {
            'date': swedish_dt.strftime('%Y-%m-%d'),
            'time': swedish_dt.strftime('%H:%M'),
            'day_of_week': swedish_dt.strftime('%A'),
            'timezone': timezone_name
        }

    @staticmethod
    def is_dst_active(dt: datetime) -> bool:
        """
        Check if daylight saving time is active in Sweden for given datetime.

        Args:
            dt: datetime object (should be timezone-aware)

        Returns:
            True if DST (CEST) is active, False if standard time (CET)
        """
        if dt.tzinfo is None:
            # Make it timezone-aware in Swedish time
            dt = TimeConverter.SWEDEN_TZ.localize(dt)
        else:
            dt = dt.astimezone(TimeConverter.SWEDEN_TZ)

        # Check DST offset - CEST has +2 hours, CET has +1 hour
        return bool(dt.dst())

    @staticmethod
    def _parse_utc_timestamp(utc_timestamp: str) -> Optional[datetime]:
        """
        Parse various UTC timestamp formats.

        Args:
            utc_timestamp: UTC timestamp string

        Returns:
            Timezone-aware datetime in UTC or None if parsing fails
        """
        if not utc_timestamp:
            return None

        formats = [
            '%Y-%m-%dT%H:%M:%SZ',      # ISO format with Z
            '%Y-%m-%dT%H:%M:%S+00:00',  # ISO format with +00:00
            '%Y-%m-%dT%H:%M:%S',       # ISO format without timezone
            '%Y-%m-%d %H:%M:%S',       # Space-separated
        ]

        for fmt in formats:
            try:
                dt = datetime.strptime(utc_timestamp, fmt)
                return TimeConverter.UTC_TZ.localize(dt)
            except ValueError:
                continue

        # Try parsing with fromisoformat for more complex formats
        try:
            dt = datetime.fromisoformat(utc_timestamp.replace('Z', '+00:00'))
            if dt.tzinfo is None:
                dt = TimeConverter.UTC_TZ.localize(dt)
            return dt.astimezone(TimeConverter.UTC_TZ)
        except (ValueError, AttributeError):
            return None

    @staticmethod
    def get_swedish_offset_hours(utc_timestamp: str) -> int:
        """
        Get the UTC offset in hours for Swedish time at given timestamp.

        Args:
            utc_timestamp: UTC timestamp string

        Returns:
            1 for CET (winter), 2 for CEST (summer)
        """
        utc_dt = TimeConverter._parse_utc_timestamp(utc_timestamp)
        if utc_dt is None:
            return 1  # Default to CET

        swedish_dt = utc_dt.astimezone(TimeConverter.SWEDEN_TZ)
        return 2 if TimeConverter.is_dst_active(swedish_dt) else 1
