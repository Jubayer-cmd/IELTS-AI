"""
Utility functions.

Following FastAPI full-stack template pattern.
"""
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_email(
    email_to: str,
    subject: str,
    html_content: str,
) -> None:
    """
    Send an email.

    TODO: Implement with actual email service.
    """
    logger.info(f"Would send email to {email_to} with subject: {subject}")
    # For now, just log
    pass


def generate_password_reset_token(email: str) -> str:
    """Generate a password reset token."""
    from app.core.security import create_access_token
    from datetime import timedelta

    return create_access_token(
        data={"sub": email, "type": "reset"},
        expires_delta=timedelta(hours=1)
    )


def verify_password_reset_token(token: str) -> str | None:
    """Verify a password reset token and return email."""
    from jose import JWTError, jwt
    from app.core.config import settings

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        if payload.get("type") != "reset":
            return None
        return payload.get("sub")
    except JWTError:
        return None
