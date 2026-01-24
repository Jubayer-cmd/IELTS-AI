"""
SQLModel models for database tables and Pydantic schemas.

Following FastAPI full-stack template pattern:
- Database models (table=True)
- Request/Response schemas
- All in one file for simplicity
"""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field as PydanticField
from sqlmodel import SQLModel, Field, Relationship


# ═══════════════════════════════════════════════════════════════
# USER MODELS
# ═══════════════════════════════════════════════════════════════

class UserBase(SQLModel):
    """Shared user properties."""
    name: str = Field(max_length=255)
    email: str = Field(unique=True, index=True, max_length=255)


class User(UserBase, table=True):
    """User database model."""
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    credits: int = Field(default=3)  # Free trial credits
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    essays: list["Essay"] = Relationship(back_populates="user")


class UserCreate(SQLModel):
    """Schema for user registration."""
    name: str
    email: str
    password: str


class UserUpdate(SQLModel):
    """Schema for updating user."""
    name: str | None = None
    email: str | None = None
    password: str | None = None


class UserUpdateMe(SQLModel):
    """Schema for user updating their own profile."""
    name: str | None = None
    email: str | None = None


class UserPublic(UserBase):
    """Public user data (API response)."""
    id: int
    is_active: bool
    credits: int
    created_at: datetime


class UsersPublic(SQLModel):
    """Paginated list of users."""
    data: list[UserPublic]
    count: int


# ═══════════════════════════════════════════════════════════════
# ESSAY MODELS
# ═══════════════════════════════════════════════════════════════

class TaskType(str, Enum):
    """IELTS writing task types."""
    TASK1 = "task1"  # Describe visual information
    TASK2 = "task2"  # Essay writing


class EssayBase(SQLModel):
    """Shared essay properties."""
    text: str = Field(min_length=1)
    task_type: TaskType = Field(default=TaskType.TASK2)
    word_limit: int = Field(default=250, ge=100, le=500)


class Essay(EssayBase, table=True):
    """Essay database model."""
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    word_count: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Scores (nullable until evaluated)
    overall_score: float | None = None
    task_achievement: float | None = None
    coherence: float | None = None
    lexical: float | None = None
    grammar: float | None = None
    feedback: str | None = None

    # Relationships
    user: User = Relationship(back_populates="essays")


class EssayCreate(SQLModel):
    """Schema for submitting an essay."""
    text: str = Field(min_length=1)
    task_type: TaskType = Field(default=TaskType.TASK2)
    word_limit: int = Field(default=250, ge=100, le=500)


class EssayPublic(EssayBase):
    """Public essay data (API response)."""
    id: int
    user_id: int
    word_count: int
    created_at: datetime
    overall_score: float | None
    task_achievement: float | None
    coherence: float | None
    lexical: float | None
    grammar: float | None
    feedback: str | None


class EssaysPublic(SQLModel):
    """Paginated list of essays."""
    data: list[EssayPublic]
    count: int


# ═══════════════════════════════════════════════════════════════
# EVALUATION SCHEMAS (Request/Response only, not DB models)
# ═══════════════════════════════════════════════════════════════

class BandScore(BaseModel):
    """IELTS band score breakdown."""
    task_achievement: float = PydanticField(ge=0, le=9)
    coherence: float = PydanticField(ge=0, le=9)
    lexical: float = PydanticField(ge=0, le=9)
    grammar: float = PydanticField(ge=0, le=9)


class EvaluationRequest(BaseModel):
    """Request to evaluate an essay."""
    text: str = PydanticField(min_length=1)
    task_type: TaskType = TaskType.TASK2
    word_limit: int = PydanticField(default=250, ge=100, le=500)


class EvaluationResponse(BaseModel):
    """Essay evaluation result."""
    word_count: int
    overall_score: float
    band_scores: BandScore
    feedback: str | None = None


# ═══════════════════════════════════════════════════════════════
# AUTH SCHEMAS
# ═══════════════════════════════════════════════════════════════

class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """JWT token payload."""
    sub: int | None = None
    email: str | None = None


class NewPassword(BaseModel):
    """Password change request."""
    token: str
    new_password: str


# ═══════════════════════════════════════════════════════════════
# GENERIC SCHEMAS
# ═══════════════════════════════════════════════════════════════

class Message(BaseModel):
    """Generic message response."""
    message: str
