# PostgreSQL Database Configuration
This directory contains the PostgreSQL database setup.

## Files
- `Dockerfile`: PostgreSQL image with initialization scripts
- `docker-compose.yml`: Standalone database service
- `scripts/init.sql`: Database initialization SQL

## Running
```bash
docker-compose up -d
```

## Database Connection
- Host: localhost
- Port: 5432
- Username: postgres
- Password: postgres
- Database: myapp
