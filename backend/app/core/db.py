"""
Database configuration and session management.

Following FastAPI full-stack template pattern.
"""
from sqlmodel import SQLModel, create_engine, Session

from app.core.config import settings

# Create engine from settings (PostgreSQL)
engine = create_engine(
    str(settings.DATABASE_URL),
    echo=False,  # Set to True for SQL debugging
    pool_pre_ping=True,  # Verify connections before use
)


def init_db() -> None:
    """
    Initialize database tables.

    Called on application startup.
    In production, use Alembic migrations instead.
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Database session generator for dependency injection.

    Usage:
        @router.get("/items")
        def get_items(session: Session = Depends(get_session)):
            ...
    """
    with Session(engine) as session:
        yield session
