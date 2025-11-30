"""
Broadcast service for Swedish TV channel mappings.
Maps football leagues to their Swedish broadcast channels.
"""
from typing import List, Optional


class BroadcastService:
    """Service for mapping matches to broadcast channels (UK/International for IPTV)."""

    # UK/International broadcast mappings for top 5 European leagues
    # League ID -> List of channels (IPTV friendly)
    BROADCAST_MAPPINGS = {
        39: ['Sky Sports', 'TNT Sports', 'NOW TV'],  # Premier League
        140: ['Premier Sports', 'LaLigaTV'],          # La Liga
        78: ['Sky Sports', 'TNT Sports'],             # Bundesliga
        135: ['TNT Sports', 'BT Sport'],              # Serie A
        61: ['TNT Sports', 'beIN Sports'],            # Ligue 1
    }

    # Fallback message when no broadcast info available
    UNAVAILABLE_MESSAGE = "Broadcast info unavailable"

    @classmethod
    def get_broadcast_channels(
        cls,
        league_id: int,
        match_id: Optional[int] = None
    ) -> List[str]:
        """
        Get broadcast channels for a match.

        Args:
            league_id: League identifier
            match_id: Optional specific match ID for detailed lookup

        Returns:
            List of channel names or ["Broadcast info unavailable"]
        """
        channels = cls.BROADCAST_MAPPINGS.get(league_id)

        if channels:
            return channels.copy()

        return [cls.UNAVAILABLE_MESSAGE]

    @classmethod
    def get_all_channels(cls) -> List[str]:
        """
        Get all unique Swedish broadcast channels.

        Returns:
            List of all unique channel names
        """
        all_channels = set()
        for channels in cls.BROADCAST_MAPPINGS.values():
            all_channels.update(channels)
        return sorted(list(all_channels))

    @classmethod
    def get_leagues_by_channel(cls, channel_name: str) -> List[int]:
        """
        Get league IDs that broadcast on a specific channel.

        Args:
            channel_name: Name of the broadcast channel

        Returns:
            List of league IDs
        """
        leagues = []
        for league_id, channels in cls.BROADCAST_MAPPINGS.items():
            if channel_name in channels:
                leagues.append(league_id)
        return leagues

    @classmethod
    def is_broadcast_available(cls, league_id: int) -> bool:
        """
        Check if broadcast info is available for a league.

        Args:
            league_id: League identifier

        Returns:
            True if broadcast info exists
        """
        return league_id in cls.BROADCAST_MAPPINGS
