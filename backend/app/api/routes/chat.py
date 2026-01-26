"""
Chat API routes for thread and message management.

These endpoints integrate with the frontend chat UI and LangGraph agent.
"""

from fastapi import APIRouter, HTTPException

from app import crud
from app.api.deps import CurrentUser, SessionDep
from app.models.chat import (
    ChatMessageCreate,
    ChatMessagePublic,
    ThreadCreate,
    ThreadPublic,
)

router = APIRouter()


# ═══════════════════════════════════════════════════════════════
# THREAD ENDPOINTS
# ═══════════════════════════════════════════════════════════════


@router.post("/threads", response_model=ThreadPublic)
def create_thread(
    thread_in: ThreadCreate,
    session: SessionDep,
    current_user: CurrentUser,
):
    """
    Create a new conversation thread.

    Each thread belongs to the authenticated user.
    """
    assert current_user.id is not None  # Guaranteed by auth
    thread = crud.create_thread(
        session=session,
        user_id=current_user.id,
        thread_in=thread_in,
    )
    return thread


@router.get("/threads", response_model=list[ThreadPublic])
def get_threads(
    session: SessionDep,
    current_user: CurrentUser,
):
    """
    Get all threads for the current user.

    Returns threads ordered by most recently updated first.
    """
    assert current_user.id is not None  # Guaranteed by auth
    threads = crud.get_threads_by_user(session=session, user_id=current_user.id)
    return threads


@router.delete("/threads/{thread_id}")
def delete_thread(
    thread_id: int,
    session: SessionDep,
    current_user: CurrentUser,
):
    """
    Delete a thread and all its messages.

    Only the thread owner can delete it.
    """
    thread = crud.get_thread_by_id(session=session, thread_id=thread_id)

    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    if thread.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this thread"
        )

    crud.delete_thread(session=session, thread=thread)
    return {"message": "Thread deleted"}


# ═══════════════════════════════════════════════════════════════
# MESSAGE ENDPOINTS
# ═══════════════════════════════════════════════════════════════


@router.get("/threads/{thread_id}/messages", response_model=list[ChatMessagePublic])
def get_thread_messages(
    thread_id: int,
    session: SessionDep,
    current_user: CurrentUser,
):
    """
    Get all messages in a thread.

    Returns messages ordered by creation time (oldest first).
    """
    thread = crud.get_thread_by_id(session=session, thread_id=thread_id)

    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    if thread.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to view this thread"
        )

    messages = crud.get_messages_by_thread(session=session, thread_id=thread_id)
    return messages


@router.post("/threads/{thread_id}/messages", response_model=ChatMessagePublic)
def send_message(
    thread_id: int,
    message_in: ChatMessageCreate,
    session: SessionDep,
    current_user: CurrentUser,
):
    """
    Send a message to a thread and get AI response.

    TODO(human): Integrate with LangGraph agent here.
    For now, this just saves the user message.
    """
    thread = crud.get_thread_by_id(session=session, thread_id=thread_id)

    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    if thread.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to post to this thread"
        )

    # Save user message
    user_message = crud.create_message(
        session=session,
        thread_id=thread_id,
        role="user",
        content=message_in.content,
    )

    # Update thread timestamp
    crud.update_thread_timestamp(session=session, thread=thread)

    # TODO(human): Call LangGraph agent here and save AI response
    # For now, just return the user message

    return user_message
