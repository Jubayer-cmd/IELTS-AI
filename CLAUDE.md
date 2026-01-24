# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

IELTS Writing Feedback AI - a web application where users submit IELTS essays and get AI-powered band scores (1-9) and feedback. Users pay per evaluation using credits purchased via SSLCommerz payment gateway.

**Stack**: React 18 + Vite + TailwindCSS (frontend) | FastAPI + SQLModel + PostgreSQL (backend) | LangGraph + LangChain (AI)

## Common Commands

```bash
# Development (runs both frontend and backend)
npm run dev

# Run only backend (FastAPI on port 8000)
npm run dev:backend
# Or directly: cd backend && uv run uvicorn app.main:app --reload

# Run only frontend (Vite on port 5173)
npm run dev:frontend

# Database
npm run db:migrate              # Run Alembic migrations
npm run db:makemigrations       # Generate new migration
npm run db:seed                 # Seed initial data
npm run docker:db               # Start PostgreSQL via Docker

# Testing
npm run test:backend            # Run pytest
cd backend && uv run pytest -v  # With verbose output
cd backend && uv run pytest tests/test_auth.py -v  # Single test file
cd backend && uv run pytest -k "test_register"     # Run specific test

# Linting & Formatting
npm run lint:backend            # Ruff check
npm run format:backend          # Ruff format
```

## Architecture

### Backend Structure (FastAPI Full-Stack Template Pattern)

```
backend/app/
├── main.py           # App entry, lifespan, CORS, mounts api_router at /api/v1
├── models.py         # ALL SQLModel models + Pydantic schemas in one file
├── crud.py           # Database operations (create_user, authenticate, etc.)
├── api/
│   ├── main.py       # Router aggregation - includes all route modules
│   ├── deps.py       # Shared dependencies (SessionDep, CurrentUser, get_db)
│   └── routes/       # Endpoint modules (auth.py, users.py, writing.py)
└── core/
    ├── config.py     # Pydantic Settings from .env
    ├── db.py         # SQLModel engine, init_db()
    └── security.py   # JWT creation, password hashing (bcrypt)
```

### Key Patterns

**Dependency Injection**: Use type aliases from `app.api.deps`:
```python
from app.api.deps import SessionDep, CurrentUser

@router.get("/me")
def get_me(current_user: CurrentUser):  # Automatically validates JWT
    return current_user
```

**Models Pattern**: `models.py` contains both SQLModel tables AND Pydantic schemas:
- `User` (table=True) - database model
- `UserCreate`, `UserPublic`, `UserUpdate` - API schemas

**CRUD Pattern**: All database operations go through `crud.py`:
```python
from app import crud
user = crud.create_user(session=session, user_create=user_data)
```

### Frontend Structure

```
frontend/src/
├── services/api.jsx   # Axios client with auth interceptors, all API calls
├── services/auth.jsx  # Auth context provider
├── components/Chat/   # Main chat interface components
└── components/ui/     # Radix UI primitives
```

API calls use `/api/v1` prefix. Auth token stored in localStorage as `access_token`.

## Database

- PostgreSQL with SQLModel (SQLAlchemy + Pydantic)
- Alembic for migrations (config in `backend/alembic.ini`)
- Connection string in `.env` as `DATABASE_URL`
- Test database: `ielts_test` (configured in `tests/conftest.py`)

## Authentication Flow

1. Register: POST `/api/v1/auth/register` with `{name, email, password}`
2. Login: POST `/api/v1/auth/login` with OAuth2 form data (`username`, `password`)
3. Token returned as `{access_token, token_type: "bearer"}`
4. Protected routes use `CurrentUser` dependency which validates JWT

## Environment Variables

All config in root `.env` file. Key variables:
- `DATABASE_URL` - PostgreSQL connection string
- `JWT_SECRET_KEY` - For token signing (change in production!)
- `CORS_ORIGINS` - Allowed frontend origins
- `OPENAI_API_KEY` / `GOOGLE_API_KEY` - LLM providers
- `VITE_API_URL` - Frontend's backend URL

## Testing

Tests use pytest with FastAPI TestClient. Fixtures in `tests/conftest.py`:
- `session` - Fresh database session per test
- `client` - TestClient with DB override
- `test_user` - Pre-created user for auth tests

Tests require `ielts_test` PostgreSQL database or set `TEST_DATABASE_URL`.
