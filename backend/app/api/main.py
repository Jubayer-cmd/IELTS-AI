"""
API Router aggregation.

Import and include your route modules here.
"""

from fastapi import APIRouter

from app.api.routes import auth, chat

api_router = APIRouter()

# Auth routes: /api/v1/auth/register, /api/v1/auth/login, /api/v1/auth/me
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Chat routes: /api/v1/chat/threads, /api/v1/chat/threads/{id}/messages
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
