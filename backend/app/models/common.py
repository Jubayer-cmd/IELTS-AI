"""
Common/generic schemas.
"""

from pydantic import BaseModel


class Message(BaseModel):
    """Generic message response."""

    message: str
