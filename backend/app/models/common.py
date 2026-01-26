"""
Common/generic schemas.
"""
from datetime import datetime, timezone
from pydantic import BaseModel

def utc_now() -> datetime:
    """Return timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)
class Message(BaseModel):
    """Generic message response."""

    message: str
