"""
Chat CRUD operations.

Handles thread and message persistence for the chat system.
"""

from datetime import datetime, timezone

from sqlalchemy import asc, desc
from sqlmodel import Session, select

from app.models.chat import ChatMessage, Thread, ThreadCreate


# ═══════════════════════════════════════════════════════════════
# THREAD CRUD
# ═══════════════════════════════════════════════════════════════


def create_thread(*, session: Session, user_id: int, thread_in: ThreadCreate) -> Thread:
    """Create a new conversation thread for a user."""
    db_thread = Thread(
        user_id=user_id,
        title=thread_in.title,
    )
    session.add(db_thread)
    session.commit()
    session.refresh(db_thread)
    return db_thread


def get_thread_by_id(*, session: Session, thread_id: int) -> Thread | None:
    """Get a thread by its ID."""
    return session.get(Thread, thread_id)


def get_threads_by_user(*, session: Session, user_id: int) -> list[Thread]:
    """Get all threads for a user, ordered by most recent first."""
    statement = (
        select(Thread)
        .where(Thread.user_id == user_id)
        .order_by(desc(Thread.updated_at))  # type: ignore[arg-type]
    )
    return list(session.exec(statement).all())


def delete_thread(*, session: Session, thread: Thread) -> None:
    """Delete a thread and all its messages (cascade)."""
    session.delete(thread)
    session.commit()


def update_thread_timestamp(*, session: Session, thread: Thread) -> None:
    """Update thread's updated_at timestamp (called when new message added)."""
    thread.updated_at = datetime.now(timezone.utc)
    session.add(thread)
    session.commit()


def update_thread_title(*, session: Session, thread: Thread, title: str) -> Thread:
    """Update thread's title (for auto-title generation)."""
    thread.title = title
    thread.updated_at = datetime.now(timezone.utc)
    session.add(thread)
    session.commit()
    session.refresh(thread)
    return thread


def get_thread_message_count(*, session: Session, thread_id: int) -> int:
    """Get the count of messages in a thread (to check if first message)."""
    statement = select(ChatMessage).where(ChatMessage.thread_id == thread_id)
    return len(list(session.exec(statement).all()))


# ═══════════════════════════════════════════════════════════════
# MESSAGE CRUD
# ═══════════════════════════════════════════════════════════════


def create_message(
    *,
    session: Session,
    thread_id: int,
    role: str,
    content: str,
    message_type: str = "text",
    evaluation: str | None = None,
) -> ChatMessage:
    """Create a new message in a thread."""
    db_message = ChatMessage(
        thread_id=thread_id,
        role=role,
        content=content,
        message_type=message_type,
        evaluation=evaluation,
    )
    session.add(db_message)
    session.commit()
    session.refresh(db_message)
    return db_message


def get_messages_by_thread(*, session: Session, thread_id: int) -> list[ChatMessage]:
    """Get all messages in a thread, ordered by creation time."""
    statement = (
        select(ChatMessage)
        .where(ChatMessage.thread_id == thread_id)
        .order_by(asc(ChatMessage.created_at))  # type: ignore[arg-type]
    )
    return list(session.exec(statement).all())
