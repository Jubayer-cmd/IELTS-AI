"""
LLM Prompt Templates for IELTS Evaluation.

This module contains all prompt templates used by the IELTS evaluation agents.
Centralizing prompts makes them easier to maintain, test, and version.

TODO (Module 4+): Add prompt templates as you build each feature
"""

# System prompt for the main IELTS evaluator
IELTS_EVALUATOR_SYSTEM_PROMPT = """You are an expert IELTS Writing examiner with years of experience.
You evaluate essays according to the official IELTS band descriptors.

Your evaluation must be:
- Fair and objective
- Based on the official IELTS criteria
- Constructive with specific improvement suggestions

The four criteria you evaluate are:
1. Task Achievement/Response (25%)
2. Coherence and Cohesion (25%)
3. Lexical Resource (25%)
4. Grammatical Range and Accuracy (25%)
"""

# Prompt for classifying essay type
ESSAY_CLASSIFIER_PROMPT = """Analyze the following IELTS essay and determine if it is:
- Task 1: Describes visual information (graph, chart, diagram, map, process)
- Task 2: Argumentative/discursive essay on a given topic

Essay:
{essay}

Respond with only "task1" or "task2".
"""

# Prompt templates for each criterion scorer
TASK_ACHIEVEMENT_PROMPT = """Evaluate the following essay for Task Achievement.

Task Type: {task_type}
Essay:
{essay}

Consider:
- Does the essay address all parts of the task?
- Is the response well-developed with relevant examples?
- Is the position clear throughout?

Provide a band score (1-9) and detailed feedback.
"""

COHERENCE_PROMPT = """Evaluate the following essay for Coherence and Cohesion.

Essay:
{essay}

Consider:
- Is information and ideas organized logically?
- Is there clear progression throughout?
- Are cohesive devices used effectively?
- Is paragraphing appropriate?

Provide a band score (1-9) and detailed feedback.
"""

LEXICAL_PROMPT = """Evaluate the following essay for Lexical Resource.

Essay:
{essay}

Consider:
- Is there a wide range of vocabulary?
- Are words used accurately?
- Is there evidence of less common vocabulary?
- Are there spelling errors?

Provide a band score (1-9) and detailed feedback.
"""

GRAMMAR_PROMPT = """Evaluate the following essay for Grammatical Range and Accuracy.

Essay:
{essay}

Consider:
- Is there a variety of sentence structures?
- Are complex sentences used accurately?
- Are there grammar or punctuation errors?
- Do errors impede communication?

Provide a band score (1-9) and detailed feedback.
"""

# Aggregation prompt for final feedback
FEEDBACK_AGGREGATION_PROMPT = """Based on the following criterion scores, generate comprehensive feedback.

Task Achievement: {ta_score}/9 - {ta_feedback}
Coherence & Cohesion: {cc_score}/9 - {cc_feedback}
Lexical Resource: {lr_score}/9 - {lr_feedback}
Grammar & Accuracy: {ga_score}/9 - {ga_feedback}

Overall Band Score: {overall_band}/9

Generate:
1. A summary of strengths
2. Key areas for improvement
3. Specific actionable suggestions
4. Encouragement for the learner
"""
