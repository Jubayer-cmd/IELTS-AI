"""
Chat API routes for thread and message management.

These endpoints integrate with the frontend chat UI and LangGraph agent.
"""

import json
from collections.abc import AsyncGenerator

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from sqlmodel import Session

from app import crud
from app.api.deps import CurrentUser, SessionDep
from app.core.db import engine
from app.models.chat import (
    ChatMessageCreate,
    ChatMessagePublic,
    ThreadCreate,
    ThreadPublic,
)
from app.services.langgraph import (
    generate_thread_title,
    process_message,
    stream_message_async,
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
    Send a message to a thread and get AI response (non-streaming).

    Processes the user message through LangGraph agent and returns
    the AI assistant's complete response.
    """
    thread = crud.get_thread_by_id(session=session, thread_id=thread_id)

    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    if thread.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to post to this thread"
        )

    # Save user message
    crud.create_message(
        session=session,
        thread_id=thread_id,
        role="user",
        content=message_in.content,
    )

    # Process through LangGraph agent (with user_id for long-term memory)
    ai_response_content = process_message(
        user_message=message_in.content,
        thread_id=thread_id,
        user_id=current_user.id,
    )

    # Save AI response
    ai_message = crud.create_message(
        session=session,
        thread_id=thread_id,
        role="assistant",
        content=ai_response_content,
    )

    # Update thread timestamp
    crud.update_thread_timestamp(session=session, thread=thread)

    return ai_message


# ═══════════════════════════════════════════════════════════════
# STREAMING ENDPOINT (SSE)
# ═══════════════════════════════════════════════════════════════


@router.post("/threads/{thread_id}/messages/stream")
async def stream_message_endpoint(
    thread_id: int,
    message_in: ChatMessageCreate,
    session: SessionDep,
    current_user: CurrentUser,
):
    """
    Stream AI response as Server-Sent Events (SSE) with token-by-token output.

    Uses astream_events for true streaming from the LLM, sending tokens
    progressively as they're generated.

    SSE Protocol:
    - Token events: data: <token_text>
    - Complete event: data: {"type":"complete","id":<msg_id>,"created_at":"..."}
    - Done signal: data: [DONE]
    """
    thread = crud.get_thread_by_id(session=session, thread_id=thread_id)

    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    if thread.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to post to this thread"
        )

    # Check if this is the first message (for auto-title generation)
    existing_message_count = crud.get_thread_message_count(
        session=session, thread_id=thread_id
    )
    is_first_message = existing_message_count == 0

    # Save user message immediately (before streaming starts)
    crud.create_message(
        session=session,
        thread_id=thread_id,
        role="user",
        content=message_in.content,
    )

    # Store values for use in the async generator
    user_content = message_in.content
    user_id = current_user.id

    async def generate_sse() -> AsyncGenerator[str, None]:
        """Async generator that yields SSE-formatted events."""
        accumulated_content = ""

        try:
            # Stream tokens from LangGraph using async streaming (with user_id for long-term memory)
            async for token in stream_message_async(
                user_message=user_content,
                thread_id=thread_id,
                user_id=user_id,
            ):
                accumulated_content += token
                # SSE format: "data: <content>\n\n"
                # Escape newlines since SSE doesn't support multiline data fields
                token_escaped = token.replace("\\", "\\\\").replace("\n", "\\n")
                yield f"data: {token_escaped}\n\n"

            # After streaming completes, save AI message to database
            with Session(engine) as db_session:
                ai_message = crud.create_message(
                    session=db_session,
                    thread_id=thread_id,
                    role="assistant",
                    content=accumulated_content,
                )

                # Update thread timestamp
                thread_to_update = crud.get_thread_by_id(
                    session=db_session, thread_id=thread_id
                )
                if thread_to_update:
                    crud.update_thread_timestamp(
                        session=db_session, thread=thread_to_update
                    )

                # Generate title for first message (ChatGPT/Claude style)
                new_title = None
                if is_first_message and thread_to_update:
                    try:
                        new_title = generate_thread_title(user_content)
                        crud.update_thread_title(
                            session=db_session,
                            thread=thread_to_update,
                            title=new_title,
                        )
                    except Exception as e:
                        print(f"Failed to generate title: {e}")
                        # Don't fail the whole request if title generation fails

                # Send completion metadata (include new title if generated)
                complete_data = {
                    "type": "complete",
                    "id": ai_message.id,
                    "created_at": ai_message.created_at.isoformat(),
                }
                if new_title:
                    complete_data["title"] = new_title

                yield f"data: {json.dumps(complete_data)}\n\n"

        except Exception as e:
            # Send error event with full traceback for debugging
            import traceback
            error_msg = f"{type(e).__name__}: {e}\n{traceback.format_exc()}"
            print(f"Streaming error: {error_msg}")  # Log to console
            error_data = {"type": "error", "message": str(e) or type(e).__name__}
            yield f"data: {json.dumps(error_data)}\n\n"

        # Signal stream end
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate_sse(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
        },
    )
