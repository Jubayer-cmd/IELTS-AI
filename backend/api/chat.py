from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional

from core.database import get_db
from core.config import settings
from services.llm import IELTSConversationalAI

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

class ChatMessage(BaseModel):
    message: str
    image_data: Optional[str] = None
    conversation_state: str = "greeting"
    user_id: Optional[str] = None  # Simple user identification

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

@router.post('/message', response_model=ChatResponse)
async def send_message(
    chat_input: ChatMessage,
    db: Session = Depends(get_db)
):
    """Send a message and get response"""
    try:
        if not evaluator:
            raise HTTPException(status_code=500, detail="IELTS AI not initialized. Check Google API key configuration.")
        
        # Use provided user_id or default to "default_user"
        user_id = chat_input.user_id or "default_user"
        
        response = await evaluator.chat(
            user_message=chat_input.message,
            image_data=chat_input.image_data,
            user_id=user_id,
            conversation_state=chat_input.conversation_state
        )
        
        # Convert evaluation_data to Pydantic model if present
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
        raise HTTPException(status_code=500, detail=f'Chat error: {str(e)}')