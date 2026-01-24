from sqlmodel import SQLModel, Field
from datetime import datetime

class User(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  first_name: str = Field(index=True, nullable=False)
  last_name: str = Field(index=True, nullable=False)
  email: str = Field(index=True, nullable=False, unique=True)
  hashed_password: str = Field(nullable=False)
  is_active: bool = Field(default=True, nullable=False)
  is_superuser: bool = Field(default=False, nullable=False)
  created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
  updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
  credits : int = Field(default=50, nullable=False)

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
  is_superuser: bool
  created_at: datetime
  updated_at: datetime
  credits : int

class UserUpdate(SQLModel):
  first_name: str | None = None
  last_name: str | None = None
  email: str | None = None
  password: str | None = None
  is_active: bool | None = None
  is_superuser: bool | None = None
  credits : int | None = None


class Token(SQLModel):
  access_token: str
  token_type: str = "bearer"