# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

IELTS Writing Feedback AI - a web application where users submit IELTS essays and get AI-powered band scores (1-9) and feedback. Users pay per evaluation using credits purchased via SSLCommerz payment gateway.

**Stack**: React 19 + Vite + TailwindCSS (frontend) | FastAPI + SQLModel + PostgreSQL (backend) | LangGraph + LangChain (AI)

---

## Serena MCP Integration

This project uses **Serena** - a semantic coding MCP tool for intelligent code navigation and editing.

### Configuration

- **Location**: `.serena/project.yml`
- **Project Name**: `IELTS_WRITING_AI`
- **Language Server**: TypeScript (also covers JavaScript)
- **Encoding**: UTF-8

### Serena Memories (Project Context)

Serena stores project-specific memories in `.serena/memories/`. Always check these for context:

| Memory File                              | Purpose                                                                        |
| ---------------------------------------- | ------------------------------------------------------------------------------ |
| `backend_api_structure_analysis.md`      | Complete API routes, auth flow, dependencies, and LangGraph integration points |
| `langgraph_learning_syllabus.md`         | 10-module curriculum progress (currently at Module 5 - Streaming)              |
| `langgraph-frontend-integration-plan.md` | Step-by-step plan for SSE streaming and React integration                      |
| `user-learning-profile.md`               | User's learning preferences and goals                                          |

### Using Serena Tools

Prefer Serena's semantic tools for code navigation:

```
- find_symbol: Find functions/classes by name
- get_symbols_overview: Get file structure
- find_referencing_symbols: Find usages
- replace_symbol_body: Replace entire function/class
- search_for_pattern: Regex search across codebase
```

---

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

# Python dependencies
cd backend && uv sync           # Install/update dependencies

# UI Testing (Browser Automation with agent-browser)
agent-browser open http://localhost:5173   # Open frontend in browser
agent-browser snapshot -i                  # Get interactive elements (for AI)
agent-browser click @e2                    # Click element by ref from snapshot
agent-browser fill @e3 "test@example.com"  # Fill input field
agent-browser screenshot --full            # Full page screenshot
agent-browser --headed open localhost:5173 # Show browser window (not headless)
```

---

## Architecture

### Backend Structure (FastAPI Full-Stack Template Pattern)

```
backend/app/
├── main.py                    # FastAPI app setup, CORS, mounts at /api/v1
├── utils.py                   # Utility functions
├── initial_data.py            # Database seeding
├── backend_pre_start.py       # Pre-startup checks
├── api/
│   ├── main.py               # Router aggregation
│   ├── deps.py               # SessionDep, CurrentUser, TokenDep
│   └── routes/
│       ├── auth.py           # Authentication endpoints
│       └── chat.py           # Chat/thread endpoints (SSE streaming)
├── core/
│   ├── config.py             # Pydantic Settings from .env
│   ├── db.py                 # SQLModel engine, init_db()
│   ├── security.py           # JWT creation, password hashing (bcrypt)
│   └── memory.py             # LangGraph memory/checkpoint config
├── models/
│   ├── users.py              # User table + schemas
│   ├── chat.py               # Thread, ChatMessage models
│   └── common.py             # Generic Message schema
├── crud/
│   ├── user.py               # User CRUD operations
│   └── chat.py               # Thread/Message CRUD
├── services/
│   └── langgraph.py          # LangGraph service wrapper
├── langgraph/
│   └── agent.py              # LangGraph agent (chat + essay evaluation)
└── alembic/                  # Database migrations
```

### Frontend Structure

```
frontend/src/
├── main.jsx                   # App entry point
├── App.jsx                    # Router setup
├── services/
│   ├── api.jsx               # Axios client, all API calls, SSE streaming
│   ├── auth.jsx              # Auth context provider
│   └── payment.jsx           # Payment handling
├── store/
│   └── authStore.js          # Zustand auth state
├── context/
│   └── ThemeProvider.jsx     # Theme context
├── components/
│   ├── Chat/                 # Main chat interface
│   │   ├── ChatWindow.jsx    # Message display + input
│   │   ├── MessageList.jsx   # Streaming message rendering
│   │   ├── ChatInput.jsx     # Input component
│   │   ├── Sidebar.jsx       # Thread list
│   │   └── MobileSidebar.jsx
│   ├── Auth/                 # Login/Register forms
│   ├── Settings/             # User settings
│   ├── Common/               # Shared components
│   └── ui/                   # Radix UI primitives
├── pages/
│   ├── HomePage.jsx          # Main chat page
│   ├── LoginPage.jsx
│   └── RegisterPage.jsx
├── hooks/
│   └── useAuth.js            # Auth hook
└── lib/
    └── utils.js              # Utility functions
