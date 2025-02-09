# E-commerce API

This project is an academic assignment for WSEI University, implementing an e-commerce API using FastAPI.

## Table of Contents

- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Static Frontend](#static-frontend)
- [Database Initialization](#database-initialization)
  - [Populating the Database](#populating-the-database)
- [Running Tests](#running-tests)

## Getting Started

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ddragula/py-ecommerce-fastapi-wsei.git
   cd py-ecommerce-fastapi-wsei
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate # On Windows
   source .venv/bin/activate # On Linux or MacOS
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Start the FastAPI server with:

```bash
python main.py
```

The API will be available at `http://127.0.0.1:8000`.

## API Documentation

FastAPI provides interactive API documentation:

- Swagger UI: [http://127.0.0.1:8000/api/docs](http://127.0.0.1:8000/api/docs)
- ReDoc: [http://127.0.0.1:8000/api/redoc](http://127.0.0.1:8000/api/redoc)
- OpenAPI JSON: [http://127.0.0.1:8000/api/openapi.json](http://127.0.0.1:8000/api/openapi.json)

All API endpoints are prefixed with `/api`, ensuring separation between API functionality and frontend content.

## Static Frontend

The application serves static frontend files from the `/` route. The `static/` directory contains these files, including `index.html`.

The frontend is already built and included in the repository. If you need to modify it, navigate to the `frontend/` directory, make changes, and rebuild it with:
```sh
cd frontend
npm run build
```

## Database Initialization

Ensure that the database and tables are initialized before using the API. The application creates the necessary tables automatically on startup. If the database file is missing, ensure that the `@app.on_event("startup")` function correctly triggers table creation.

### Populating the Database

To add example products to the database, run:
```sh
python populate_products.py
```

## Running Tests

To execute the unit tests, run:
```sh
pytest tests/
```

This will check the core functionality of the application.

## Author

Created by Dawid Draguła as part of final assignments for classes at WSEI.

