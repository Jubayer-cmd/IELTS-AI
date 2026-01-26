from typing import Annotated

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from pydantic import SecretStr
from typing_extensions import TypedDict

from app.core.config import settings


class BasicChat(TypedDict):
    message: Annotated[list, add_messages]


model = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=SecretStr(settings.OPENROUTER_API_KEY),
    model="xiaomi/mimo-v2-flash:free",
)

checkpoint = MemorySaver()


@tool
def count_words(text: str) -> int:
    """Count the number of words in the given text."""
    return len(text.split())


@tool
def count_words_limit(text: str) -> bool:
    """checking if number of word exceeds the 300 word limit"""
    if len(text.split()) > 300:
        return False
    else:
        return True


tools = [count_words, count_words_limit]
model_with_tools = model.bind_tools(tools)


def chat(state: BasicChat):
    messages = [
        SystemMessage(
            content="You are a friendly English tutor named Engla. Help users with basic English questions, grammar, vocabulary, and language learning tips. your every message should be relevent to the English tutor focus and reply if user askend unrelvent things that you can only help in english learning"
        ),
        *state["message"],
    ]
    response = model.invoke(messages)
    return {"message": [AIMessage(content=response.content)]}


def essay(state: BasicChat):
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
            Use the count_words_limit tool to verify if essay meets requirements."""
        ),
        *state["message"],
    ]

    # Call LLM with tools available
    # model_with_tools can decide: "I need a tool" OR "I have the answer"
    response = model_with_tools.invoke(messages)

    # ─────────────────────────────────────────────────────────────
    # TOOL CALL HANDLING LOOP
    # ─────────────────────────────────────────────────────────────
    # response.tool_calls is a list like:
    # [{"id": "call_abc", "name": "count_words", "args": {"text": "..."}}]
    # If empty [], the while loop doesn't run (LLM gave direct answer)
    # ─────────────────────────────────────────────────────────────
    while response.tool_calls:
        # Step 1: Add the AI's "I want to use tools" message to history
        # This is important! LLM needs to see its own tool request
        messages.append(response)

        # Step 2: Loop through each tool the LLM wants to call
        # LLM might request multiple tools at once
        for tool_call in response.tool_calls:
            # Extract tool info from the request
            # tool_call = {"id": "call_abc", "name": "count_words", "args": {"text": "..."}}
            tool_name = tool_call["name"]  # Which tool? e.g., "count_words"
            tool_args = tool_call["args"]  # Arguments? e.g., {"text": "my essay"}

            # Step 3: Execute the actual tool function
            # We match the name and call the corresponding Python function
            if tool_name == "count_words":
                result = count_words.invoke(tool_args)  # Returns: 267
            elif tool_name == "count_words_limit":
                result = count_words_limit.invoke(tool_args)  # Returns: True/False
            else:
                result = "Tool not found"

            # Step 4: Send the tool result back to LLM
            # ToolMessage tells LLM: "Here's the result of the tool you requested"
            # tool_call_id links this result to the original request
            messages.append(
                ToolMessage(
                    content=str(result),  # The actual result: "267" or "True"
                    tool_call_id=tool_call["id"],  # Links to original request
                )
            )

        # Step 5: Call LLM again with the tool results
        # Now LLM sees: [SystemMsg, UserMsg, AIMsg(tool_call), ToolMsg(result)]
        # LLM can now: give final answer OR request more tools
        response = model_with_tools.invoke(messages)

    # ─────────────────────────────────────────────────────────────
    # Loop ends when response.tool_calls is empty []
    # Now response.content has the final answer!
    # ─────────────────────────────────────────────────────────────
    return {"message": [AIMessage(content=response.content)]}


def router(state: BasicChat):
    last_message = state["message"][-1].content

    response = model.invoke(
        [
            SystemMessage(
                content="""Classify user intent.
        Reply with ONLY one word:
        - "essay" if user wants IELTS essay evaluation
        - "chat" if general conversation"""
            ),
            HumanMessage(content=last_message),
        ]
    )

    route = str(response.content).strip().lower()
    if "essay" in route:
        return "essay"
    return "chat"


builder = StateGraph(BasicChat)
builder.add_node("chat", chat)
builder.add_node("essay", essay)
builder.add_conditional_edges(START, router)
builder.add_edge("chat", END)
builder.add_edge("essay", END)

graph = builder.compile(checkpointer=checkpoint)

config: RunnableConfig = {"configurable": {"thread_id": "user-123"}}

if __name__ == "__main__":
    print("Chat with AI (type 'quit' to exit)")
    print("─" * 40)

    while True:
        user_input = input("\nYou: ")
        if user_input == "quit":
            break

        print("AI: ", end="", flush=True)

        # Stream the response token by token
        # stream_mode="messages" returns tuples: (AIMessageChunk, metadata_dict)
        for msg_chunk, metadata in graph.stream(
            {"message": [HumanMessage(content=user_input)]},
            config,
            stream_mode="messages",
        ):
            # msg_chunk is AIMessageChunk with content attribute
            # metadata is dict with thread info (we don't need it)
            # Only print if it has content (skip empty chunks)
            if hasattr(msg_chunk, "content") and msg_chunk.content:
                print(msg_chunk.content, end="", flush=True)

        print()  # New line after response complete
