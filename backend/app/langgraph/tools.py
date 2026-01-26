"""
Tools for the IELTS LangGraph agent.

Tools extend what agents can do - they're functions the LLM can call.
For IELTS evaluation, tools include:
- Word counting (check minimum requirements)
- Band criteria lookup
- Grammar checking
- Vocabulary analysis

TODO (Module 4): Implement your @tool functions here
"""

from langchain_core.tools import tool

from app.langgraph.state import TASK1_MIN_WORDS, TASK2_MIN_WORDS


@tool
def count_words(essay: str) -> dict:
    """
    Count words in an essay and check against IELTS requirements.

    Args:
        essay: The essay text to analyze

    Returns:
        Dictionary with word_count and whether it meets requirements
    """
    words = essay.split()
    word_count = len(words)

    return {
        "word_count": word_count,
        "meets_task1_requirement": word_count >= TASK1_MIN_WORDS,
        "meets_task2_requirement": word_count >= TASK2_MIN_WORDS,
        "task1_minimum": TASK1_MIN_WORDS,
        "task2_minimum": TASK2_MIN_WORDS,
    }


@tool
def get_band_descriptor(criterion: str, band: int) -> str:
    """
    Get the official IELTS band descriptor for a criterion and band level.

    Args:
        criterion: One of 'task_achievement', 'coherence', 'lexical', 'grammar'
        band: Band level (1-9)

    Returns:
        The official band descriptor text
    """
    # TODO: Implement full band descriptors
    # For now, return placeholder
    return f"Band {band} descriptor for {criterion}: [To be implemented]"


# TODO (Module 4): Add more tools as needed
# - analyze_vocabulary(essay: str) -> dict
# - check_grammar(essay: str) -> list[dict]
# - detect_essay_type(essay: str) -> str
# - calculate_overall_band(scores: dict) -> float
