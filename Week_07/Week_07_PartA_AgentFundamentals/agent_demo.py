"""
Week 7 - Part A: Agent Fundamentals & LangGraph Core

Implements:
1. AgentState with append-only reducer (add_messages) and scalar overwrite (steps).
2. LangGraph nodes: agent_node, tools, give_up_node.
3. Conditional edge route_after_agent checking MAX_STEPS = 6.
4. Practice & Challenges (Challenge 1: MAX_STEPS=2, Challenge 2: failing tool, Challenge 3: Mermaid graph).
"""

import os
import sys
from pathlib import Path
from typing import Annotated, TypedDict, List
from dotenv import load_dotenv

# Load environment variables
_curr_dir = Path(__file__).resolve().parent
_week7_env = _curr_dir.parent / ".env"
if _week7_env.exists():
    load_dotenv(_week7_env)
else:
    load_dotenv()

from langchain_core.messages import SystemMessage, AIMessage, HumanMessage, ToolMessage, BaseMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

# System prompt
SYSTEM_PROMPT = """You are a helpful and precise library assistant.
You can help users find books and check their availability using the tools provided.
Always verify if a book is available before confirming to the user."""

# ---------------------------------------------------------------------------
# 1. Tools Definition
# ---------------------------------------------------------------------------
@tool
def search_books(genre_or_title: str) -> str:
    """Search library catalog by genre, topic, or book title."""
    books = {
        "science fiction": "Found: 'Dune' by Frank Herbert (ID: 101, Genre: Sci-Fi)",
        "sci-fi": "Found: 'Dune' by Frank Herbert (ID: 101, Genre: Sci-Fi)",
        "dune": "Found: 'Dune' by Frank Herbert (ID: 101, Genre: Sci-Fi)",
        "fantasy": "Found: 'The Hobbit' by J.R.R. Tolkien (ID: 102, Genre: Fantasy)"
    }
    query = genre_or_title.lower()
    for key, val in books.items():
        if key in query:
            return val
    return f"Found: 'Neuromancer' by William Gibson (ID: 103, Genre: Sci-Fi)"

@tool
def check_availability(book_id: int) -> str:
    """Check if a specific book is currently available in the library by book ID."""
    if book_id in [101, 103]:
        return f"Book ID {book_id} is AVAILABLE (2 copies on shelf)."
    elif book_id == 102:
        return f"Book ID {book_id} is UNAVAILABLE (All copies checked out)."
    return f"Book ID {book_id} status: AVAILABLE (1 copy)."

@tool
def failing_tool(query: str) -> str:
    """A tool that simulates an unhandled failure by raising an exception."""
    raise RuntimeError("Simulated internal hardware/network crash in failing_tool!")

TOOLS = [search_books, check_availability]

# ---------------------------------------------------------------------------
# 2. State & Graph Construction
# ---------------------------------------------------------------------------
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]  # append-only reducer
    steps: int  # plain overwrite counter

