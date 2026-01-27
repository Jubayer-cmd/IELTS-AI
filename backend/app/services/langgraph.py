"""
LangGraph service for processing chat messages through the IELTS AI agent.

This module provides the integration layer between the FastAPI chat endpoints
and the LangGraph agent defined in app/langgraph/agent.py.

Supports both synchronous (invoke) and asynchronous (streaming) operations.
"""

from collections.abc import AsyncGenerator, Generator

from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

from app.langgraph.agent import graph

# ═══════════════════════════════════════════════════════════════
# ASYNC STREAMING (Token-by-token via astream_events)
# ═══════════════════════════════════════════════════════════════


async def stream_message_async(
    user_message: str, thread_id: int
) -> AsyncGenerator[str, None]:
    """
    Stream AI response tokens using astream_events for true token-by-token output.

    This async generator uses LangGraph's astream_events to capture streaming
    tokens from the underlying LLM calls, providing real-time output.

    Args:
        user_message: The user's input text
        thread_id: Database thread ID for conversation memory isolation

    Yields:
        Individual content tokens from the AI response
    """
    config: RunnableConfig = {"configurable": {"thread_id": str(thread_id)}}

    # Valid nodes that produce final AI responses
    valid_nodes = {"chat", "essay"}

    async for event in graph.astream_events(
        {"message": [HumanMessage(content=user_message)]},
        config,
        version="v2",
    ):
        # Filter for chat model streaming events
        # These contain the actual tokens being generated
        if event["event"] == "on_chat_model_stream":
            # Check if this is from a valid node (not router)
            # The langgraph_node tag tells us which node triggered this
            tags = event.get("tags", [])
            node_name = None
            for tag in tags:
                if tag in valid_nodes:
                    node_name = tag
                    break

            # Also check metadata for node info
            if not node_name:
                metadata = event.get("metadata", {})
                node_name = metadata.get("langgraph_node", "")

            # Skip if not from chat/essay nodes
            if node_name not in valid_nodes:
                continue

            # Extract token content from the chunk
            chunk = event.get("data", {}).get("chunk")
            if chunk and hasattr(chunk, "content") and chunk.content:
                content = chunk.content
                if isinstance(content, str) and content:
                    yield content


# ═══════════════════════════════════════════════════════════════
# SYNC STREAMING (State-level via graph.stream)
# ═══════════════════════════════════════════════════════════════


def stream_message(user_message: str, thread_id: int) -> Generator[str, None, None]:
    """
    Stream AI response at the message level (not token-level).

    This sync generator uses graph.stream which streams state updates.
    For true token-by-token streaming, use stream_message_async instead.

    Args:
        user_message: The user's input text
        thread_id: Database thread ID for conversation memory isolation

    Yields:
        Content chunks from the AI response (may be full messages)
    """
    config: RunnableConfig = {"configurable": {"thread_id": str(thread_id)}}
    valid_nodes = {"chat", "essay"}

    for msg_chunk, metadata in graph.stream(
        {"message": [HumanMessage(content=user_message)]},
        config,
        stream_mode="messages",
    ):
        # Filter: only yield from chat/essay nodes, not router
        node_name = metadata.get("langgraph_node", "")
        if node_name not in valid_nodes:
            continue

        if hasattr(msg_chunk, "content") and msg_chunk.content:
            content = msg_chunk.content
            if isinstance(content, str) and content:
                yield content


# ═══════════════════════════════════════════════════════════════
# SYNC INVOKE (Complete response)
# ═══════════════════════════════════════════════════════════════


def process_message(user_message: str, thread_id: int) -> str:
    """
    Process a user message and return the complete AI response.

    This function invokes the compiled LangGraph with proper thread configuration
    for conversation memory persistence. Use this for non-streaming scenarios.

    Args:
        user_message: The user's input text
        thread_id: Database thread ID for conversation memory isolation

    Returns:
        The AI assistant's response text
    """
    config: RunnableConfig = {"configurable": {"thread_id": str(thread_id)}}

    state = graph.invoke(
        {"message": [HumanMessage(content=user_message)]},
        config,
    )

    ai_response = state["message"][-1]
    return str(ai_response.content)


# Expose the graph for advanced usage
ielts_agent = graph
