# Backend API

Python Flask-based REST API backend.

## Features
- Flask web framework
- PostgreSQL database integration
- CORS enabled
- RESTful API endpoints
- Docker containerization

## Quick Start

### Local Development
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env

# Run application
python main.py
```

### Docker
```bash
docker-compose up --build
```

## API Endpoints

- `GET /api/health` - Health check endpoint
- `GET /api/info` - API information

## Configuration

Environment variables in `.env`:
- `FLASK_ENV` - Development or production
- `PORT` - Server port (default: 5000)
- `DATABASE_URL` - PostgreSQL connection string

## Dependencies

See `requirements.txt` for all dependencies:
- Flask 2.3.2
- Flask-CORS 4.0.0
- psycopg2-binary 2.9.6
- SQLAlchemy 2.0.19
- python-dotenv 1.0.0
- gunicorn 21.2.0