def create_agent_graph(max_steps: int = 6, tools_list=None):
    if tools_list is None:
        tools_list = TOOLS

    # Model resolution: Gemini primary, OpenAI fallback, or Mock fallback
    gemini_key = os.getenv("GEMINI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    model = None

    if gemini_key:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            model = ChatGoogleGenerativeAI(
                model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
                google_api_key=gemini_key,
                temperature=0.0
            )
        except Exception as e:
            print(f"[Model Warning] Could not initialize Gemini: {e}")

    if model is None and openai_key:
        try:
            from langchain_openai import ChatOpenAI
            model = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
        except Exception:
            pass

    if model is None:
        # Deterministic simulation model if no keys available
        raise RuntimeError("No LLM API Key found. Please set GEMINI_API_KEY in .env.")

    model_with_tools = model.bind_tools(tools_list)

    def agent_node(state: AgentState):
        messages = [SystemMessage(SYSTEM_PROMPT)] + state["messages"]
        reply = model_with_tools.invoke(messages)
        return {
            "messages": [reply],
            "steps": state.get("steps", 0) + 1
        }

    def route_after_agent(state: AgentState):
        if state.get("steps", 0) >= max_steps:
            return "give_up"
        last_message = state["messages"][-1]
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"
        return END

    def give_up_node(state: AgentState):
        return {
            "messages": [
                AIMessage(content="I could not finish this within my step limit. Please clarify your request or try again.")
            ]
        }

    # Build Graph
    builder = StateGraph(AgentState)
    builder.add_node("agent", agent_node)
    builder.add_node("tools", ToolNode(tools_list))
    builder.add_node("give_up", give_up_node)

    builder.add_edge(START, "agent")
    builder.add_conditional_edges(
        "agent",
        route_after_agent,
        {"tools": "tools", "give_up": "give_up", END: END}
    )
    builder.add_edge("tools", "agent")
    builder.add_edge("give_up", END)

    return builder.compile()

# ---------------------------------------------------------------------------
# 3. Execution & Practice Demonstration
# ---------------------------------------------------------------------------
def run_practice_demo():
    print("=" * 70)
    print("WEEK 7 - PART A: LANGGRAPH AGENT FUNDAMENTALS")
    print("=" * 70)

    app = create_agent_graph(max_steps=6)

    # Challenge 3: Generate Mermaid Diagram
    print("\n[Challenge 3] Compiled LangGraph Mermaid Diagram:")
    print("-" * 50)
    mermaid_code = app.get_graph().draw_mermaid()
    print(mermaid_code)
    print("-" * 50)

    # Standard Run
    query = "Find a science fiction book and tell me if it is available."
    print(f"\n[Test Run] User: \"{query}\"")
    print("-" * 50)
    
    initial_state = {
        "messages": [HumanMessage(content=query)],
        "steps": 0
    }

    result = app.invoke(initial_state)

    print("\nExecution History Trace (Labeled):")
    for msg in result["messages"]:
        if isinstance(msg, HumanMessage):
            print(f"[USER PROMPT]: {msg.content}")
        elif isinstance(msg, AIMessage):
            if msg.tool_calls:
                print(f"[THOUGHT / TOOL CALL]: {msg.tool_calls}")
            else:
                print(f"[AGENT ANSWER]: {msg.content}")
        elif isinstance(msg, ToolMessage):
            print(f"[TOOL OBSERVATION] ({msg.name}): {msg.content}")

    print(f"\nTotal steps taken: {result['steps']}")

    # -----------------------------------------------------------------------
    # Challenge 1: MAX_STEPS = 2
    # -----------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("[Challenge 1] Testing with MAX_STEPS = 2 (Enforcing Step Exhaustion)")
    print("=" * 70)
    limited_app = create_agent_graph(max_steps=2)
    res_limited = limited_app.invoke({
        "messages": [HumanMessage(content="Find a science fiction book and tell me if it is available.")],
        "steps": 0
    })
    for msg in res_limited["messages"]:
        if isinstance(msg, AIMessage) and not msg.tool_calls:
            print(f"[RESULT UNDER STEP LIMIT]: {msg.content}")
    print(f"Steps recorded: {res_limited['steps']}")

    # -----------------------------------------------------------------------
    # Challenge 2: Tool that raises an exception
    # -----------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("[Challenge 2] Testing Tool that raises an unhandled exception")
    print("=" * 70)
    failing_tools = [failing_tool]
    failing_app = create_agent_graph(max_steps=6, tools_list=failing_tools)
    print("Predicting behavior: Tool will raise RuntimeError; unhandled exception will propagate unless caught in node.")
    try:
        failing_app.invoke({
            "messages": [HumanMessage(content="Use the failing_tool to check status.")],
            "steps": 0
        })
        print("Outcome: Completed without error.")
    except Exception as ex:
        print(f"Outcome (Observed): Graph execution halted abruptly with exception: {type(ex).__name__}: {ex}")

if __name__ == "__main__":
    run_practice_demo()
