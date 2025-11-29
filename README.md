# A-py-scraper - Full Stack Application Boilerplate

A complete boilerplate for a modern web application with Python backend, PostgreSQL database, and Angular frontend.

## Quick Access

Once services are running:

- **Frontend**: http://localhost:4201
- **Backend API**: http://localhost:5001/api/
- **pgAdmin (Database UI)**: http://localhost:5050
  - Email: `admin@example.com`
  - Password: `admin`
- **Database Direct**: `localhost:5433` (postgres:postgres)

```
.
├── backend/                 # Python Flask API
│   ├── app/
│   │   ├── __init__.py     # Flask app factory
│   │   └── routes.py       # API routes
│   ├── main.py             # Entry point
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile          # Backend container
│   ├── docker-compose.yml  # Backend standalone compose
│   ├── README.md
│   └── .env.example        # Environment variables template
│
├── database/               # PostgreSQL Database
│   ├── scripts/
│   │   └── init.sql       # Database initialization
│   ├── Dockerfile         # Database container
│   ├── docker-compose.yml # Database standalone compose
│   ├── .gitignore
│   └── README.md
│
├── frontend/              # Angular Frontend
│   ├── src/
│   │   ├── app/           # Angular components and modules
│   │   ├── index.html     # Main HTML
│   │   ├── main.ts        # Bootstrap
│   │   └── styles.css     # Global styles
│   ├── package.json       # Node dependencies
│   ├── tsconfig.json      # TypeScript config
│   ├── angular.json       # Angular config
│   ├── Dockerfile         # Frontend container
│   ├── docker-compose.yml # Frontend standalone compose
│   ├── .dockerignore
│   ├── .gitignore
│   └── README.md
│
├── docker-compose.yml     # Orchestration (all services)
└── README.md             # This file
```

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Run All Services

```bash
# Navigate to project
cd A-py-scraper

# Start all services
docker-compose up -d

# Services will be available at:
# Frontend: http://localhost:4201
# Backend API: http://localhost:5001
# pgAdmin: http://localhost:5050
# Database: localhost:5433
```

### Run Individual Services

Each service has its own docker-compose file:

```bash
# Backend only
cd backend
docker-compose up --build

# Database only
cd database
docker-compose up --build

# Frontend only
cd frontend
docker-compose up --build
```

## Service Details

### Backend (Python Flask)
- **Port**: 5001
- **Framework**: Flask 2.3.2
- **Database Driver**: psycopg2-binary
- **Key Files**:
  - `main.py`: Entry point
  - `app/__init__.py`: Flask app factory
  - `app/routes.py`: API endpoints
  - `requirements.txt`: Dependencies

**Endpoints**:
- `GET /api/health` - Health check
- `GET /api/info` - API information

### Database (PostgreSQL)
- **Port**: 5433 (5432 internal)
- **Version**: PostgreSQL 15 Alpine
- **Default Credentials**:
  - User: postgres
  - Password: postgres
  - Database: myapp
- **Management UI**: pgAdmin at http://localhost:5050

### pgAdmin Dashboard
- **Port**: 5050
- **Email**: admin@example.com
- **Password**: admin
- **Features**: 
  - View database structure
  - Browse tables (users, posts)
  - Run SQL queries
  - Manage connections

### Frontend (Angular)
- **Port**: 4201
- **Version**: Angular 20
- **Key Files**:
  - `src/main.ts`: Bootstrap
  - `src/app/app.component.ts`: Root component
  - `src/index.html`: HTML template

## Environment Variables

### Backend
Create `backend/.env`:
```
FLASK_ENV=development
PORT=5000
DATABASE_URL=postgresql://postgres:postgres@db:5432/myapp
```

## API Examples

```bash
# Health check
curl http://localhost:5001/api/health

# API info
curl http://localhost:5001/api/info
```

## Database Management

### Using pgAdmin (Recommended)
1. Open http://localhost:5050
2. Login with: admin@example.com / admin
3. Add server connection:
   - Host: app-db
   - Port: 5432
   - Username: postgres
   - Password: postgres
   - Database: myapp
4. Browse tables and run queries

### Direct Connection
```bash
# Connect using psql
psql -h localhost -p 5433 -U postgres -d myapp

# Or via Docker
docker exec -it app-db psql -U postgres -d myapp

# View tables
\dt

# View table structure
\d users
```

## Development

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Frontend Development
```bash
cd frontend
npm install
npm start
```

### Database Development
```bash
cd database
docker build -t myapp-db .
docker run -p 5432:5432 -e POSTGRES_PASSWORD=postgres myapp-db
```

## Testing

```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd frontend
npm test
```

## Production Deployment

For production, update:
1. Environment variables in each service
2. Use environment-specific docker-compose files
3. Configure CORS properly in backend
4. Build optimized frontend: `ng build --configuration production`
5. Use production-grade server (gunicorn for Flask is already configured)

## Troubleshooting

**Backend can't connect to database?**
- Ensure database service is running: `docker ps`
- Check DATABASE_URL in backend/.env
- Verify network: `docker network ls`

**Frontend can't reach backend?**
- Check CORS settings in `backend/app/__init__.py`
- Verify backend is running on port 5000
- Check browser console for errors

**Database initialization not running?**
- Check `database/scripts/init.sql` permissions
- Verify init.sql is in docker-entrypoint-initdb.d/
- Check Docker logs: `docker logs app-db`

## Contributing

1. Create feature branch
2. Make changes
3. Test locally
4. Submit pull request

## License

MIT

## Support

For issues or questions, please open an issue in the repository.
