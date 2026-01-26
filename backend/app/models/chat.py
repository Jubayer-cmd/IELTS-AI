"""
Chat models for Thread and Message persistence.

These models integrate with LangGraph's conversation history
while providing database persistence for the frontend chat UI.
"""

from datetime import datetime, timezone
from typing import TYPE_CHECKING
from models.common import utc_now
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.users import User



# ═══════════════════════════════════════════════════════════════
# DATABASE MODELS (table=True)
# ═══════════════════════════════════════════════════════════════


class Thread(SQLModel, table=True):
    """
    A conversation thread owned by a user.

    Maps to LangGraph's thread_id for checkpoint persistence.
    Each thread contains multiple messages and belongs to one user.
    """

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True, nullable=False)
    title: str | None = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=utc_now, nullable=False)
    updated_at: datetime = Field(default_factory=utc_now, nullable=False)

    # Relationships
    user: "User" = Relationship(back_populates="threads")
    messages: list["ChatMessage"] = Relationship(
        back_populates="thread",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class ChatMessage(SQLModel, table=True):
    """
    A single message in a conversation thread.

    Stores both user messages and AI responses for chat history display.
    """

    __tablename__: str = "chat_message"  # type: ignore[assignment]

    id: int | None = Field(default=None, primary_key=True)
    thread_id: int = Field(foreign_key="thread.id", index=True, nullable=False)

    role: str = Field(default="user", max_length=20, nullable=False)
    message_type: str = Field(default="text", max_length=32, nullable=False)
    content: str = Field(nullable=False)
    evaluation: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=utc_now, index=True, nullable=False)
    updated_at: datetime = Field(default_factory=utc_now, nullable=False)

    # Relationship
    thread: Thread = Relationship(back_populates="messages")


# ═══════════════════════════════════════════════════════════════
# PYDANTIC SCHEMAS (for API requests/responses)
# ═══════════════════════════════════════════════════════════════


class ThreadCreate(SQLModel):
    """Schema for creating a new thread."""

    title: str | None = None


class ThreadPublic(SQLModel):
    """Schema for thread API responses."""

    id: int
    title: str | None
    created_at: datetime
    updated_at: datetime


class ChatMessageCreate(SQLModel):
    """Schema for creating a new message."""

    content: str


class ChatMessagePublic(SQLModel):
    """Schema for message API responses."""

    id: int
    thread_id: int
    role: str
    message_type: str
    content: str
    evaluation: str | None
    created_at: datetime
