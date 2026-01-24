# 🎯 IELTS Writing Feedback AI

> **CLEAR PROJECT GOAL**: Build a web application where users submit IELTS essays and get AI-powered band scores (1-9) and feedback. Users pay per evaluation using credits purchased via SSLCommerz payment gateway.

## 🤖 **For AI Implementation:**
This is a **React + FastAPI + LangGraph** project with the following clear structure:
- **Frontend**: Single React app with user interface and admin panel
- **Backend**: FastAPI with LangGraph for AI evaluation workflow  
- **Database**: SQLite for users, payments, essays, evaluations
- **AI**: Single LLM call for comprehensive IELTS evaluation
- **Payment**: SSLCommerz integration for credit purchases

## 📖 Project Overview

This project helps IELTS test takers improve their writing skills by providing:
- **Instant band scores** (1-9) for essays
- **Detailed feedback** on all four IELTS criteria
- **Actionable improvement suggestions**
- **Support for both Task 1 and Task 2** essays
- **AI Agent can give task 1 or task 2 question and can evaluate the answer **
- **user can give question and answer in image or text to evaluate **

## 🏗️ Architecture

### Technology Stack
- **Frontend**: React 18 + Vite + TailwindCSS + Radix UI
- **Backend**: FastAPI + Python 3.10+ + SQLModel
- **Database**: PostgreSQL 15+
- **AI Framework**: LangGraph + LangChain
- **Auth**: JWT + bcrypt
- **Package Manager**: UV (Python), npm (Node)
- **DevOps**: Docker Compose, GitHub Actions

### System Design
```
React Frontend ──► FastAPI Backend ──► LangGraph Workflow ──► Multi-LLM AI
       │                   │                   │                    │
       │                   ▼                   ▼                    │
       │           PostgreSQL DB       State Management            │
       │                   │                   │                    │
       └────────────── JSON API Response ◄─────────────────────────┘
```

## 🎯 Core Features

### **Phase 1: MVP Core (Essential)**
- [ ] **Essay Evaluation Engine**
  - Text input with rich editor
  - Image input extract the word for evaluate
  - Essay length validation (150-400 words)
  - Language detection (English only)
  - Single LLM comprehensive evaluation
  - Instant IELTS band score (1-9)
  - Detailed feedback for 4 criteria
  - Task 1/2 automatic detection
  - Response time < 10 seconds

- [ ] **User & admin & Payment System**
  - Quick registration (email + password)
  - SSLCommerz payment integration
  - Credit-based pricing (50 BDT per evaluation)
  - Free trial (2-3 evaluations)
  - Credit balance tracking
  - Payment history

- [ ] **Core User Experience**
  - Mobile-responsive design
  - One-page evaluation flow
  - Instant results display(Streaming)
  - Basic essay history (last 10)
  - Share results feature

### **Phase 2: Business Growth**
- [ ] **Advanced Features**
  - Multiple LLM providers
  - Subscription plans

- [ ] **Admin & Scaling**
  - Admin dashboard (using the same react)

## 🤖 **FOR AI IMPLEMENTATION - STEP BY STEP**

### **DATABASE MODELS (SQLModel)**
```python
# Implemented in backend/app/models.py

class User(SQLModel, table=True):
    id: int
    name: str
    email: str                  # unique, indexed
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    credits: int = 3            # Free trial credits
    created_at: datetime

class Essay(SQLModel, table=True):
    id: int
    user_id: int                # Foreign key to User
    text: str
    task_type: TaskType         # TASK1 or TASK2
    word_count: int
    overall_score: float | None
    task_achievement: float | None
    coherence: float | None
    lexical: float | None
    grammar: float | None
    feedback: str | None
    created_at: datetime

# Payment model - TODO
class Payment(SQLModel, table=True):
    id, user_id, amount, credits_purchased, transaction_id, status
```

### **API ENDPOINTS (FastAPI)**
```python
# Essential endpoints to implement:

POST /auth/register           # User registration
POST /auth/login             # User login
GET  /auth/me                # Get current user

POST /payment/initiate       # Start SSLCommerz payment
POST /payment/success        # Payment success callback
POST /payment/cancel         # Payment cancel callback

POST /generate-question      # AI generates IELTS question
POST /evaluate              # Evaluate essay (deduct 1 credit)
GET  /evaluations           # User's evaluation history

GET  /admin/users           # Admin: view all users
GET  /admin/payments        # Admin: view all payments
```

