# What2Watch API Documentation

## Overview
Backend API for the What2Watch application providing recommendations for streaming content, sports events, and movies.

**Server:** http://127.0.0.1:8000/
**Base URL:** `/api/content/`

---

## Authentication
Most endpoints use `AllowAny` permission for development. JWT authentication is configured for protected endpoints.

---

## API Endpoints

### 1. Streaming Availability API ✅ WORKING

#### Test Connection
```bash
GET /api/content/api/test/
```
**Response:**
```json
{
  "status": "success",
  "message": "Successfully connected to Streaming Availability API!",
  "countries_count": 67,
  "sample_countries": {...}
}
```

#### Get Streaming Services
```bash
GET /api/content/api/services/?country=us
```
**Query Params:**
- `country` (optional): Country code (default: 'us')

#### Search Shows
```bash
GET /api/content/api/search/?title=breaking+bad&country=us&show_type=series
```
**Query Params:**
- `title` (required): Show title to search
- `country` (optional): Country code (default: 'us')
- `show_type` (optional): 'movie' or 'series'

#### Get Show Details
```bash
GET /api/content/api/show/series/tt0903747/?country=us
```
**URL Params:**
- `show_type`: 'movie' or 'series'
- `show_id`: IMDB ID (e.g., 'tt0903747')

**Query Params:**
- `country` (optional): Country code (default: 'us')

#### Get New Shows
```bash
GET /api/content/api/new/?country=us
```
**Query Params:**
- `country` (optional): Country code (default: 'us')

---

### 2. API-Football ✅ WORKING

#### Test Connection
```bash
GET /api/content/api/football/test/
```
**Response:**
```json
{
  "status": "success",
  "message": "Successfully connected to Football API!",
  "data": {...}
}
```

#### Get Premier League Matches
```bash
GET /api/content/api/football/premier-league/?season=2024
GET /api/content/api/football/premier-league/?date=2024-12-25
GET /api/content/api/football/premier-league/?next=5
```
**Query Params (choose one):**
- `season`: Year (e.g., 2024)
- `date`: Date in YYYY-MM-DD format
- `next`: Number of upcoming matches
- None: Returns today's matches

#### Get Live Matches
```bash
GET /api/content/api/football/live/?league_id=39
```
**Query Params:**
- `league_id` (optional): League ID (39 = Premier League)

#### Get Today's Matches
```bash
GET /api/content/api/football/today/?league_id=39
```
**Query Params:**
- `league_id` (optional): League ID (39 = Premier League)

#### Search Football Team
```bash
GET /api/content/api/football/search-team/?name=manchester
```
**Query Params:**
- `name` (required): Team name to search

---

### 3. AI Movie Recommender API ⚠️ INTEGRATION COMPLETE (API SERVICE ISSUE)

**Status:** Code is fully implemented and working. Currently experiencing intermittent 502 errors from RapidAPI's AI Movie Recommender service.

#### Test Connection
```bash
GET /api/content/api/movies/test/
```

#### Search Movies (AI-Powered)
```bash
GET /api/content/api/movies/search/?q=10s+sad+movies
GET /api/content/api/movies/search/?q=action+thriller
```
**Query Params:**
- `q` (required): Natural language search query

**Example Response:**
```json
{
  "success": true,
  "query": "10s sad movies",
  "movies": [
    {
      "id": 334541,
      "title": "Manchester by the Sea",
      "release_date": "2016-11-17",
      "overview": "After his older brother passes away...",
      "genre_ids": [18],
      "vote_average": 7.547,
      "vote_count": 6195,
      "poster_path": "/o9VXYOuaJxCEKOxbA86xqtwmqYn.jpg"
    }
  ],
  "total": 5
}
```

#### Get Recommendations by Mood
```bash
GET /api/content/api/movies/mood/?mood=happy&decade=90s
GET /api/content/api/movies/mood/?mood=scary
```
**Query Params:**
- `mood` (required): 'sad', 'happy', 'scary', 'romantic', etc.
- `decade` (optional): '10s', '90s', '80s', etc.

#### Get Recommendations by Genre
```bash
GET /api/content/api/movies/genre/?genre=action&year=2020
GET /api/content/api/movies/genre/?genre=comedy
```
**Query Params:**
- `genre` (required): 'action', 'comedy', 'thriller', etc.
- `year` (optional): Specific year

#### Get Family Recommendations
```bash
GET /api/content/api/movies/family/
```

#### Get Kids Recommendations
```bash
GET /api/content/api/movies/kids/
```

#### Get Movie IDs (TMDB/IMDb)
```bash
GET /api/content/api/movies/id/?title=Inception
```
**Query Params:**
- `title` (required): Movie title

**Response:**
```json
{
  "title": "Inception",
  "tmdb": "27205",
  "imdb": "tt1375666"
}
```

---

## Caching Strategy

- **Streaming Availability:** 1 hour cache
- **Football Matches:** 30 minutes cache
- **Movie Recommendations:** 6 hours cache
- **Movie IDs:** 24 hours cache (IDs don't change)

---

## Error Handling

All endpoints return consistent error responses:

```json
{
  "error": "Error message description"
}
```

**HTTP Status Codes:**
- `200` - Success
- `400` - Bad Request (missing required parameters)
- `404` - Not Found
- `503` - Service Unavailable (external API down)

---

## Environment Variables

All API keys are stored in `.env` file:

```env
# RapidAPI - Single key for multiple services
RAPIDAPI_KEY=your_rapidapi_key_here

# API-Football
API_FOOTBALL_KEY=your_api_football_key_here
```

---

## Known Issues

### AI Movie Recommender API
- **Issue:** Intermittent 502 Bad Gateway errors from RapidAPI service
- **Status:** Under investigation
- **Workaround:** The API works when tested directly on RapidAPI dashboard but fails from Django application
- **Suspected Cause:** Rate limiting or IP-based restrictions
- **Impact:** Endpoints are implemented and will work once service stabilizes

---

## Testing Examples

### Test All Working APIs
```bash
# Streaming Availability
curl "http://127.0.0.1:8000/api/content/api/test/"

# Football API
curl "http://127.0.0.1:8000/api/content/api/football/test/"

# Search Premier League
curl "http://127.0.0.1:8000/api/content/api/football/premier-league/?season=2024"
```

---

## Next Steps

1. **Frontend Integration:** Build Next.js UI components for working APIs
2. **Movie API:** Monitor RapidAPI Movie Recommender service status
3. **Alternative APIs:** Consider TMDB API as backup for movie recommendations
4. **Testing:** Comprehensive endpoint testing
5. **Documentation:** OpenAPI/Swagger documentation
6. **Deployment:** Production deployment with PostgreSQL

---

## Tech Stack

- **Framework:** Django 4.2 LTS + Django REST Framework
- **Authentication:** JWT (djangorestframework-simplejwt)
- **Caching:** Django Cache Framework
- **External APIs:**
  - Streaming Availability API (RapidAPI)
  - API-Football (api-football.com)
  - AI Movie Recommender (RapidAPI)

---

**Last Updated:** 2025-11-29
**API Version:** 1.0
**Django Version:** 4.2.11
**DRF Version:** 3.14.0
