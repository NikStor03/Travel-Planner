# Travel Planner API

A FastAPI backend that allows users to create travel projects, attach places to visit, add notes, and track visit completion.

The project focuses on clean architecture, business rules, and testability

---

## Overview

A **travel project** is a collection of places a user wants to visit.

- Projects can contain 1–10 places
- Places are validated using the Art Institute of Chicago API
- Users can add notes and mark places as visited
- When all places are visited, the project is automatically marked as **completed**
- Projects **cannot be deleted** if any place is visited

---

## Tech Stack

- Python 3.11+
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic v2
- HTTPX
- Pytest + pytest-cov
- Docker / Docker Compose

---

## Architecture

The application uses a layered design:

- Routers – HTTP & validation
- Services – business logic
- Repositories – database access
- External clients – third-party API integration

This keeps the codebase modular, testable, and easy to extend.

---

## API

Interactive API documentation:

### Projects
- `POST /projects`
- `GET /projects`
- `GET /projects/{id}`
- `PATCH /projects/{id}`
- `DELETE /projects/{id}`

### Places (project-scoped)
- `POST /projects/{id}/places`
- `GET /projects/{id}/places`
- `GET /projects/{id}/places/{place_id}`
- `PATCH /projects/{id}/places/{place_id}`

---

## Third-Party API

Places are validated using the **Art Institute of Chicago API**:

- `GET /api/v1/artworks/{id}`
Responses are cached to reduce external calls.

---

## Running Locally

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload```

API available at:
http://localhost:8000/docs

---

## Running with Docker

```docker compose up --build```

---

## Testing

```python -m pytest```

## Coverage
```python -m pytest --cov=app --cov-report=term-missing```
