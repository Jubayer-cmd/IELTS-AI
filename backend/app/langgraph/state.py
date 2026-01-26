"""
State definitions for the IELTS LangGraph agent.

MODULE 1 GOAL: Define the state that flows through your graph.

HINTS:
------
1. State is a TypedDict - a dictionary with typed keys
2. Use Annotated with add_messages for message lists (appends instead of replaces)
3. Start simple - just messages and essay for now

EXAMPLE STATE STRUCTURE:
    class MyState(TypedDict):
        messages: Annotated[list[AnyMessage], add_messages]  # Conversation history
        essay: str | None                                     # The essay text

IMPORTS YOU'LL NEED:
    from typing import Annotated
    from typing_extensions import TypedDict
    from langgraph.graph.message import add_messages
    from langchain_core.messages import AnyMessage
"""

# TODO(human): Write your imports here


# TODO(human): Define your IELTSState TypedDict class
# Start with just 'messages' and 'essay' fields for Module 1
