"""
Models package.

Add your models here and re-export them for convenient imports:
    from app.models import YourModel
"""

# Common schemas
# Chat models
from app.models.chat import (
    ChatMessage,
    ChatMessageCreate,
    ChatMessagePublic,
    Thread,
    ThreadCreate,
    ThreadPublic,
)
from app.models.common import Message

# User models
from app.models.users import Token, User, UserCreate, UserPublic, UserUpdate

__all__ = [
    # Common
    "Message",
    # User
    "User",
    "UserCreate",
    "UserPublic",
    "UserUpdate",
    "Token",
    # Chat
    "Thread",
    "ThreadCreate",
    "ThreadPublic",
    "ChatMessage",
    "ChatMessageCreate",
    "ChatMessagePublic",
]
