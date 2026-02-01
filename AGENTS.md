# Repository Guidelines

## Project Structure & Module Organization

- `backend/`: FastAPI + SQLModel service.
  - Entry point: `backend/app/main.py`
  - API routes: `backend/app/api/routes/`
  - DB/config/security: `backend/app/core/`
  - Models: `backend/app/models/`
  - Migrations: `backend/app/alembic/` (Alembic)
  - Tests: `backend/tests/`
- `frontend/`: Vite + React app.
  - Source: `frontend/src/` (UI in `frontend/src/components/`, API calls in `frontend/src/services/`)
  - Build output: `frontend/dist/`
- `compose.yml`: local infra (PostgreSQL, etc.)
- `scripts/`: helper scripts and utilities

## Build, Test, and Development Commands

Run from the repo root:

- `npm run dev`: run backend + frontend (default: API on `:8000`, UI on `:5173`)
- `npm run dev:backend`: run FastAPI with reload
- `npm run dev:frontend`: run Vite dev server
- `npm run docker:db`: start PostgreSQL via Docker Compose
- `npm run db:migrate`: apply migrations (`alembic upgrade head`)
- `npm run db:makemigrations`: generate a migration (`alembic revision --autogenerate`)
- `npm run db:seed`: seed initial data

Python dependencies use `uv`: `cd backend && uv sync`.

## Coding Style & Naming Conventions

- Python: format/lint with Ruff (88-char lines). Use `npm run format:backend` and `npm run lint:backend`.
- Frontend: keep components in `PascalCase` (e.g., `ChatMessage.jsx`) and variables/functions in `camelCase`.

## Testing Guidelines

- Backend: `cd backend && uv run pytest` (place tests in `backend/tests/`, name files `test_*.py`).
- Frontend: no test runner is wired up yet.
- Pre-commit runs Ruff + pytest (see `.pre-commit-config.yaml`).

## Commit & Pull Request Guidelines

- Prefer Conventional Commit-style subjects used in this repo: `feat:`, `fix:`, `refactor:`, `chore:`.
- PRs include: concise description, testing notes/commands, linked issue (if any), and screenshots for UI changes.
- CI (`.github/workflows/test.yml`) runs backend tests and expects `frontend` lint/build; frontend lint currently requires adding an ESLint config.

## Security & Configuration Tips

- Use `.env` for local configuration; do not commit secrets (API keys, JWT secrets, database URLs).
- When adding new env vars, document them in `README.md`.

## Agent-Specific Instructions

- Do **not** write or modify LangGraph / AI / LLM-related code (including prompts, agents, workflows, or files under `backend/app/langgraph/`). I’m learning LangGraph and want to implement those parts myself.
- You may still help by reviewing, explaining, or suggesting approaches for LangGraph/AI changes, but keep it to guidance (no code edits).
