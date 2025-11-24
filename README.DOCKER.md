# Docker Setup - Gas Emissions API

This guide explains how to run the complete application (backend and frontend) using Docker and Docker Compose.

## Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 2.0 or higher)

## Docker Structure

The project includes:

- **Backend**: Django API in Python 3.13
- **Frontend**: Angular 21 with Nginx
- **Docker Compose**: Orchestrates both services

## Quick Start

### 1. Build and run all services

**Using Makefile (recommended):**
```bash
make up-build
```

**Or using Docker Compose directly:**
```bash
docker-compose up --build
```

This command:
- Builds Docker images for backend and frontend
- Starts both containers
- Configures the network between services
- Automatically runs Django migrations

### 2. Access the application

- **Frontend**: http://localhost:4200
- **Backend API**: http://localhost:8000
- **API Endpoints**: http://localhost:8000/api/emissions/

### 3. Stop services

**Using Makefile:**
```bash
make down
```

**Or using Docker Compose:**
```bash
docker-compose down
```

To also remove volumes:
```bash
docker-compose down -v
```

## Useful Commands

### Build and Run

**Using Makefile:**
```bash
# Build images only
make build

# Start services in detached mode
make up

# Build and start services
make up-build

# Rebuild and restart all services
make rebuild

# Rebuild and restart only frontend
make rebuild-frontend

# Rebuild and restart only backend
make rebuild-backend
```

**Or using Docker Compose directly:**
```bash
docker-compose build
docker-compose up -d
docker-compose up --build
```

### View Logs

```bash
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only
docker-compose logs -f frontend
```

### Execute Commands in Containers

```bash
# Backend - Run migrations manually
docker-compose exec backend python manage.py migrate

# Backend - Create superuser
docker-compose exec backend python manage.py createsuperuser

# Backend - Load test data
docker-compose exec backend python manage.py loaddata fixtures/sample_emissions.json

# Backend - Run tests
docker-compose exec backend pytest

# Frontend - Access shell
docker-compose exec frontend sh
```

### Attach to Containers

**Using Makefile:**
```bash
# Attach to backend container
make attach-backend

# Attach to frontend container
make attach-frontend
```

**Or using Docker directly:**
```bash
docker attach backend
docker attach frontend
```

### Rebuild a Specific Service

**Using Makefile:**
```bash
# Rebuild only backend
make rebuild-backend

# Rebuild only frontend
make rebuild-frontend
```

**Or using Docker Compose:**
```bash
# Rebuild only backend
docker-compose build backend
docker-compose up -d backend

# Rebuild only frontend
docker-compose build frontend
docker-compose up -d frontend
```

## Environment Variables

Environment variables can be configured in a `.env` file at the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
```

Or pass them directly in `docker-compose.yml`.

## Development

### Development Mode with Hot Reload

For development, the backend code is mounted as a volume, so changes are reflected automatically. However, for the frontend you'll need to rebuild the image after significant changes.

### Database

The SQLite database is persisted in `./backend/db.sqlite3` via a Docker volume.

## Production

For production, consider:

1. **Remove source code volume** in `docker-compose.yml` (commented line)
2. **Configure appropriate environment variables**
3. **Use an external database** (PostgreSQL, MySQL) instead of SQLite
4. **Configure HTTPS** with a reverse proxy (Nginx, Traefik)
5. **Optimize Docker images**

## Troubleshooting

### Backend won't start

```bash
# View detailed logs
docker-compose logs backend

# Verify port 8000 is not in use
netstat -tuln | grep 8000
```

### Frontend can't connect to backend

Verify that:
- Both containers are on the same network (`emissions-network`)
- Frontend uses `http://backend:8000` for API calls (not `localhost`)
- Health checks are passing: `docker-compose ps`

### Clean everything and start fresh

```bash
# Stop and remove containers, networks, and volumes
docker-compose down -v

# Remove images
docker-compose rm -f

# Clean Docker system (careful: removes everything)
docker system prune -a
```

## Architecture

```
┌─────────────────┐
│   Frontend      │
│   (Nginx)       │
│   Port: 4200    │
└────────┬────────┘
         │
         │ HTTP
         │
┌────────▼────────┐
│   Backend       │
│   (Django)      │
│   Port: 8000    │
└─────────────────┘
```

Both services are on the `emissions-network` network and can communicate using service names (`backend`, `frontend`).
