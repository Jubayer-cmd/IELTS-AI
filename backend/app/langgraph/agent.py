"""
IELTS LangGraph Agent - Everything in One File!

MODULE 1: Build your first graph

CONCEPTS:
---------
1. STATE = A TypedDict that holds data (like a shopping cart)
2. NODE = A function that processes state (like a worker)
3. EDGE = Connection between nodes (like a conveyor belt)
4. GRAPH = Nodes + Edges compiled together

YOUR GOAL:
----------
Build: START -> process_essay -> END

HINTS:
------
# Step 1: Define State
class MyState(TypedDict):
    messages: Annotated[list, add_messages]  # add_messages = append, not replace
    essay: str | None

# Step 2: Create Node (just a function!)
def my_node(state: MyState) -> dict:
    return {"messages": [AIMessage(content="Hello!")]}

# Step 3: Build Graph
builder = StateGraph(MyState)
builder.add_node("my_node", my_node)
builder.add_edge(START, "my_node")
builder.add_edge("my_node", END)
graph = builder.compile()

# Step 4: Run it!
result = graph.invoke({"messages": [], "essay": "my essay"})
"""

# ============================================
# IMPORTS - These are what you need
# ============================================
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage, AnyMessage


# ============================================
# TODO(human): Define your IELTSState here
# ============================================
# Hint: You need 'messages' (with add_messages) and 'essay' fields


# ============================================
# TODO(human): Create your process_essay_node function
# ============================================
# Hint: Check if essay exists, return appropriate message


# ============================================
# TODO(human): Build and compile the graph
# ============================================
# Hint: StateGraph -> add_node -> add_edge -> compile


# ============================================
# TEST: Uncomment below to test your graph
# ============================================
# if __name__ == "__main__":
#     result = graph.invoke({"messages": [], "essay": None})
#     print("No essay:", result["messages"][-1].content)
#
#     result = graph.invoke({"messages": [], "essay": "This is my test essay about climate change."})
#     print("With essay:", result["messages"][-1].content)
