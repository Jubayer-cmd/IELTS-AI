"""
Main IELTS Evaluation Graph.

This is the primary entry point for the LangGraph IELTS evaluation system.

MODULE 1 GOAL: Build a simple graph that accepts an essay and returns a response.

HINTS:
------
1. Import what you need:
   - StateGraph, START, END from langgraph.graph
   - Your IELTSState from state.py
   - Your node function from nodes.py

2. Create graph builder:
   - builder = StateGraph(YourStateClass)

3. Add nodes (workers):
   - builder.add_node("node_name", node_function)

4. Add edges (connections):
   - builder.add_edge(START, "first_node")
   - builder.add_edge("last_node", END)

5. Compile the graph:
   - graph = builder.compile()

FLOW: START -> process_essay -> END
"""

# TODO(human): Write your imports here


# TODO(human): Create the create_ielts_graph function that builds and compiles the graph


# TODO(human): Create a get_graph function that returns the compiled graph
