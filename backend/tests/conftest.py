"""
Pytest configuration and fixtures.

Following FastAPI full-stack template pattern.
"""
import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.main import app
from app.api.deps import get_db
from app.models import User
from app.core.security import get_password_hash


# Use PostgreSQL for tests (same as production)
# Falls back to in-memory SQLite if TEST_DATABASE_URL not set
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://postgres:1234@localhost:5432/ielts_test"
)


@pytest.fixture(name="session")
def session_fixture() -> Generator[Session, None, None]:
    """Create a fresh database session for each test."""
    engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
    SQLModel.metadata.drop_all(engine)  # Clean slate
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)  # Cleanup after


@pytest.fixture(name="client")
def client_fixture(session: Session) -> Generator[TestClient, None, None]:
    """Create a test client with database override."""
    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(session: Session) -> User:
    """Create a test user."""
    user = User(
        name="Test User",
        email="test@example.com",
        hashed_password=get_password_hash("testpass123"),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