### **LANGGRAPH WORKFLOW**
```python
# Simple single-step evaluation:

def evaluate_essay(essay_text, task_type):
    prompt = f"""
    Evaluate this IELTS {task_type} essay. Return ONLY valid JSON:
    
    {{
        "overall_band_score": 7.0,
        "task_achievement": {{"score": 7, "feedback": "Addresses task well..."}},
        "coherence_cohesion": {{"score": 6, "feedback": "Good organization..."}},
        "lexical_resource": {{"score": 7, "feedback": "Good vocabulary range..."}},
        "grammatical_accuracy": {{"score": 6, "feedback": "Generally accurate..."}},
        "improvement_suggestions": ["Use more complex sentences", "Add more examples"]
    }}
    
    Essay ({len(essay_text.split())} words): {essay_text}
    """
    
    return llm.invoke(prompt)
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 20+
- PostgreSQL 15+
- Docker (optional)
- LLM Provider API key (OpenAI, Google, or local Ollama)

### Setup & Run

```bash
# Clone and enter project
git clone <repo-url>
cd IELTS_WRITING_AI

# Copy environment file and edit values
cp .env.example .env

# Start PostgreSQL (using Docker)
npm run docker:db

# Install dependencies
npm install                    # Frontend deps
cd backend && uv sync          # Backend deps
cd ..

# Run both frontend and backend
npm run dev
```

### Using Docker (Recommended)

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down
```

### Available Scripts

```bash
# Development
npm run dev              # Run backend + frontend
npm run dev:backend      # Backend only (port 8000)
npm run dev:frontend     # Frontend only (port 5173)

# Database
npm run docker:db        # Start PostgreSQL
npm run db:migrate       # Run migrations
npm run db:seed          # Seed initial data

# Testing & Quality
npm run test             # Run all tests
npm run lint             # Lint code
npm run format           # Format code

# Docker
npm run docker:up        # Start all services
npm run docker:down      # Stop services
```

### Access
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc

### Usage
1. Register/Login to get credits
2. Purchase evaluation credits via SSLCommerz
3. Submit IELTS essay for evaluation
4. Get instant AI feedback and band scores

## 📁 Project Structure (Monorepo)

