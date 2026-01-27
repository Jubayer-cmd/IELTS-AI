"""
LangGraph agent for IELTS Writing AI.

This module defines the conversational AI agent with two modes:
- Chat: General English tutoring conversations
- Essay: IELTS essay evaluation with scoring and feedback

The agent uses a router to classify user intent and direct to the appropriate node.
"""

from typing import Annotated

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from pydantic import SecretStr
from typing_extensions import TypedDict

from app.core.config import settings

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
    model="upstage/solar-pro-3:free",
    streaming=True,
)

checkpoint = MemorySaver()


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
# NODE FUNCTIONS
# ═══════════════════════════════════════════════════════════════


def chat_node(state: AgentState) -> dict:
    """
    General English tutoring chat node.

    Handles casual conversation about English learning, grammar,
    vocabulary, and language tips.
    """
    messages = [
        SystemMessage(
            content=(
                "You are a friendly English tutor named Engla. "
                "Help users with basic English questions, grammar, vocabulary, "
                "and language learning tips. Keep responses focused on English learning. "
                "If users ask unrelated questions, politely redirect to English topics."
            )
        ),
        *state["message"],
    ]

    response = model.invoke(messages)
    return {"message": [AIMessage(content=response.content)]}


def essay_node(state: AgentState) -> dict:
    """
    IELTS essay evaluation node.

    Evaluates essays using official IELTS band descriptors and provides:
    - Overall band score (1-9)
    - Individual criterion scores
    - Detailed feedback with improvements
    """
    messages = [
        SystemMessage(
            content="""You are an expert IELTS examiner. Evaluate essays and provide:
1. Overall Band Score (1-9)
2. Task Achievement score
3. Coherence & Cohesion score
4. Lexical Resource score
5. Grammatical Range & Accuracy score
6. Detailed feedback with specific improvements

Use the count_words tool to check word count.
Use the count_words_limit tool to verify if essay meets the minimum 250 word requirement."""
        ),
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

builder = StateGraph(AgentState)

# Add nodes
builder.add_node("chat", chat_node)
builder.add_node("essay", essay_node)

# Add edges - router is a conditional edge function, not a node
# This means it won't appear in langgraph_node metadata
builder.add_conditional_edges(START, router)
builder.add_edge("chat", END)
builder.add_edge("essay", END)

# Compile with checkpointer for conversation memory
graph = builder.compile(checkpointer=checkpoint)
