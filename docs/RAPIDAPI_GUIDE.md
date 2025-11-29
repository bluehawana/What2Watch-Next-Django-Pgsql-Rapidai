# RapidAPI Integration Guide

## Overview

RapidAPI will be our primary source for real-time content data including:
- Streaming platform availability
- Movie and TV show metadata
- Sports schedules and live scores
- TV programming schedules

## Recommended APIs

### 1. Streaming Content

#### Streaming Availability API
- **Purpose**: Find which streaming service has specific movies/shows
- **URL**: https://rapidapi.com/movie-of-the-night-movie-of-the-night-default/api/streaming-availability
- **Features**:
  - Check availability across 150+ streaming services
  - Search by title, genre, type
  - Get new releases
  - Country-specific availability
- **Pricing**: Free tier available
- **Use Case**: Core feature for "where to watch" functionality

#### TMDB (The Movie Database) API
- **Purpose**: Comprehensive movie and TV show metadata
- **URL**: https://rapidapi.com/apidojo/api/imdb8 or direct TMDB API
- **Features**:
  - Movie details, cast, crew
  - TV show episodes and seasons
  - Images, posters, backdrops
  - Reviews and ratings
  - Trending content
- **Pricing**: Free tier available
- **Use Case**: Rich content information and images

### 2. Sports Content

#### API-Football (Soccer)
- **Purpose**: Live football/soccer data
- **URL**: https://rapidapi.com/api-sports/api/api-football
- **Features**:
  - Live scores and fixtures
  - Team and player statistics
  - League standings
  - Match events
- **Pricing**: Free tier: 100 requests/day
- **Use Case**: Soccer match schedules and notifications

#### API-NBA
- **Purpose**: Basketball game data
- **URL**: https://rapidapi.com/api-sports/api/api-nba
- **Features**:
  - NBA games and schedules
  - Team stats
  - Player information
  - Live scores
- **Pricing**: Free tier available
- **Use Case**: Basketball match information

#### Live Sports Odds API
- **Purpose**: Multi-sport coverage
- **URL**: https://rapidapi.com/theoddsapi/api/live-sports-odds
- **Features**:
  - Multiple sports coverage
  - Upcoming games
  - Live scores
- **Pricing**: Free tier available
- **Use Case**: Broad sports coverage

### 3. TV Programming

#### TV Guide API
- **Purpose**: TV channel programming schedules
- **URL**: Search RapidAPI for "TV Guide" or "EPG" (Electronic Program Guide)
- **Features**:
  - Channel schedules
  - Program information
  - What's on TV now
- **Use Case**: Traditional TV programming display

## Implementation Strategy

### Phase 1: Core Streaming Content

1. **Set up API integration layer**
   ```python
   # backend/apps/content/services/rapidapi_client.py
   import requests
   from django.conf import settings

   class RapidAPIClient:
       def __init__(self):
           self.headers = {
               'X-RapidAPI-Key': settings.RAPIDAPI_KEY,
               'X-RapidAPI-Host': 'streaming-availability.p.rapidapi.com'
           }
           self.base_url = 'https://streaming-availability.p.rapidapi.com'

       def search_movies(self, query):
           # Implementation
           pass

       def get_streaming_availability(self, imdb_id):
           # Implementation
           pass
   ```

2. **Create Celery tasks for data fetching**
   ```python
   # backend/apps/content/tasks.py
   from celery import shared_task
   from .services.rapidapi_client import RapidAPIClient

   @shared_task
   def fetch_new_movies():
       client = RapidAPIClient()
       # Fetch and store new movies
       pass

   @shared_task
   def update_streaming_availability():
       # Update which platforms have which content
       pass
   ```

3. **Schedule periodic updates**
   ```python
   # backend/what2watch/celery.py
   from celery.schedules import crontab

   app.conf.beat_schedule = {
       'fetch-new-movies-daily': {
           'task': 'apps.content.tasks.fetch_new_movies',
           'schedule': crontab(hour=2, minute=0),  # 2 AM daily
       },
   }
   ```

### Phase 2: Sports Integration

1. **Football/Soccer data fetching**
   ```python
   # backend/apps/content/services/sports_api.py
   class SportsAPIClient:
       def get_upcoming_matches(self, sport_type, league):
           # Fetch upcoming matches
           pass

       def get_live_scores(self):
           # Get live match scores
           pass
   ```

