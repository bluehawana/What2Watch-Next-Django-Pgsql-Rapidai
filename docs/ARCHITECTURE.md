# What2Watch Architecture

## Overview

What2Watch is a full-stack application designed to help users discover content across multiple platforms with personalized recommendations.

## Technology Stack

### Backend
- **Framework**: Django 5.0+ with Django REST Framework
- **Database**: PostgreSQL 15+
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Task Queue**: Celery with Redis
- **API Integration**: RapidAPI for external content sources

### Frontend
- **Framework**: Next.js 14+ (React 18)
- **Styling**: TailwindCSS
- **State Management**: Zustand
- **Data Fetching**: TanStack Query (React Query)
- **HTTP Client**: Axios

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Database**: PostgreSQL (containerized)
- **Caching**: Redis

## Application Structure

### Backend (`/backend`)

```
backend/
├── what2watch/           # Django project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── users/            # User management & authentication
│   ├── content/          # Movies, TV shows, sports events
│   ├── preferences/      # User preferences & watchlist
│   └── recommendations/  # Recommendation engine
├── requirements.txt
└── manage.py
```

### Frontend (`/frontend`)

```
frontend/
├── app/                  # Next.js 14 App Router
│   ├── layout.tsx
│   ├── page.tsx
│   └── globals.css
├── components/           # React components
├── lib/                  # Utility functions
└── public/               # Static assets
```

## Database Schema

### Core Models

#### Users App
- `User`: Extended Django user model
- `ProfileType`: User profile categories (Hacker, Sports Fan, etc.)
- `UserProfile`: User preferences and streaming subscriptions

#### Content App
- `StreamingPlatform`: Streaming services (Netflix, Disney+, etc.)
- `Genre`: Content genres
- `Movie`: Movie content
- `TVShow`: TV series content
- `SportsEvent`: Sports matches and events
- `TVChannel`: TV channels
- `TVProgram`: TV program schedules

#### Preferences App
- `WatchlistItem`: User's watchlist
- `FavoriteGenre`: User's favorite genres
- `SportsPreference`: Sports preferences

## API Endpoints

### Authentication
- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token

### Users
- `POST /api/users/register/` - User registration
- `GET /api/users/me/` - Get current user
- `GET /api/users/profile/` - Get/Update user profile
- `GET /api/users/profile-types/` - List profile types

### Content
- `GET /api/content/movies/` - List movies
- `GET /api/content/tv-shows/` - List TV shows
- `GET /api/content/sports/` - List sports events
- `GET /api/content/platforms/` - List streaming platforms

### Preferences
- `GET /api/preferences/watchlist/` - User's watchlist
- `GET /api/preferences/favorite-genres/` - Favorite genres
- `GET /api/preferences/sports/` - Sports preferences

### Recommendations
- `GET /api/recommendations/` - Get personalized recommendations
- `GET /api/recommendations/daily/` - Daily picks

## Future Enhancements

1. **Mobile Apps**
   - Android (Kotlin)
   - iOS (Swift)

2. **Features**
   - Push notifications
   - Real-time updates
   - Advanced recommendation algorithms
   - Social features (share recommendations)
   - Integration with more streaming platforms

3. **Infrastructure**
   - CI/CD pipeline
   - Production deployment
   - Monitoring and logging
   - Performance optimization
