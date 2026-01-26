"""
Supervisor Agent for IELTS Evaluation.

The supervisor orchestrates the multi-agent workflow:
1. Receives essay submission
2. Routes to classifier (Task 1 vs Task 2)
3. Delegates to appropriate criterion scorers
4. Aggregates scores into final band (1-9)
5. Generates comprehensive feedback

TODO (Module 9): Implement supervisor pattern
"""

from langgraph.graph import StateGraph

from app.langgraph.state import IELTSState


def create_supervisor_agent() -> StateGraph:
    """
    Create the supervisor agent graph.

    Returns:
        Compiled StateGraph for the supervisor agent
    """
    # TODO: Implement supervisor logic
    raise NotImplementedError("Supervisor agent not yet implemented")