Based on [FastAPI Full-Stack Template](https://github.com/fastapi/full-stack-fastapi-template).

```
IELTS_WRITING_AI/
├── .env                           # Root environment variables
├── .gitignore                     # Git ignore rules
├── .pre-commit-config.yaml        # Code quality hooks
├── .github/workflows/             # CI/CD pipelines
├── package.json                   # Monorepo scripts
├── pyproject.toml                 # Python workspace config
├── compose.yml                    # Docker Compose (production)
├── compose.override.yml           # Docker Compose (development)
├── scripts/                       # Utility scripts
│   ├── test.sh
│   ├── lint.sh
│   ├── format.sh
│   └── prestart.sh
│
├── backend/
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── alembic.ini                # Database migrations config
│   ├── tests/
│   │   ├── conftest.py
│   │   └── test_auth.py
│   └── app/
│       ├── main.py                # FastAPI application
│       ├── models.py              # SQLModel models (User, Essay)
│       ├── crud.py                # CRUD operations
│       ├── utils.py               # Utility functions
│       ├── initial_data.py        # Seed data script
│       ├── api/
│       │   ├── main.py            # Router aggregation
│       │   ├── deps.py            # Dependencies (auth, db)
│       │   └── routes/
│       │       ├── auth.py        # /api/v1/auth/*
│       │       ├── users.py       # /api/v1/users/*
│       │       └── writing.py     # /api/v1/writing/*
│       ├── core/
│       │   ├── config.py          # Pydantic Settings
│       │   ├── db.py              # Database engine
│       │   └── security.py        # JWT & password hashing
│       └── alembic/
│           └── versions/          # Migration files
│
└── frontend/
    ├── Dockerfile
    ├── package.json
    └── src/
        ├── components/
        │   ├── Auth/              # Login/Register
        │   ├── Chat/              # Chat interface
        │   └── ui/                # Radix UI components
        ├── services/
        │   ├── api.jsx            # API client with auth
        │   └── auth.jsx           # Authentication context
        └── pages/
```

## 🔧 API Endpoints

All endpoints are prefixed with `/api/v1`

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | User registration |
| POST | `/api/v1/auth/login` | Get access token (OAuth2) |
| GET | `/api/v1/auth/me` | Get current user |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/users/` | List users (paginated) |
| GET | `/api/v1/users/{id}` | Get user by ID |
| PATCH | `/api/v1/users/me` | Update current user |
| DELETE | `/api/v1/users/{id}` | Delete user |

### Writing Evaluation
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/writing/evaluate` | Evaluate essay (uses 1 credit) |
| GET | `/api/v1/writing/essays` | Get user's essays |
| GET | `/api/v1/writing/essays/{id}` | Get specific essay |
| DELETE | `/api/v1/writing/essays/{id}` | Delete essay |

### Payment (SSLCommerz) - TODO
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/payment/initiate` | Initiate payment |
| POST | `/api/v1/payment/success` | Payment success callback |
| GET | `/api/v1/payment/history` | Payment history |

## 📊 IELTS Evaluation Criteria

The system evaluates essays based on official IELTS criteria:

1. **Task Achievement/Response** (25%)
   - Addresses all parts of the task
   - Clear position and relevant ideas
   - Appropriate word count

2. **Coherence and Cohesion** (25%)
   - Logical organization
   - Clear paragraphing
   - Effective linking words

3. **Lexical Resource** (25%)
   - Range of vocabulary
   - Accuracy and appropriateness
   - Natural collocations

4. **Grammatical Range and Accuracy** (25%)
   - Variety of structures
   - Accuracy of grammar
   - Punctuation and spelling

## 🔄 LangGraph Workflow

The evaluation process uses a structured LangGraph workflow:

```
Essay Input → Preprocessing → Parallel Evaluation → Score Calculation → Final Feedback
                               ├─ Task Achievement
                               ├─ Coherence & Cohesion
                               ├─ Lexical Resource
                               └─ Grammatical Accuracy
```

## 🎨 Modular Configuration

### Payment Providers
```python
# Easy to switch payment providers
PAYMENT_PROVIDER = "sslcommerz"  # or "stripe", "razorpay", etc.
```

### Multi-LLM Configuration (LangGraph)
```python
# LangGraph supports multiple LLM providers
LLM_PROVIDERS = {
    "openai": {
        "models": ["gpt-4", "gpt-3.5-turbo"],
        "api_key": "OPENAI_API_KEY"
    },
    "google": {
        "models": ["gemini-pro", "gemini-1.5-pro"],
        "api_key": "GOOGLE_API_KEY"
    }
}

# Single LLM for complete evaluation
EVALUATION_CONFIG = {
    "provider": "ollama",           # or "openai", "anthropic", "google"
    "model": "llama2",              # or "gpt-4", "claude-3-sonnet", "gemini-pro"
    "evaluation_mode": "comprehensive"  # Single comprehensive evaluation
}
```

### Multi-tenant Support
```python
# White-label configuration
TENANT_CONFIG = {
    "brand_name": "IELTS AI",
    "theme_colors": {...},
    "pricing_plans": {...}
}
```

## 💰 Pricing Structure

```python
CREDIT_PACKAGES = {
    "basic": {"credits": 5, "price": 500},      # 5 evaluations for 500 BDT
    "standard": {"credits": 15, "price": 1200}, # 15 evaluations for 1200 BDT
    "premium": {"credits": 30, "price": 2000}   # 30 evaluations for 2000 BDT
}
```

## ⚙️ Environment Variables

All environment variables are defined in the root `.env` file:

```bash
# Database (PostgreSQL)
DATABASE_URL=postgresql://postgres:1234@localhost:5432/ielts_db

# Security
SECRET_KEY=your-secret-key-min-32-chars
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]

# LLM Providers
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...
DEFAULT_LLM_PROVIDER=ollama
DEFAULT_LLM_MODEL=llama2

# LangSmith (optional)
LANGSMITH_TRACING=true
LANGCHAIN_API_KEY=...

# Payment - SSLCommerz
SSLCOMMERZ_STORE_ID=...
SSLCOMMERZ_STORE_PASSWORD=...
SSLCOMMERZ_IS_SANDBOX=true

# Frontend
VITE_API_URL=http://localhost:8000
```

## 🧪 Testing

```bash
# Run all backend tests
npm run test:backend

# Or directly with pytest
cd backend && uv run pytest -v

# With coverage
uv run pytest --cov=app
```

## 🚀 Deployment

### Docker Compose (Recommended)

```bash
# Production
docker compose up -d

# View logs
docker compose logs -f backend
```

### Manual Deployment

1. Set up PostgreSQL database
2. Configure `.env` with production values
3. Run migrations: `cd backend && uv run alembic upgrade head`
4. Seed data: `uv run python -m app.initial_data`
5. Start backend: `uv run uvicorn app.main:app --host 0.0.0.0`
6. Build frontend: `cd frontend && npm run build`
7. Serve with nginx

## 📄 License

MIT License

