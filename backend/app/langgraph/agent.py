"""
LangGraph agent for IELTS Writing AI.

This module defines the conversational AI agent with two modes:
- Chat: General English tutoring conversations
- Essay: IELTS essay evaluation with scoring and feedback

Memory Architecture:
- Short-term: PostgresSaver checkpointer (thread-scoped conversation history)
- Long-term: PostgresStore (cross-session user profiles and preferences)

See: https://docs.langchain.com/oss/python/langgraph/memory
"""

from typing import Annotated

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.store.base import BaseStore
from pydantic import SecretStr
from typing_extensions import TypedDict

from app.core.config import settings
from app.core.memory import (
    get_async_checkpointer,
    get_async_memory_store,
    get_checkpointer,
    get_memory_store,
)

# ═══════════════════════════════════════════════════════════════
# STATE DEFINITION
# ═══════════════════════════════════════════════════════════════


class AgentState(TypedDict):
    """State schema for the IELTS agent graph."""

    message: Annotated[list, add_messages]


# ═══════════════════════════════════════════════════════════════
# MODEL CONFIGURATION
# ═══════════════════════════════════════════════════════════════

# Single model instance with streaming enabled
# Router output is filtered by langgraph_node in astream_events (best practice)
# See: https://docs.langchain.com/oss/python/langgraph/streaming
model = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=SecretStr(settings.OPENROUTER_API_KEY),
    model="tngtech/tng-r1t-chimera:free",
    streaming=True,
)


# ═══════════════════════════════════════════════════════════════
# TOOLS
# ═══════════════════════════════════════════════════════════════


@tool
def count_words(text: str) -> int:
    """Count the number of words in the given text."""
    return len(text.split())


@tool
def count_words_limit(text: str) -> bool:
    """Check if the text meets the minimum 250 word requirement for IELTS Task 2."""
    return len(text.split()) >= 250


tools = [count_words, count_words_limit]
model_with_tools = model.bind_tools(tools)


# ═══════════════════════════════════════════════════════════════
# LONG-TERM MEMORY HELPERS
# ═══════════════════════════════════════════════════════════════


def get_user_context(store: BaseStore, user_id: str) -> str:
    """
    Retrieve user's long-term memory context.

    Fetches user profile and preferences from the memory store
    to personalize the agent's responses.
    """
    if not user_id:
        return ""

    context_parts = []

    # Get user profile
    namespace = (user_id, "profile")
    try:
        items = list(store.search(namespace))
        for item in items:
            if "data" in item.value:
                context_parts.append(f"User info: {item.value['data']}")
    except Exception:
        pass  # Store might not be initialized yet

    # Get recent notes about user
    namespace = (user_id, "notes")
    try:
        items = list(store.search(namespace, limit=3))
        for item in items:
            if "data" in item.value:
                context_parts.append(f"Previous observation: {item.value['data']}")
    except Exception:
        pass

    return "\n".join(context_parts)


# ═══════════════════════════════════════════════════════════════
# NODE FUNCTIONS
# ═══════════════════════════════════════════════════════════════


def chat_node(state: AgentState, config: RunnableConfig, *, store: BaseStore) -> dict:
    """
    General English tutoring chat node.

    Handles casual conversation about English learning, grammar,
    vocabulary, and language tips.

    Uses long-term memory to personalize responses.
    """
    # Get user context from long-term memory
    user_id = config.get("configurable", {}).get("user_id", "")
    user_context = get_user_context(store, user_id)

    system_content = (
        "You are a friendly English tutor named Engla. "
        "Help users with basic English questions, grammar, vocabulary, "
        "and language learning tips. Keep responses focused on English learning. "
        "If users ask unrelated questions, politely redirect to English topics."
    )

    if user_context:
        system_content += f"\n\nUser Context:\n{user_context}"

    messages = [
        SystemMessage(content=system_content),
        *state["message"],
    ]

    response = model.invoke(messages)
    return {"message": [AIMessage(content=response.content)]}


