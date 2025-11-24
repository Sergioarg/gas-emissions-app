# Gas Emissions APP

A full-stack application for managing and querying greenhouse gas emissions data. The project consists of a Django REST API backend and an Angular frontend, following Domain-Driven Design (DDD) principles and SOLID best practices.

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Technologies](#technologies)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Development](#local-development)
  - [Docker Development](#docker-development)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [CI/CD](#cicd)
- [Project Architecture](#project-architecture)
- [Additional Documentation](#additional-documentation)

## 🎯 Overview

The Gas Emissions API provides a RESTful interface for querying greenhouse gas emissions data with advanced filtering capabilities. The backend is built with Django and follows Domain-Driven Design principles, ensuring clean architecture and maintainability.

### Key Features

- ✅ **RESTful API** for emissions data
- ✅ **Advanced Filtering** by country, activity, and emission type
- ✅ **Domain-Driven Design** architecture
- ✅ **Database-level filtering** for optimal performance
- ✅ **Comprehensive test coverage** (94%+)
- ✅ **CI/CD pipeline** with GitHub Actions
- ✅ **Postman collection** included for API testing

## 📁 Project Structure

```
gas-emissions-api/
├── backend/                 # Django REST API
│   ├── emissions/           # Main Django app
│   │   ├── domain/         # Domain layer (entities, repositories)
│   │   ├── app/            # Application layer (services)
│   │   ├── infrastructure/ # Infrastructure layer (Django ORM)
│   │   ├── helpers/        # Utility functions
│   │   └── tests/          # Test suite
│   ├── config/             # Django project settings
│   ├── fixtures/           # Sample data
│   └── Postman/            # Postman collection
├── frontend/               # Angular application
├── .github/
│   └── workflows/          # CI/CD pipelines
├── docker-compose.yml      # Docker orchestration
└── README.md              # This file
```

## 🛠 Technologies

### Backend
- **Python 3.10+**
- **Django 5.0.6** - Web framework
- **Django REST Framework 3.15.1** - API framework
- **SQLite3** - Database (development/testing)
- **pytest** - Testing framework
- **isort** - Import sorting
- **flake8** - Code linting

### Frontend
- **Angular 21**
- **TypeScript**
- **Nginx** - Web server

### DevOps
- **Docker & Docker Compose** - Containerization
- **GitHub Actions** - CI/CD
- **pytest-cov** - Test coverage

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+** (for local backend development)
- **Node.js & npm** (for local frontend development)
- **Docker & Docker Compose** (for containerized development)
- **Git**

### Local Development

#### Backend Setup

For detailed instructions on setting up and using the backend, see the file [backend/README.md](../backend/README.md).


### Docker Development

The easiest way to run the entire application is using Docker Compose:

1. **Build and start all services:**
   ```bash
   docker-compose up --build
   ```

2. **Access the application:**
   - **Frontend**: http://localhost:4200
   - **Backend API**: http://localhost:8000
   - **API Endpoints**: http://localhost:8000/api/emissions/

3. **Stop services:**
   ```bash
   docker-compose down
   ```

For detailed Docker instructions, see [README.DOCKER.md](./README.DOCKER.md)

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api/emissions/
```

### Endpoints

#### GET /api/emissions/
Retrieve all emissions or filtered results.

**Query Parameters:**
- `country` (optional): Filter by country name(s). Supports comma-separated values.
  - Example: `?country=Japan` or `?country=Japan,Canada`
- `activity` (optional): Filter by activity type(s). Supports comma-separated values.
  - Example: `?activity=Transportation` or `?activity=Transportation,Agriculture`
- `emission_type` (optional): Filter by emission type(s). Supports comma-separated values.
  - Example: `?emission_type=CO2` or `?emission_type=CO2,CH4`

**Multiple filters:** Combine filters using `&` (AND logic)
- Example: `?country=Japan&emission_type=CO2&activity=Transportation`

**Response:**
```json
[
  {
    "id": 1,
    "year": 2020,
    "emissions": 100.5,
    "emission_type": "CO2",
    "country": "Japan",
    "activity": "Transportation",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

## 🔄 CI/CD

The project includes a GitHub Actions workflow for continuous integration:
Workflow Location:  `.github/workflows/backend-ci.yml`

## 🔒 Security Notes

- **SQLite3** is used for development/testing only
- **Production** should use PostgreSQL or another production-grade database
- **API Key authentication** should be implemented for production
- **SECRET_KEY** must be set via environment variables (never commit to repository)
---

### Notes:
This is a technical test project. For production deployment, consider:
- Using a production database (PostgreSQL)
- Implementing API key authentication
- Setting up proper logging and monitoring
- Using a production WSGI server (Gunicorn, uWSGI)
- Configuring HTTPS and security headers

