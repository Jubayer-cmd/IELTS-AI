from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import Optional, List
from datetime import datetime

from core.database import get_db
from core.config import settings
from services.llm import IELTSConversationalAI
from models.chat import Thread, Message

router = APIRouter(prefix='/chat', tags=['chat'])

# Initialize IELTS Conversational AI
def get_evaluator():
    if not settings.google_api_key:
        raise HTTPException(status_code=500, detail="Google API key not configured")
    return IELTSConversationalAI(google_api_key=settings.google_api_key)

evaluator = None
try:
    evaluator = get_evaluator()
except Exception as e:
    print(f"Warning: Failed to initialize IELTS AI: {e}")

# Pydantic Models
class ThreadCreate(BaseModel):
    title: Optional[str] = "New Chat"

class ThreadResponse(BaseModel):
    id: int
    title: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

class ChatMessage(BaseModel):
    message: str
    image_data: Optional[str] = None
    conversation_state: str = "greeting"
    user_id: Optional[str] = None

class EvaluationData(BaseModel):
    overall_band_score: Optional[float] = None
    task_achievement_score: Optional[float] = None
    coherence_cohesion_score: Optional[float] = None
    lexical_resource_score: Optional[float] = None
    grammatical_accuracy_score: Optional[float] = None
    detailed_feedback: Optional[dict] = None
    word_count: Optional[int] = None
    task_type: Optional[str] = None
    question: Optional[str] = None

class ChatResponse(BaseModel):
    message: str
    should_deduct_credit: bool
    conversation_state: str
    user_intent: str
    evaluation_data: Optional[EvaluationData] = None

# Thread Endpoints
@router.post('/threads', response_model=ThreadResponse)
def create_thread(thread_data: ThreadCreate, db: Session = Depends(get_db)):
    # TODO: Get actual user_id from auth
    user_id = "default_user"
    new_thread = Thread(title=thread_data.title, user_id=user_id)
    db.add(new_thread)
    db.commit()
    db.refresh(new_thread)
    return new_thread

@router.get('/threads', response_model=List[ThreadResponse])
def get_threads(db: Session = Depends(get_db)):
    # TODO: Filter by user_id
    user_id = "default_user"
    threads = db.query(Thread).filter(Thread.user_id == user_id).order_by(Thread.updated_at.desc()).all()
    return threads

@router.delete('/threads/{thread_id}')
def delete_thread(thread_id: int, db: Session = Depends(get_db)):
    """Delete a thread and all its messages"""
    thread = db.query(Thread).filter(Thread.id == thread_id).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    db.delete(thread)
    db.commit()
    return {"message": "Thread deleted successfully"}

@router.get('/threads/{thread_id}/messages', response_model=List[MessageResponse])
def get_thread_messages(thread_id: int, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.thread_id == thread_id).order_by(Message.created_at.asc()).all()
    return messages

@router.post('/threads/{thread_id}/messages', response_model=ChatResponse)
async def send_message_to_thread(
    thread_id: int,
    chat_input: ChatMessage,
    db: Session = Depends(get_db)
):
    """Send a message to a specific thread and get response"""
    try:
        if not evaluator:
            raise HTTPException(status_code=500, detail="IELTS AI not initialized")
        
        thread = db.query(Thread).filter(Thread.id == thread_id).first()
        if not thread:
            raise HTTPException(status_code=404, detail="Thread not found")

        # Save user message
        user_msg = Message(thread_id=thread_id, role="user", content=chat_input.message)
        db.add(user_msg)
        
        # Get response from AI
        user_id = chat_input.user_id or "default_user"
        response = await evaluator.chat(
            user_message=chat_input.message,
            image_data=chat_input.image_data,
            user_id=user_id,
            conversation_state=chat_input.conversation_state
        )
        
        # Save assistant message
        assistant_msg = Message(thread_id=thread_id, role="assistant", content=response["response"])
        db.add(assistant_msg)
        
        # Update thread timestamp and title if it's the first message
        thread.updated_at = func.now()
        # Simple title generation if title is "New Chat" and it's the first user message
        if thread.title == "New Chat":
             # Take first 30 chars of message
             thread.title = chat_input.message[:30] + "..." if len(chat_input.message) > 30 else chat_input.message
        
        db.commit()
        
        # Convert evaluation_data
        evaluation_data = None
        if response.get("evaluation_data"):
            evaluation_data = EvaluationData(**response["evaluation_data"])
        
        return ChatResponse(
            message=response["response"],
            should_deduct_credit=response["should_deduct_credit"],
            conversation_state=response["conversation_state"],
            user_intent=response["user_intent"],
            evaluation_data=evaluation_data
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f'Chat error: {str(e)}')

# Keep the old endpoint for backward compatibility if needed, or remove it. 
# For now, I'll leave it but it won't save to a thread unless we modify it.
# Actually, let's remove it to force usage of threads, or update it to create a temp thread?
# The user wants dynamic sidebar, so they likely want persistence.
# I will remove the old /message endpoint to avoid confusion, as the new flow is thread-based.