# pgAdmin Setup Guide

pgAdmin is a web-based PostgreSQL management interface included in this boilerplate.

## Quick Access

**URL**: http://localhost:5050

**Credentials**:
- Email: `admin@example.com`
- Password: `admin`

## Connecting to the Database

### Method 1: Manual Connection (Recommended)

1. Open http://localhost:5050
2. Log in with the credentials above
3. In the left sidebar, right-click on **Servers** → **Create** → **Server**
4. Fill in the connection details:
   - **Name**: MyApp Database (or any name you prefer)
   - **Host name/address**: `app-db`
   - **Port**: `5432`
   - **Maintenance database**: `postgres`
   - **Username**: `postgres`
   - **Password**: `postgres`
5. Click **Save**

### Method 2: Command Line Connection

You can also connect directly using psql from your host:

```bash
# Using psql directly
psql -h localhost -p 5433 -U postgres -d myapp

# Or through Docker
docker exec -it app-db psql -U postgres -d myapp
```

## Database Contents

Once connected, you can browse:

- **Tables**:
  - `users` - User profiles
  - `posts` - Blog posts/content

- **Indexes**:
  - `idx_users_email` - Email lookup optimization
  - `idx_posts_user_id` - User posts filtering

## Features

Once connected in pgAdmin, you can:

- 📊 View database structure and tables
- 📝 Run SQL queries in the Query Tool
- 📈 View table statistics and indexes
- 🔧 Manage database users and permissions
- 💾 Backup and restore databases
- 📋 Create and modify tables

## Troubleshooting

### Connection Refused Error

If you get "connection refused", verify:

1. Database container is running:
   ```bash
   docker ps | grep app-db
   ```

2. Database is healthy:
   ```bash
   docker-compose ps
   ```
   Should show `(healthy)` status

3. Use correct hostname: **`app-db`** (not localhost or 127.0.0.1)

### Port Issues

- pgAdmin: `http://localhost:5050`
- Database: `localhost:5433` (external) or `app-db:5432` (internal)

### Reset pgAdmin

If you need to reset pgAdmin:

```bash
docker-compose down pgadmin
docker volume rm a-py-scraper_pgadmin_data
docker-compose up -d pgadmin
```

## See Also

- [README.md](../README.md) - Main project documentation
- [Database Schema](../database/scripts/init.sql) - SQL initialization script
