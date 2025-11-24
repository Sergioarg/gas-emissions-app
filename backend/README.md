# Gas Emissions API Documentation

## Overview

This documentation outlines how to set up and use the Gas Emissions API, a Django backend designed for secure and efficient management of greenhouse gas emissions data.
The API follows Domain-Driven Design (DDD) principles and provides comprehensive filtering capabilities.

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

6. Configure environment variables:

   Create a `.envrc` file or set environment variables:

   ```bash
    cd backend/ && touch .envrc

   ```

   ```bash
   export SECRET_KEY='your-secret-key-here'
   export DEBUG='True'  # Use 'False' for production
   ```

   Or use the provided `.envrc` file (requires `direnv`):

   ```bash
   direnv allow && source .envrc
   ```

7. Apply migrations to set up the database:

```
python manage.py migrate
```

8. (Optional/Recomended) Load sample data with 25 emission records:

```
python manage.py loaddata emissions/fixtures/sample_emissions.json
```

The sample data includes emissions from various English-speaking countries (United States, United Kingdom, Canada, Australia, etc.) with different emission types (CO2, CH4, N2O, SF6) and activities (Transportation, Agriculture, Energy Production, Waste, Industrial Processes).

## Running the Server

To start the server, run:

```
python manage.py runserver
```

The server will start at `http://localhost:8000`.

## API Endpoints

## Accessing the API Endpoints

Once the application is running, you can access the API endpoints using a web browser or a tool like `curl` or Postman.

### Postman Collection

A Postman collection is included with pre-configured requests and example responses. This makes it easy to test the API without writing curl commands.

#### Collection Contents

The collection includes:

- **Get Emissions** request with multiple example responses:
  - **Get All Emissions**: Example response for retrieving all emissions
- **Optional Filter**:
  - **By Country**: Example response for filtering by country (e.g., `?country=Japan,Canada`)
  - **By Waste**: Example response for filtering by activity (e.g., `?activity=Waste`)
  - **By Emission Type**: Example response for filtering by emission type with multiple values (e.g., `?emission_type=N2O,CH4`)

#### Using the Collection

1. The collection uses a variable `{{localhost}}` set to `http://localhost:8000`
2. You can modify query parameters directly in the request
3. View example responses by clicking on the "Examples" dropdown in the response section
4. Enable/disable query parameters as needed to test different filter combinations

### CURL Base

```bash
curl -X GET "http://localhost:8000/api/emissions/" \
  -H "Content-Type: application/json"
```

#### Example Requests in Collection

- `GET {{localhost}}/api/emissions/` - Get all emissions
- `GET {{localhost}}/api/emissions/?country=Japan` - Filter by country
- `GET {{localhost}}/api/emissions/?activity=Waste` - Filter by activity
- `GET {{localhost}}/api/emissions/?emission_type=N2O,CH4` - Filter by multiple emission types
- `GET {{localhost}}/api/emissions/?emission_type=N2O,CH4&activity=Waste` - Filter by multiple params

### Response Format

All endpoints return data in the following format:

```json
[
  {
    "year": 2016,
    "emissions": 2.9,
    "emission_type": "N2O",
    "country": "United Kingdom",
    "activity": "Waste"
  }
]
```

#### Validation Rules

- Numeric-only values are rejected: `?country=123` returns 400 Bad Request
- Multiple comma-separated values are supported: `?country=Japan,Canada` is valid

### Available Filter Values

#### Activities (Economic Sectors)

- Transportation
- Agriculture
- Energy Production
- Industrial Processes
- Waste
- Manufacturing
- Mining
- Deforestation
- Cement Production
- Fuel Combustion

#### Emission Types

- CO2 (Carbon Dioxide)
- CH4 (Methane)
- N2O (Nitrous Oxide)
- SF6 (Sulfur Hexafluoride)

## Testing

The project includes comprehensive tests covering all layers of the DDD architecture.

### Run Tests with pytest

#### Run All Tests

```bash
# Run all tests
pytest
# without coverage
pytest --no-cov
```

#### Run Specific Test Classes or Methods

```bash

# Run specific file
pytest emissions/tests/test_api.py

# Run tests matching a pattern
pytest -k "TestEmissionAPI" -v --no-cov
```

### Test Coverage

The test suite covers:

```
---------- coverage: platform linux, python 3.10.12-final-0 ----------
Name                                            Stmts   Miss  Cover   Missing
-----------------------------------------------------------------------------
emissions/__init__.py                               0      0   100%
emissions/app/__init__.py                           0      0   100%
emissions/app/service.py                           21      2    90%   17, 21
emissions/apps.py                                   4      0   100%
emissions/domain/emission.py                       12      0   100%
emissions/domain/repository.py                     13      3    77%   13, 17, 27
emissions/helpers/__init__.py                       0      0   100%
emissions/helpers/query_parser.py                   7      0   100%
emissions/helpers/validators.py                    13      2    85%   23, 29
emissions/infrastructure/__init__.py                0      0   100%
emissions/infrastructure/django_repository.py      31      4    87%   17-18, 21-22
emissions/migrations/0001_initial.py                5      0   100%
emissions/migrations/__init__.py                    0      0   100%
emissions/models.py                                10      1    90%   13
emissions/serializers.py                           12      0   100%
emissions/tests/__init__.py                         0      0   100%
emissions/tests/conftest.py                        18      1    94%   51
emissions/tests/test_api.py                        46      0   100%
emissions/tests/test_helpers.py                    15      0   100%
emissions/views.py                                 29      2    93%   52-53
-----------------------------------------------------------------------------
TOTAL                                             236     15    94%
Coverage HTML written to dir htmlcov
```

### Run Tests with Coverage

```bash
# Run tests with coverage report
pytest --cov=emissions --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

## Django App Emissions Files

```
📁 emissions/
├── 📁 domain/
│   ├── emission.py
│   └── repository.py
├── 📁 app/
│   └── service.py
├── 📁 infrastructure/
│   └── django_repository.py
├── 📁 helpers/
│   ├── query_parser.py
│   └── validators.py
├── 📁 tests/
│   ├── conftest.py
│   ├── test_api.py
│   └── test_helpers.py
├── models.py
├── serializers.py
└── views.py
```

### Data Flow

```
Request → ViewSet → Application Service → Repository → Database (ORM)
                ↓
         Query Parser (helpers)
                ↓
         Validators (helpers)
```

### Supported Emission Types

- **CO2**: Carbon Dioxide
- **CH4**: Methane
- **N2O**: Nitrous Oxide
- **SF6**: Sulfur Hexafluoride