```

---

## Key Patterns

### Dependency Injection

Use type aliases from `app.api.deps`:

```python
from app.api.deps import SessionDep, CurrentUser

@router.get("/me")
def get_me(current_user: CurrentUser):  # Automatically validates JWT
    return current_user
```

### Models Pattern

`models/` contains both SQLModel tables AND Pydantic schemas:

- `User` (table=True) - database model
- `UserCreate`, `UserPublic`, `UserUpdate` - API schemas

### CRUD Pattern

All database operations go through `crud/`:

```python
from app.crud import user as user_crud
user = user_crud.create_user(session=session, user_create=user_data)
```

### SSE Streaming Pattern

Backend uses `sse-starlette` for streaming:

```python
from sse_starlette.sse import EventSourceResponse

@router.post("/threads/{thread_id}/stream")
async def stream_message(...):
    async def event_generator():
        for chunk in langgraph_service.stream(...):
            yield {"event": "token", "data": json.dumps({"token": chunk})}
        yield {"event": "done", "data": "{}"}
    return EventSourceResponse(event_generator())
```

Frontend consumes with native EventSource or fetch ReadableStream.

---

## Database

- PostgreSQL with SQLModel (SQLAlchemy + Pydantic)
- Alembic for migrations (config in `backend/alembic.ini`)
- Connection string in `.env` as `DATABASE_URL`
- Test database: `ielts_test` (configured in `tests/conftest.py`)

### Current Tables

- `user` - User accounts with credits
- `thread` - Chat conversation threads
- `chatmessage` - Individual messages within threads

---

## Authentication Flow

1. Register: POST `/api/v1/auth/register` with `{first_name, last_name, email, password}`
2. Login: POST `/api/v1/auth/login` with OAuth2 form data (`username`, `password`)
3. Token returned as `{access_token, token_type: "bearer"}`
4. Protected routes use `CurrentUser` dependency which validates JWT
5. Frontend stores token in `localStorage` as `access_token`

---

## LangGraph Agent

**Location**: `backend/app/langgraph/agent.py`

### Current Features

- **Two nodes**: `chat` (English tutor) and `essay` (IELTS evaluator)
- **LLM-based routing**: Classifies user intent to route appropriately
- **Tools**: `count_words`, `count_words_limit`
- **Persistence**: `MemorySaver` checkpointer for conversation history
- **Streaming**: `stream_mode="messages"` for token-by-token output

### Learning Progress (Module 5 of 10)

✅ Modules 1-4 Complete: Fundamentals, Persistence, Routing, Tools
⏳ Module 5 In Progress: Streaming (basic complete, FastAPI SSE done)
📋 Upcoming: Human-in-the-Loop, Error Handling, Subgraphs, Multi-Agent

See `.serena/memories/langgraph_learning_syllabus.md` for full curriculum.

---

## Environment Variables

All config in root `.env` file. Key variables:

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/ielts

# Authentication
JWT_SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=["http://localhost:5173"]

# LLM Providers
OPENROUTER_API_KEY=your-key
OPENAI_API_KEY=your-key
GOOGLE_API_KEY=your-key

# Frontend
VITE_API_URL=http://localhost:8000
```

---

## Testing

Tests use pytest with FastAPI TestClient. Fixtures in `tests/conftest.py`:

- `session` - Fresh database session per test
- `client` - TestClient with DB override
- `test_user` - Pre-created user for auth tests

Tests require `ielts_test` PostgreSQL database or set `TEST_DATABASE_URL`.

### UI Testing with agent-browser

`agent-browser` is a browser automation CLI designed for AI agents. Use it to test the frontend UI.

**Workflow:**

