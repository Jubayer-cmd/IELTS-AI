"""
Initial data seeding script.

Run with: python -m app.initial_data
"""

import logging

from app.core.db import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    """Initialize database with initial data."""
    init_db()
    # Add your seed data here


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
