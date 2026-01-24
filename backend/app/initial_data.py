"""
Initial data seeding script.

Run with: python -m app.initial_data
"""
import logging

from sqlmodel import Session, select

from app.core.db import engine, init_db
from app.core.security import get_password_hash
from app.models import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    """Initialize database with initial data."""
    init_db()

    with Session(engine) as session:
        # Check if superuser exists
        user = session.exec(
            select(User).where(User.email == "admin@ieltsai.com")
        ).first()

        if not user:
            # Create superuser
            user = User(
                name="Admin",
                email="admin@ieltsai.com",
                hashed_password=get_password_hash("admin123"),
                is_superuser=True,
                credits=999,
            )
            session.add(user)
            session.commit()
            logger.info("Created superuser: admin@ieltsai.com")
        else:
            logger.info("Superuser already exists")


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