```bash
# 1. Start the frontend
npm run dev:frontend

# 2. Open and get element refs
agent-browser open http://localhost:5173
agent-browser snapshot -i              # Shows interactive elements with @refs

# 3. Interact using refs from snapshot
agent-browser click @e5                # Click element ref @e5
agent-browser fill @e3 "hello@test.com"
agent-browser type @e4 "my essay text"
agent-browser press Enter

# 4. Verify results
agent-browser screenshot results.png
agent-browser get text @e10            # Get text content
```

**Key Commands:**
| Command | Description |
|---------|-------------|
| `open <url>` | Navigate to URL |
| `snapshot -i` | Get accessibility tree with refs (AI-friendly) |
| `click @ref` | Click element by ref |
| `fill @ref <text>` | Clear and fill input |
| `type @ref <text>` | Type into element |
| `screenshot [path]` | Take screenshot |
| `--headed` | Show browser window (visible mode) |
| `wait <sel\|ms>` | Wait for element or milliseconds |

**Testing Chat Flow:**

```bash
agent-browser open http://localhost:5173
agent-browser snapshot -i                    # Find login/chat elements
agent-browser fill @e3 "user@example.com"    # Email
agent-browser fill @e4 "password123"         # Password
agent-browser click @e5                      # Login button
agent-browser wait 2000                      # Wait for redirect
agent-browser snapshot -i                    # Find chat input
agent-browser fill @e10 "Hello, AI!"         # Type message
agent-browser click @e11                     # Send button
```

---

## Coding Style & Conventions

- **Python**: Format/lint with Ruff (88-char lines)
- **Frontend**: Components in `PascalCase`, variables in `camelCase`
- **Commits**: Conventional style - `feat:`, `fix:`, `refactor:`, `chore:`
- **PRs**: Concise description, test notes, linked issues, screenshots for UI

---

## Agent-Specific Instructions

> ⚠️ **IMPORTANT**: These instructions are for AI agents working on this codebase.

### LangGraph Code Restrictions

**Do NOT write or modify LangGraph/AI/LLM-related code**, including:

- Files under `backend/app/langgraph/`
- Prompts, agents, or workflows
- LangChain integration code

The project owner is **learning LangGraph** and wants to implement those parts themselves.

**You MAY**:

- Review and explain LangGraph code
- Suggest approaches or patterns
- Answer questions about LangGraph concepts
- Help with non-LangGraph parts that integrate with the agent

### What Agents CAN Help With

✅ All non-LangGraph code (API routes, models, frontend, tests)
✅ Database migrations and schema design
✅ Frontend components and styling
✅ Authentication and authorization
✅ API integration and streaming
✅ Code review and debugging
✅ Documentation

---

## Quick Reference

### API Endpoints

| Endpoint                             | Method | Description       | Auth |
| ------------------------------------ | ------ | ----------------- | ---- |
| `/api/v1/auth/register`              | POST   | Register user     | No   |
| `/api/v1/auth/login`                 | POST   | Login (OAuth2)    | No   |
| `/api/v1/auth/me`                    | GET    | Get current user  | Yes  |
| `/api/v1/auth/me`                    | PATCH  | Update profile    | Yes  |
| `/api/v1/chat/threads`               | GET    | List threads      | Yes  |
| `/api/v1/chat/threads`               | POST   | Create thread     | Yes  |
| `/api/v1/chat/threads/{id}`          | DELETE | Delete thread     | Yes  |
| `/api/v1/chat/threads/{id}/messages` | GET    | Get messages      | Yes  |
| `/api/v1/chat/threads/{id}/stream`   | POST   | Stream chat (SSE) | Yes  |
| `/health`                            | GET    | Health check      | No   |

### File Locations Quick Reference

| What               | Where                            |
| ------------------ | -------------------------------- |
| API Routes         | `backend/app/api/routes/`        |
| Database Models    | `backend/app/models/`            |
| CRUD Operations    | `backend/app/crud/`              |
| LangGraph Agent    | `backend/app/langgraph/agent.py` |
| Frontend API Calls | `frontend/src/services/api.jsx`  |
| Chat Components    | `frontend/src/components/Chat/`  |
| Serena Memories    | `.serena/memories/`              |
| Environment Config | `.env` (root)                    |
