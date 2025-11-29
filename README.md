# What2Watch

A personalized content discovery platform that aggregates streaming services, sports schedules, and TV programming to solve the "what to watch" problem.

## Vision

Help users discover what to watch across multiple platforms with personalized recommendations based on their profile (Sports fan, Hacker, Family, Kids, etc.).

## Tech Stack

### Frontend
- **Framework**: Next.js 14+ (React)
- **Styling**: TailwindCSS
- **State Management**: React Context / Zustand
- **UI Components**: shadcn/ui

### Backend
- **Framework**: Django 5.0+ with Django REST Framework
- **Database**: PostgreSQL 15+
- **API Integration**: RapidAPI for content sources
- **Authentication**: Django JWT

### Future Plans
- Android app (Kotlin)
- iOS app (Swift)
- Push notifications
- Real-time updates

## Project Structure

```
what2watch/
├── backend/          # Django + DRF API
├── frontend/         # Next.js React app
├── docs/             # Documentation
├── docker-compose.yml
└── README.md
```

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Docker (optional)

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Docker Setup
```bash
docker-compose up -d
```

## Features (Roadmap)

- [ ] User profiles and preferences
- [ ] Multi-platform streaming content aggregation
- [ ] Sports schedules and live match notifications
- [ ] TV channel programming
- [ ] Personalized recommendations
- [ ] Custom popup widgets
- [ ] Push notifications
- [ ] Mobile apps (Android & iOS)

## Contributing

This project is in early development. Stay tuned!

## License

TBD
