from datetime import datetime
from typing import TYPE_CHECKING
from models.common import _utc_now
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.chat import Thread


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    first_name: str = Field(index=True, nullable=False)
    last_name: str = Field(index=True, nullable=False)
    email: str = Field(index=True, nullable=False, unique=True)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    is_verified: bool = Field(default=False)
    is_superuser: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default_factory=_utc_now, nullable=False)
    updated_at: datetime = Field(default_factory=_utc_now, nullable=False)
    credits: int = Field(default=50, nullable=False)

    # Relationships
    threads: list["Thread"] = Relationship(back_populates="user")


class UserCreate(SQLModel):
    first_name: str
    last_name: str
    email: str
    password: str


class UserPublic(SQLModel):
    id: int | None
    first_name: str
    last_name: str
    email: str
    is_active: bool
    is_verified: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
    credits: int


class UserUpdate(SQLModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    password: str | None = None
    is_active: bool | None = None
    is_verified: bool | None = None
    is_superuser: bool | None = None
    credits: int | None = None


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"
