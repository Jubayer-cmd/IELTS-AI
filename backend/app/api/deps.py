"""
API Dependencies.

Reusable dependencies for FastAPI route handlers.
"""
from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.core.db import engine


def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency.

    Yields a SQLModel session and ensures cleanup after request.

    Usage:
        @router.get("/items")
        def get_items(session: SessionDep):
            ...
    """
    with Session(engine) as session:
        yield session


# Type alias for cleaner dependency injection
SessionDep = Annotated[Session, Depends(get_db)]
