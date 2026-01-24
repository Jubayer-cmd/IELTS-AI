# User Learning Profile

## Learning Status
- **Level:** Beginner → Building Real Project
- **Approach:** Learn by building IELTS Writing AI app
- **Mode:** Teach + Build simultaneously

## Project: IELTS Writing Feedback AI
**Goal:** Users submit IELTS essays → Get AI band scores (1-9) + feedback
**Stack:** FastAPI + SQLModel + PostgreSQL + LangGraph + React
**Payment:** SSLCommerz (credit-based, 50 BDT per evaluation)

## Architecture (Updated)
```
backend/app/
├── main.py           # FastAPI app with lifespan
├── core/
│   ├── config.py     # Pydantic Settings (.env)
│   ├── db.py         # SQLModel engine
│   └── security.py   # JWT + bcrypt
├── models/           # SQLModel models
├── api/
│   ├── deps.py       # SessionDep, auth deps
│   ├── main.py       # Router aggregation
│   └── routes/       # Endpoint files
└── alembic/          # Database migrations
```

## ✅ COMPLETED
- FastAPI basics (routes, routers, Depends, CORS)
- Pydantic validation (BaseModel, Field, Optional, Enum)
- SQLAlchemy basics (engine, session, CRUD)
- SQLModel (combined Pydantic + SQLAlchemy)
- CRUD operations (Create, Read, Update, Delete)
- Professional project structure

## 🔄 CURRENT: Building Real Features
1. **User Model** ← NOW
2. **Authentication** (JWT + bcrypt)
3. **Essay Model** (with relationships)
4. **Alembic** (database migrations)
5. **LangGraph** (AI evaluation workflow)

## 📋 TO LEARN (as needed)
- **Alembic** - Database migrations (user is new to this)
- **Relationships** - Foreign keys (User → Essays)
- **LangChain/LangGraph** - AI workflows
- **JWT Authentication** - Secure API
- **File uploads** - Image-based essay input
- **SSLCommerz** - Payment integration

## Important Guidelines
- ❌ DO NOT write code for the user
- ✅ Explain concepts clearly
- ✅ Give guidance and direction
- ✅ Let user practice by writing code themselves
- ✅ Review their code and give feedback
- ✅ Build real project features while learning
