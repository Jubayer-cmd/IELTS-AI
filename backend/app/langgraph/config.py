"""
LangGraph Configuration for IELTS Evaluation.

This module contains configuration settings for the LangGraph agents:
- Checkpointer setup (memory, PostgreSQL)
- Model configuration
- Retry policies
- Runtime settings

TODO (Module 2+): Configure as you implement features
"""

from typing import Any

from langgraph.checkpoint.memory import MemorySaver

# Default checkpointer for development (in-memory)
# For production, switch to PostgreSQL checkpointer
DEFAULT_CHECKPOINTER = MemorySaver()


def get_checkpointer(use_postgres: bool = False) -> Any:
    """
    Get the appropriate checkpointer based on environment.

    Args:
        use_postgres: If True, use PostgreSQL checkpointer for production

    Returns:
        Checkpointer instance
    """
    if use_postgres:
        # TODO (Module 10): Implement PostgreSQL checkpointer
        # from langgraph.checkpoint.postgres import PostgresSaver
        # return PostgresSaver(connection_string=settings.DATABASE_URL)
        raise NotImplementedError("PostgreSQL checkpointer not yet configured")

    return DEFAULT_CHECKPOINTER


# Retry policy for API calls (Module 7)
DEFAULT_RETRY_POLICY = {
    "max_attempts": 3,
    "initial_interval": 1.0,
    "backoff_multiplier": 2.0,
}

# Model configuration
MODEL_CONFIG = {
    "default_model": "gpt-4o-mini",  # Cost-effective for development
    "evaluation_model": "gpt-4o",     # Better quality for actual scoring
    "temperature": 0.3,               # Lower for consistent evaluations
    "max_tokens": 2000,
}

# Graph execution settings
GRAPH_CONFIG = {
    "recursion_limit": 50,  # Maximum number of steps
    "timeout": 120,         # Seconds before timeout
}
