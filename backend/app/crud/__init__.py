"""
CRUD package.

Re-exports all CRUD operations for convenient imports:
    from app import crud
    crud.create_user(...)
    crud.create_thread(...)
"""

# User operations
from app.crud.user import (
    authenticate_user,
    create_user,
    get_user_by_email,
    get_user_by_id,
    update_user,
)

# Chat operations
from app.crud.chat import (
    create_message,
    create_thread,
    delete_thread,
    get_messages_by_thread,
    get_thread_by_id,
    get_thread_message_count,
    get_threads_by_user,
    update_thread_timestamp,
    update_thread_title,
)

__all__ = [
    # User
    "get_user_by_email",
    "get_user_by_id",
    "create_user",
    "authenticate_user",
    "update_user",
    # Chat - Threads
    "create_thread",
    "get_thread_by_id",
    "get_thread_message_count",
    "get_threads_by_user",
    "delete_thread",
    "update_thread_timestamp",
    "update_thread_title",
    # Chat - Messages
    "create_message",
    "get_messages_by_thread",
]
