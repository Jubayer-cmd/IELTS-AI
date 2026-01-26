"""
Security utilities for password hashing and JWT tokens.

Uses bcrypt directly (more reliable than passlib with newer Python).
"""

from datetime import datetime, timedelta, timezone

import bcrypt
from jose import jwt

from app.core.config import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.

    Args:
        plain_password: The password user entered
        hashed_password: The hash stored in database

    Returns:
        True if password matches, False otherwise
    """
    # bcrypt needs bytes, not strings
    password_bytes = plain_password.encode("utf-8")
    hash_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hash_bytes)


def get_password_hash(password: str) -> str:
    """
    Hash a password for storing in database.

    Args:
        password: Plain text password

    Returns:
        Bcrypt hash string
    """
    # bcrypt needs bytes
    password_bytes = password.encode("utf-8")
    # Generate salt and hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    # Return as string for database storage
    return hashed.decode("utf-8")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: Payload to encode (should include 'sub' for user_id)
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt
