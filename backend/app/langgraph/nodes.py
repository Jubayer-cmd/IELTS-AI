"""
Node functions for the IELTS LangGraph agent.

MODULE 1 GOAL: Create a simple node that processes essay submissions.

HINTS:
------
1. A node is just a function that:
   - Receives state as input
   - Returns a dict with state updates

2. Node function signature:
   def my_node(state: YourState) -> dict:
       # Read from state
       essay = state.get("essay")
       # Return updates
       return {"messages": [AIMessage(content="...")]}

3. For messages, return a list - the add_messages reducer will append them

IMPORTS YOU'LL NEED:
    from langchain_core.messages import AIMessage, HumanMessage
    from app.langgraph.state import IELTSState
"""

# TODO(human): Write your imports here


# TODO(human): Create a process_essay_node function
# It should:
# 1. Get the essay from state
# 2. If no essay, return a message asking for one
# 3. If essay exists, return a message with the word count
