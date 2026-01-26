"""
Utility functions.
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

    TODO: Implement with actual email service (SendGrid, AWS SES, etc.)
    """
    logger.info(f"Would send email to {email_to} with subject: {subject}")
