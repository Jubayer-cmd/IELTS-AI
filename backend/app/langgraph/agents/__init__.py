"""
IELTS Multi-Agent System.

This package contains specialized agents for the IELTS evaluation workflow:
- Supervisor: Orchestrates the evaluation workflow
- Scorers: Individual criterion scoring agents (Task Achievement, Coherence, Lexical, Grammar)
"""

from app.langgraph.agents.supervisor import create_supervisor_agent

__all__ = ["create_supervisor_agent"]
