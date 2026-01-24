# User Learning Profile

## Learning Status
- **Level:** Beginner
- **Approach:** Learning by building from scratch

## Technologies Learning (in order)

### ✅ COMPLETED: FastAPI + Pydantic (Basics)

### 📋 LEARN WHEN NEEDED: FastAPI (Advanced)
- File uploads (UploadFile) → when adding essay image feature
- Authentication (OAuth2, JWT) → when adding user accounts
- WebSockets → when building speaking test
- Background tasks → when AI processing takes long
- Status codes (201, 204) → when polishing REST API
- Testing (TestClient) → before deployment

### 📋 LEARN WHEN NEEDED: Pydantic (Advanced)
- model_validator → when validating related fields
- model_dump() / model_validate() → when working with database
- Computed fields → when needing auto-calculated values
- Field aliases → when frontend needs different names

### ✅ COMPLETED: FastAPI + Pydantic (Basics)
**Routes & Endpoints:**
- GET, POST, PUT, DELETE routes
- Path parameters (`/essay/{id}`)
- Query parameters (`?timed=true`)
- Routers (organizing code in `api/` folder)
- Response models (`response_model=`)
- HTTPException (error handling)
- Depends (dependency injection)
- CORS middleware

**Pydantic:**
- BaseModel
- Optional fields
- Field() validation (min_length, ge, etc.)
- Nested models (BandScore inside EvaluationResponse)
- field_validator (custom validation)
- Enum (TaskType for fixed choices)

### ✅ COMPLETED: SQLAlchemy Basics
**Learned:**
- `create_engine()` - Database connection
- `declarative_base()` - Parent for models
- `sessionmaker()` - Create sessions
- `Column()`, `Integer`, `String` - Define columns
- `db.add()`, `db.commit()`, `db.refresh()` - Save data
- `db.query().all()`, `db.query().filter().first()` - Read data
- `db.delete()` - Remove data

### ✅ COMPLETED: SQLModel (Primary ORM)
**Learned:**
- `SQLModel` - Combines Pydantic + SQLAlchemy
- `table=True` - Marks class as database table
- `Field()` - Define column properties
- `Session(engine)` - Context manager for sessions
- `db.exec(select(Model)).all()` - Read all
- `db.get(Model, id)` - Read one by ID
- Inheritance pattern: `UserBase` → `User`, `UserCreate`, `UserUpdate`

### ✅ COMPLETED: CRUD Operations
- **C**reate: `POST /users/` with `db.add()`
- **R**ead: `GET /users/` and `GET /users/{id}`
- **U**pdate: `PATCH /users/{id}` with optional fields
- **D**elete: `DELETE /users/{id}` with `db.delete()`

### 🔄 NEXT TO LEARN:
5. **Relationships** - Foreign keys, User → Essays (optional, learn when needed)
6. **LangChain** - AI building blocks (before LangGraph)
7. **LangGraph** - AI workflow orchestration
8. **Prompt Engineering** - Writing effective AI prompts
9. **Async/Await** - Handle many requests efficiently

## Project: IELTS Mock Test App
- **Features:** Writing + Speaking tests
- **User System:** Simple accounts (save history, track progress)

## Important Guidelines
- ❌ DO NOT write code for the user
- ❌ DO NOT create files automatically
- ✅ Explain concepts clearly
- ✅ Give guidance and direction
- ✅ Let user practice by writing code themselves
- ✅ Review their code and give feedback
- ✅ Provide hints when stuck

## Current Status
- Starting fresh backend from scratch
- Building step-by-step while learning
- Keep: .env, .venv, folder structure
- User writes all code themselves