2. **Create notification triggers**
   - Detect when user's favorite team has a match
   - Send notifications 1 hour before kickoff
   - Update match status in real-time

### Phase 3: TV Programming

1. **EPG data integration**
2. **Channel lineup based on user's location**
3. **"What's on now" feature**

## API Key Management

### Setup

1. **Sign up for RapidAPI**: https://rapidapi.com/auth/sign-up
2. **Subscribe to APIs** (start with free tiers)
3. **Get your API key** from RapidAPI dashboard
4. **Add to .env file**:
   ```
   RAPIDAPI_KEY=your_api_key_here
   ```

### Security Best Practices

- Never commit API keys to git
- Use environment variables
- Rotate keys periodically
- Monitor usage to avoid unexpected charges
- Set up rate limiting in your app

## Rate Limiting Strategy

### Implementation

```python
# backend/apps/content/services/rate_limiter.py
from django.core.cache import cache
import time

class RateLimiter:
    def __init__(self, max_calls, time_window):
        self.max_calls = max_calls
        self.time_window = time_window

    def check_rate_limit(self, key):
        current_calls = cache.get(key, 0)
        if current_calls >= self.max_calls:
            return False
        cache.set(key, current_calls + 1, self.time_window)
        return True
```

### Cache Responses

```python
from django.core.cache import cache

def get_movie_details(imdb_id):
    cache_key = f'movie_{imdb_id}'
    cached_data = cache.get(cache_key)

    if cached_data:
        return cached_data

    # Fetch from API
    data = api_client.get_movie(imdb_id)

    # Cache for 24 hours
    cache.set(cache_key, data, 60 * 60 * 24)
    return data
```

## Data Models Integration

### Mapping API responses to Django models

```python
# backend/apps/content/services/data_mapper.py
from apps.content.models import Movie, StreamingPlatform

class ContentMapper:
    @staticmethod
    def map_movie(api_response):
        movie, created = Movie.objects.update_or_create(
            imdb_id=api_response['imdb_id'],
            defaults={
                'title': api_response['title'],
                'description': api_response['overview'],
                'release_date': api_response['release_date'],
                'rating': api_response['vote_average'],
                'poster_url': api_response['poster_path'],
                # ... more fields
            }
        )

        # Add streaming platforms
        for platform_data in api_response.get('streaming_info', []):
            platform = StreamingPlatform.objects.get(
                slug=platform_data['service']
            )
            movie.platforms.add(platform)

        return movie
```

## Testing API Integration

### Unit Tests

```python
# backend/apps/content/tests/test_rapidapi.py
from django.test import TestCase
from unittest.mock import Mock, patch
from apps.content.services.rapidapi_client import RapidAPIClient

class RapidAPIClientTest(TestCase):
    @patch('requests.get')
    def test_search_movies(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {'results': []}
        mock_get.return_value = mock_response

        client = RapidAPIClient()
        result = client.search_movies('Inception')

        self.assertIsNotNone(result)
```

## Monitoring and Logging

```python
import logging

logger = logging.getLogger(__name__)

def fetch_data_with_logging():
    try:
        logger.info('Fetching data from RapidAPI')
        response = api_client.get_movies()
        logger.info(f'Successfully fetched {len(response)} movies')
        return response
    except Exception as e:
        logger.error(f'Error fetching data: {str(e)}')
        raise
```

## Cost Optimization

1. **Use free tiers first** - Most APIs offer free tiers
2. **Implement caching** - Cache responses for 24 hours
3. **Batch requests** - Fetch multiple items in single requests
4. **Monitor usage** - Track API calls to stay within limits
5. **Fallback strategies** - Use cached/stale data if API is unavailable

## Next Steps

1. Sign up for RapidAPI
2. Subscribe to Streaming Availability API (free tier)
3. Subscribe to API-Football (free tier)
4. Test API endpoints in Postman or similar tool
5. Implement RapidAPIClient service
6. Create data mapping functions
7. Set up Celery for background tasks
8. Implement caching layer
9. Add error handling and retry logic
10. Monitor and optimize

## Resources

- RapidAPI Documentation: https://docs.rapidapi.com/
- RapidAPI Hub: https://rapidapi.com/hub
- Celery Documentation: https://docs.celeryproject.org/
- Django Cache Framework: https://docs.djangoproject.com/en/stable/topics/cache/
