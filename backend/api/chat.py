from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional

from core.database import get_db
from services.ielts_evaluator import IELTSEvaluator

router = APIRouter(prefix='/chat', tags=['chat'])

# Initialize IELTS Evaluator
evaluator = IELTSEvaluator()

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    message: str

@router.post('/message', response_model=ChatResponse)
async def send_message(
    chat_input: ChatMessage,
    db: Session = Depends(get_db)
):
    """Send a message and get response"""
    try:
        response = await evaluator.chat(chat_input.message)
        return ChatResponse(message=response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Chat error: {str(e)}')