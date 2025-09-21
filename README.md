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
- **Frontend**: React 18 + Vite + TypeScript
- **Backend**: FastAPI + Python 3.11+
- **AI Framework**: LangGraph + LangChain 
- **Package Manager**: UV (Python)
- **Database**: SQLite (MVP) → PostgreSQL (Production)

### System Design
```
React Frontend ──► FastAPI Backend ──► LangGraph Workflow ──► Multi-LLM AI
       │                   │                   │                    │
       │                   ▼                   ▼                    │
       │            SQLite Database    State Management            │
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

### **DATABASE MODELS (SQLAlchemy)**
```python
# Essential database tables to create:

class User:
    id, email, password_hash, credits, created_at

class Essay:
    id, user_id, content, task_type, word_count, created_at

class Evaluation:
    id, essay_id, overall_band_score, task_achievement_score, 
    coherence_score, lexical_score, grammar_score, feedback_json, created_at

class Payment:
    id, user_id, amount, credits_purchased, sslcommerz_transaction_id, status
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
- Python 3.11+
- Node.js 18+
- LLM Provider API key (OpenAI, Anthropic, Google, or local Ollama)
- SSLCommerz merchant account

### Setup & Run

```bash
# Backend Setup
mkdir backend && cd backend
uv init
uv add fastapi uvicorn langgraph langchain-openai langchain-google-genai sqlalchemy pydantic python-multipart bcryptx python-jose sslcommerz-python

# Environment Configuration
cat > .env << EOF
# LLM Provider Keys (add at least one)
OPENAI_API_KEY=your_openai_api_key_optional
ANTHROPIC_API_KEY=your_anthropic_api_key_optional
GOOGLE_API_KEY=your_google_api_key_optional
OLLAMA_BASE_URL=http://localhost:11434

# Payment Integration
SSLCOMMERZ_STORE_ID=your_store_id
SSLCOMMERZ_STORE_PASSWORD=your_store_password
SSLCOMMERZ_IS_SANDBOX=true

# Application Config
JWT_SECRET_KEY=your_jwt_secret
DATABASE_URL=sqlite:///./app.db
DEFAULT_LLM_PROVIDER=ollama
DEFAULT_LLM_MODEL=llama2
EOF

# Run Backend
uv run uvicorn main:app --reload

# Frontend Setup (new terminal)
cd ..
npm create vite@latest frontend -- --template react
cd frontend
npm install axios react-router-dom shadcn-ui lucide-react

# Run Frontend
npm run dev
```

### Access
- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Usage
1. Register/Login to get credits
2. Purchase evaluation credits via SSLCommerz
3. Submit IELTS essay for evaluation
4. Get instant AI feedback and band scores from multiple LLMs

## 📁 Project Structure

```
IELTS_WRITING_AI/
├── backend/
│   ├── main.py                    # FastAPI application
│   ├── core/
│   │   ├── config.py              # Environment configuration
│   │   ├── security.py            # JWT authentication
│   │   └── database.py            # Database connection
│   ├── services/
│   │   ├── ielts_evaluator.py     # LangGraph evaluation
│   │   ├── payment_service.py     # SSLCommerz integration
│   │   └── user_service.py        # User management
│   ├── models/
│   │   ├── user.py                # User database models
│   │   ├── payment.py             # Payment models
│   │   └── evaluation.py          # Essay evaluation models
│   ├── api/
│   │   ├── auth.py                # Authentication endpoints
│   │   ├── payment.py             # Payment endpoints
│   │   └── evaluation.py          # Evaluation endpoints
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Auth/              # Login/Register
│   │   │   ├── Payment/           # Credit purchase
│   │   │   ├── Evaluation/        # Essay evaluation
│   │   │   └── Dashboard/         # User dashboard
│   │   ├── services/
│   │   │   ├── api.js             # API client
│   │   │   ├── auth.js            # Authentication
│   │   │   └── payment.js         # Payment handling
│   │   └── App.jsx
│   └── package.json
└── README.md
```

## 🔧 API Endpoints

### Authentication
```
POST /auth/register    # User registration
POST /auth/login       # User login
GET  /auth/me          # Get current user
```

### Payment (SSLCommerz)
```
POST /payment/initiate     # Initiate payment
POST /payment/success      # Payment success callback
POST /payment/cancel       # Payment cancel callback
GET  /payment/history      # Payment history
```

### Evaluation
```
POST /evaluate             # Evaluate essay (requires credits)
GET  /evaluations          # User's evaluation history
GET  /evaluations/{id}     # Specific evaluation details
```

### User Management
```
GET  /user/credits         # Check credit balance
GET  /user/dashboard       # User dashboard data
```

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

