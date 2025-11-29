"""
Models for content management (movies, TV shows, sports, etc.).
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class StreamingPlatform(models.Model):
    """Streaming platforms (Netflix, Disney+, etc.)."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    logo = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('streaming platform')
        verbose_name_plural = _('streaming platforms')
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Content genres."""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = _('genre')
        verbose_name_plural = _('genres')
        ordering = ['name']

    def __str__(self):
        return self.name


class Movie(models.Model):
    """Movie content."""
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    release_date = models.DateField(null=True, blank=True)
    duration_minutes = models.IntegerField(null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    poster_url = models.URLField(blank=True)
    backdrop_url = models.URLField(blank=True)
    trailer_url = models.URLField(blank=True)

    # External IDs
    imdb_id = models.CharField(max_length=20, blank=True, unique=True, null=True)
    tmdb_id = models.IntegerField(blank=True, null=True)

    genres = models.ManyToManyField(Genre, related_name='movies', blank=True)
    platforms = models.ManyToManyField(StreamingPlatform, related_name='movies', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('movie')
        verbose_name_plural = _('movies')
        ordering = ['-release_date']

    def __str__(self):
        return self.title


class TVShow(models.Model):
    """TV Show/Series content."""
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    first_air_date = models.DateField(null=True, blank=True)
    last_air_date = models.DateField(null=True, blank=True)
    number_of_seasons = models.IntegerField(default=1)
    number_of_episodes = models.IntegerField(null=True, blank=True)
    episode_duration = models.IntegerField(null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    poster_url = models.URLField(blank=True)
    backdrop_url = models.URLField(blank=True)
    trailer_url = models.URLField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('RETURNING', 'Returning Series'),
            ('ENDED', 'Ended'),
            ('CANCELED', 'Canceled'),
            ('IN_PRODUCTION', 'In Production'),
        ],
        default='RETURNING'
    )

    # External IDs
    imdb_id = models.CharField(max_length=20, blank=True, unique=True, null=True)
    tmdb_id = models.IntegerField(blank=True, null=True)

    genres = models.ManyToManyField(Genre, related_name='tv_shows', blank=True)
    platforms = models.ManyToManyField(StreamingPlatform, related_name='tv_shows', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('TV show')
        verbose_name_plural = _('TV shows')
        ordering = ['-first_air_date']

    def __str__(self):
        return self.title


class SportsEvent(models.Model):
    """Sports events and matches."""
    SPORT_TYPES = [
        ('FOOTBALL', 'Football/Soccer'),
        ('BASKETBALL', 'Basketball'),
        ('AMERICAN_FOOTBALL', 'American Football'),
        ('BASEBALL', 'Baseball'),
        ('HOCKEY', 'Hockey'),
        ('TENNIS', 'Tennis'),
        ('CRICKET', 'Cricket'),
        ('RUGBY', 'Rugby'),
        ('OTHER', 'Other'),
    ]

    title = models.CharField(max_length=255)
    sport_type = models.CharField(max_length=50, choices=SPORT_TYPES)
    league = models.CharField(max_length=100)
    home_team = models.CharField(max_length=100)
    away_team = models.CharField(max_length=100)
    event_date = models.DateTimeField()
    venue = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)

    # Broadcasting
    tv_channel = models.CharField(max_length=100, blank=True)
    streaming_platforms = models.ManyToManyField(
        StreamingPlatform,
        related_name='sports_events',
        blank=True
    )

    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('SCHEDULED', 'Scheduled'),
            ('LIVE', 'Live'),
            ('FINISHED', 'Finished'),
            ('POSTPONED', 'Postponed'),
            ('CANCELED', 'Canceled'),
        ],
        default='SCHEDULED'
    )

    # External API data
    external_id = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('sports event')
        verbose_name_plural = _('sports events')
        ordering = ['event_date']

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} - {self.event_date}"


class TVChannel(models.Model):
    """TV Channels."""
    name = models.CharField(max_length=100)
    channel_number = models.CharField(max_length=10, blank=True)
    logo_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    country = models.CharField(max_length=2)  # ISO country code
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('TV channel')
        verbose_name_plural = _('TV channels')
        ordering = ['name']

    def __str__(self):
        return self.name


class TVProgram(models.Model):
    """TV Program schedule."""
    channel = models.ForeignKey(
        TVChannel,
        on_delete=models.CASCADE,
        related_name='programs'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    category = models.CharField(max_length=50, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('TV program')
        verbose_name_plural = _('TV programs')
        ordering = ['start_time']

    def __str__(self):
        return f"{self.title} on {self.channel.name}"
