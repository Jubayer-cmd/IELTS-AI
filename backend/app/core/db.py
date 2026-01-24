"""
Database configuration.
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
    # Import models so SQLModel registers them
    from app.models.users import User  # noqa: F401

    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Database session generator for dependency injection.
    """
    with Session(engine) as session:
        yield session
