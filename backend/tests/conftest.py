"""
Pytest configuration and fixtures.
"""

import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.api.deps import get_db
from app.main import app

# Use PostgreSQL for tests (same as production)
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL", "postgresql://postgres:1234@localhost:5432/ielts_test"
)


@pytest.fixture(name="session")
def session_fixture() -> Generator[Session, None, None]:
    """Create a fresh database session for each test."""
    engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
def client_fixture(session: Session) -> Generator[TestClient, None, None]:
    """Create a test client with database override."""

    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
