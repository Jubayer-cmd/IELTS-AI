# FastAPI main application entry point

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

# Import routers
from api import auth, payment, admin, chat
from core.database import Base, engine

# Import models to register them with SQLAlchemy
from models.chat import Thread, Message
from models.user import User
from models.essay import Essay
from models.payment import Payment
from models.evaluation import Evaluation

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="IELTS Writing Feedback AI", version="1.0.0")

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(payment.router)
app.include_router(admin.router)
app.include_router(chat.router)

@app.get("/")
async def root():
    return {"message": "IELTS Writing Feedback AI API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "IELTS Writing Feedback AI"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
