# Gas Emissions API Documentation

## Overview

This documentation outlines how to set up and use the Gas Emissions API, a Django backend designed for secure and efficient management of greenhouse gas emissions data. The API follows Domain-Driven Design (DDD) principles and provides comprehensive filtering capabilities.

## API Endpoints

The API provides read-only access to emissions data with advanced filtering capabilities:

### Emissions Management

- **List Emissions**: `GET /api/emissions/` - Retrieve emissions with optional filtering

## Getting Started

### Prerequisites

- Python 3.10.0 or higher
- Django 5.0.6 or higher
- Django REST framework 3.15.1 or higher
- pytest (for testing)

### Installation

1. Clone the repository:
    ```
    git clone <repository-url>
    ```
2. Navigate to the backend directory:
   ```
   cd gas-emissions-api/backend
   ```
3. Create a virtual environment (optional but recommended):
   ```
   python3 -m venv venv
   ```
4. Activate the virtual environment:
   - On Windows:
      ```
      .\venv\Scripts\activate
      ```
   - On Unix or MacOS:
     ```
     source venv/bin/activate
     ```
5. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
6. Apply migrations to set up the database:
   ```
   python manage.py migrate
   ```
7. (Optional) Load sample data:
   ```
   python manage.py loaddata emissions/fixtures/sample_emissions.json
   ```

## Running the Server

To start the server, run:
```
python manage.py runserver
```
The server will start at `http://localhost:8000`.

## API Endpoints

### Usage

To interact with the API, you can use tools like `curl`, Postman, or any HTTP client library in your preferred programming language.

### Emissions Endpoint

**Base URL**: `http://127.0.0.1:8000/api/emissions/`

#### List Emissions with Filtering

- **Endpoint**: `/api/emissions/`
- **Method**: `GET`
- **Description**: Retrieve emissions data with optional filtering
- **Query Parameters**:
  - `country` (string): Filter by country name (e.g., "México", "Brasil")
  - `activity` (string): Filter by activity type (e.g., "Transporte", "Industria")
  - `emission_type` (string): Filter by emission type (e.g., "CO2", "CH4")
- **Response**: Array of emission objects
- **Example Response**:
  ```json
  [
    {
      "id": 1,
      "year": 2023,
      "emissions": 150.5,
      "emission_type": "CO2",
      "country": "México",
      "activity": "Transporte",
      "created_at": "2023-11-22T12:00:00Z"
    }
  ]
  ```

## Accessing the API Endpoints

Once the application is running, you can access the API endpoints using a web browser or a tool like `curl` or Postman.

### API Usage Examples

#### Get All Emissions
```bash
curl -X GET "http://127.0.0.1:8000/api/emissions/" \
     -H "Content-Type: application/json"
```

#### Filter by Country
```bash
curl -X GET "http://127.0.0.1:8000/api/emissions/?country=México" \
     -H "Content-Type: application/json"
```

#### Filter by Activity
```bash
curl -X GET "http://127.0.0.1:8000/api/emissions/?activity=Transporte" \
     -H "Content-Type: application/json"
```

#### Filter by Emission Type
```bash
curl -X GET "http://127.0.0.1:8000/api/emissions/?emission_type=CO2" \
     -H "Content-Type: application/json"
```

#### Multiple Filters
```bash
curl -X GET "http://127.0.0.1:8000/api/emissions/?country=Brasil&emission_type=CH4" \
     -H "Content-Type: application/json"
```

### Response Format

All endpoints return data in the following format:

```json
{
  "count": 25,
  "results": [
    {
      "id": 1,
      "year": 2023,
      "emissions": 150.5,
      "emission_type": "CO2",
      "country": "México",
      "activity": "Transporte",
      "created_at": "2023-11-22T12:00:00Z"
    }
  ]
}
```

### Available Filter Values

#### Countries (Nombres completos)
- México
- Brasil
- Argentina
- Colombia
- Perú
- Chile
- Ecuador
- Uruguay

#### Activities (Actividades)
- Transporte
- Industria
- Agricultura
- Energía
- Manufactura
- Minería
- Residuos
- Deforestación
- Producción de cemento
- Quema de combustibles

#### Emission Types (Tipos de Emisión)
- CO2 (Dióxido de Carbono)
- CH4 (Metano)
- N2O (Óxido Nitroso)
- SF6 (Hexafluoruro de Azufre)

## Testing

The project includes comprehensive tests covering all layers of the DDD architecture.

### Run Tests with pytest

```bash
# Run all tests
python -m pytest emissions/tests.py -v

# Run with coverage report
python -m pytest emissions/tests.py --cov=emissions --cov-report=html

# Run specific test categories
python -m pytest emissions/tests.py::TestCountryValueObject -v  # Domain tests
python -m pytest emissions/tests.py::TestEmissionAPI -v        # API tests
```

### Test Coverage

The test suite covers:

- **Domain Layer**: Value Objects, Entities, and business rules
- **Application Layer**: Use cases and service orchestration
- **Infrastructure Layer**: Repository implementations and data access
- **Presentation Layer**: API endpoints, serialization, and filtering

## Architecture

This API follows **Domain-Driven Design (DDD)** principles with clean architecture:

```
📁 emissions/
├── 📁 domain/           # Domain Layer
│   ├── emission.py      # Domain Entity
│   └── repository.py    # Repository Interface
├── 📁 app/             # Application Layer
│   └── service.py      # Application Services
├── 📁 infrastructure/  # Infrastructure Layer
│   └── django_emission_repository.py  # Repository Implementation
├── 📁 value_objects.py # Domain Value Objects
├── 📁 serializers.py   # Presentation Serializers
├── 📁 views.py         # API Controllers
├── 📁 helpers.py       # Filtering Logic
└── 📁 tests.py         # Comprehensive Tests
```

### Key Design Patterns

- **Repository Pattern**: Abstract data access
- **Value Objects**: Immutable domain objects
- **Application Services**: Use case orchestration
- **Clean Architecture**: Dependency inversion

## Data Model

### Emission Entity

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| year | Integer | Year of emission |
| emissions | Decimal | Emission amount (tons) |
| emission_type | String | Type of greenhouse gas |
| country | String | Country name (full name) |
| activity | String | Economic activity sector |
| created_at | DateTime | Record creation timestamp |

### Supported Countries

The API includes data for Latin American countries:
- México, Brasil, Argentina, Colombia, Perú, Chile, Ecuador, Uruguay

### Supported Emission Types

- **CO2**: Carbon Dioxide
- **CH4**: Methane
- **N2O**: Nitrous Oxide
- **SF6**: Sulfur Hexafluoride