def essay_node(state: AgentState, config: RunnableConfig, *, store: BaseStore) -> dict:
    """
    IELTS essay evaluation node.

    Evaluates essays using official IELTS band descriptors and provides:
    - Overall band score (1-9)
    - Individual criterion scores
    - Detailed feedback with improvements

    Uses long-term memory for personalized feedback.
    """
    # Get user context from long-term memory
    user_id = config.get("configurable", {}).get("user_id", "")
    user_context = get_user_context(store, user_id)

    system_content = """You are an expert IELTS examiner. Evaluate essays and provide:
1. Overall Band Score (1-9)
2. Task Achievement score
3. Coherence & Cohesion score
4. Lexical Resource score
5. Grammatical Range & Accuracy score
6. Detailed feedback with specific improvements

Use the count_words tool to check word count.
Use the count_words_limit tool to verify if essay meets the minimum 250 word requirement."""

    if user_context:
        system_content += f"\n\nUser Context (tailor feedback based on this):\n{user_context}"

    messages = [
        SystemMessage(content=system_content),
        *state["message"],
    ]

    # Call LLM with tools available
    response = model_with_tools.invoke(messages)

    # Tool call handling loop
    while response.tool_calls:
        messages.append(response)

        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            # Execute the requested tool
            if tool_name == "count_words":
                result = count_words.invoke(tool_args)
            elif tool_name == "count_words_limit":
                result = count_words_limit.invoke(tool_args)
            else:
                result = "Tool not found"

            messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call["id"],
                )
            )

        # Get next response (may request more tools or give final answer)
        response = model_with_tools.invoke(messages)

    return {"message": [AIMessage(content=response.content)]}


# ═══════════════════════════════════════════════════════════════
# ROUTER (Conditional Edge Function)
# ═══════════════════════════════════════════════════════════════


def router(state: AgentState) -> str:
    """
    Route user messages to the appropriate node.

    Classifies intent as either 'essay' (for IELTS evaluation)
    or 'chat' (for general English tutoring).

    Note: Router output is filtered by langgraph_node in streaming,
    so we don't need a separate non-streaming model.
    """
    last_message = state["message"][-1].content

    response = model.invoke(
        [
            SystemMessage(
                content="""Classify user intent. Reply with ONLY one word:
- "essay" if user wants IELTS essay evaluation or submits an essay
- "chat" if general conversation or English learning question"""
            ),
            HumanMessage(content=last_message),
        ]
    )

    route = str(response.content).strip().lower()
    if "essay" in route:
        return "essay"
    return "chat"


# ═══════════════════════════════════════════════════════════════
# GRAPH CONSTRUCTION
# ═══════════════════════════════════════════════════════════════


def _build_graph_base():
    """Build the base graph structure (without memory components)."""
    builder = StateGraph(AgentState)

    # Add nodes
    builder.add_node("chat", chat_node)
    builder.add_node("essay", essay_node)

    # Add edges - router is a conditional edge function, not a node
    builder.add_conditional_edges(START, router)
    builder.add_edge("chat", END)
    builder.add_edge("essay", END)

    return builder


def build_graph():
    """
    Build and compile the sync agent graph with memory.

    Returns a compiled graph with:
    - PostgresSaver checkpointer (short-term memory)
    - PostgresStore (long-term memory)

    Use this for synchronous operations like graph.invoke().
    """
    builder = _build_graph_base()

    # Get sync memory components
    checkpointer = get_checkpointer()
    store = get_memory_store()

    # Compile with both checkpointer (short-term) and store (long-term)
    return builder.compile(checkpointer=checkpointer, store=store)


def build_async_graph():
    """
    Build and compile the async agent graph with memory.

    Returns a compiled graph with:
    - AsyncPostgresSaver checkpointer (async short-term memory)
    - AsyncPostgresStore (async long-term memory)

    Use this for async operations like astream_events().
    """
    builder = _build_graph_base()

    # Get async memory components
    checkpointer = get_async_checkpointer()
    store = get_async_memory_store()

    # Compile with async checkpointer and store
    return builder.compile(checkpointer=checkpointer, store=store)


# Lazy initialization of graphs (to avoid import-time database connection)
_graph = None
_async_graph = None


def get_graph():
    """Get the compiled sync graph (lazy initialization)."""
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph


def get_async_graph():
    """Get the compiled async graph (lazy initialization)."""
    global _async_graph
    if _async_graph is None:
        _async_graph = build_async_graph()
    return _async_graph
