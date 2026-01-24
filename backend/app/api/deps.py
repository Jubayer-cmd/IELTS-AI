"""
API Dependencies.

Reusable dependencies for FastAPI route handlers.
"""
from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from jose import jwt, JWTError

from app.core.db import engine
from app.core.config import settings
from app.models.users import User


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Database Session Dependency
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency.

    Yields a SQLModel session and ensures cleanup after request.
    """
    with Session(engine) as session:
        yield session


# Type alias for cleaner dependency injection
SessionDep = Annotated[Session, Depends(get_db)]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Authentication Dependencies
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# OAuth2 scheme - tells FastAPI to look for "Authorization: Bearer <token>"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
TokenDep = Annotated[str, Depends(oauth2_scheme)]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    """
    Get current authenticated user from JWT token.

    Flow:
    1. Extract token from "Authorization: Bearer <token>" header
    2. Decode JWT to get payload {"sub": "user_id", "exp": ...}
    3. Fetch user from database using user_id
    4. Return user or raise 401 if invalid
    """
    try:
        # Decode the JWT token → get payload dictionary
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        # Get user_id from payload ("sub" = subject = user ID)
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError:
        # Token is invalid, expired, or tampered with
        raise HTTPException(status_code=401, detail="Invalid token")

    # Find user in database
    user = session.get(User, int(user_id))

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


# Type alias - use this in routes to get the logged-in user
CurrentUser = Annotated[User, Depends(get_current_user)]
