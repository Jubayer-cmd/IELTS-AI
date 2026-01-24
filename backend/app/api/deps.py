"""
API Dependencies.

Reusable dependencies for FastAPI route handlers.
Following the FastAPI full-stack template pattern.
"""
from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlmodel import Session

from app.core.config import settings
from app.core.db import engine
from app.models import User


# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


class TokenPayload(BaseModel):
    """JWT token payload structure."""
    sub: int | None = None
    email: str | None = None


def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency.

    Yields a SQLModel session and ensures cleanup after request.
    """
    with Session(engine) as session:
        yield session


# Type alias for cleaner dependency injection
SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    """
    Validate JWT token and return current user.

    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenPayload(sub=user_id, email=payload.get("email"))
    except JWTError:
        raise credentials_exception

    user = session.get(User, token_data.sub)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return user


# Type alias for current user dependency
CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    """
    Validate that current user is a superuser.

    Note: Requires is_superuser field on User model.
    """
    if not getattr(current_user, 'is_superuser', False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user
