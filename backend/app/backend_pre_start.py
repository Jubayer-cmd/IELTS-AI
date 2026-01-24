"""
Pre-start script for backend.

Waits for database to be ready before starting the app.
Used in Docker deployments.

Run with: python -m app.backend_pre_start
"""
import logging

from sqlalchemy import text
from sqlmodel import Session

from app.core.db import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60
wait_seconds = 1


def init() -> None:
    """Check database connection."""
    try:
        with Session(engine) as session:
            # Try simple query
            session.exec(text("SELECT 1"))
        logger.info("Database is ready!")
    except Exception as e:
        logger.error(f"Database not ready: {e}")
        raise


def main() -> None:
    logger.info("Checking database connection...")
    init()


if __name__ == "__main__":
    main()
