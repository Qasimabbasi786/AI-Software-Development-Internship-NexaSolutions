"""
Week 6 Part D — Tool Calling with LangChain & .NET Endpoint

Features:
1. Tool Definition: @tool decorator exposes check_book_availability(book_id: int)
   with descriptive docstrings and parameter schemas.
2. Tool Binding: Attached to Google Gemini using model.bind_tools([check_book_availability]).
3. Autonomous Decision Making: The LLM autonomously decides WHEN to invoke live external
   services (availability check) vs. when to answer directly from general knowledge.
4. Round-Trip Execution: Feeds tool execution results back as ToolMessage to produce
   a polished, natural-language synthesized response.
5. Live .NET / DB Integration: Connects to .NET endpoint `GET /api/books/{id}/availability`
   with local catalog fallback.
"""
import os
import sys
from pathlib import Path
from typing import Any
import requests
from dotenv import load_dotenv

# Ensure local .env is loaded
_part_dir = Path(__file__).resolve().parent
_local_env = _part_dir / ".env"
_root_env = _part_dir.parent / ".env"

if _local_env.exists():
    load_dotenv(dotenv_path=_local_env)
elif _root_env.exists():
    load_dotenv(dotenv_path=_root_env)
else:
    load_dotenv()

from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from model_factory import get_chat_model

DOTNET_API_URL = os.getenv("DOTNET_API_URL", "http://localhost:5000")

# Local catalog fallback matching PostgreSQL seeded records
LOCAL_AVAILABILITY = {
    1: {"title": "Clean Code", "isAvailable": True},
    2: {"title": "Designing Data-Intensive Applications", "isAvailable": False},
    3: {"title": "The Pragmatic Programmer", "isAvailable": True},
    4: {"title": "Dune", "isAvailable": True},
    5: {"title": "Pride and Prejudice", "isAvailable": False}
}


# -------------------------------------------------------------
# 1. Defining the LangChain Tool
# -------------------------------------------------------------
@tool
def check_book_availability(book_id: int) -> str:
    """
    Check whether a specific library book (by its numeric ID) is currently available to borrow.
    Always use this tool when the user asks about availability, checkout status, or borrowing state.
    """
    try:
        url = f"{DOTNET_API_URL}/api/books/{book_id}/availability"
        resp = requests.get(url, timeout=1.5)
        if resp.status_code == 200:
            data = resp.json()
            is_avail = data.get("isAvailable", False)
            title = data.get("title", f"Book #{book_id}")
            return f"Book '{title}' (ID: {book_id}) is currently {'Available to borrow' if is_avail else 'Checked out / borrowed'}."
    except Exception:
        pass

    # Fallback to local catalog
    item = LOCAL_AVAILABILITY.get(book_id)
    if item:
        status_str = "Available to borrow" if item["isAvailable"] else "Checked out / borrowed"
        return f"Book '{item['title']}' (ID: {book_id}) is currently {status_str}."
    return f"Book ID {book_id} was not found in the catalog."


# -------------------------------------------------------------
# 2. Binding Tools to Model
# -------------------------------------------------------------
base_model = get_chat_model()
tools = [check_book_availability]
tools_by_name = {t.name: t for t in tools}

if hasattr(base_model, "bind_tools"):
    model_with_tools = base_model.bind_tools(tools)
else:
    model_with_tools = base_model


def extract_text(content: Any) -> str:
    """Extracts string representation from AIMessage content list or string."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        texts = [item.get("text", "") for item in content if isinstance(item, dict) and "text" in item]
        if texts:
            return " ".join(texts)
    return str(content)


# -------------------------------------------------------------
# 3. Demonstration & Round-Trip Execution
# -------------------------------------------------------------
def run_tool_calling_demo():
    print("==================================================================")
    print(" WEEK 6 PART D: LANGCHAIN TOOL CALLING & .NET AVAILABILITY DEMO")
    print(f" Active Model Provider: {type(base_model).__name__}")
    print("==================================================================")

    # ---------------------------------------------------------
    # Test 1: Query that MUST trigger tool (Availability Check)
    # ---------------------------------------------------------
    q1 = "Is book 4 available right now to borrow?"
    print(f"\n[Test 1] User asks: '{q1}'")
    msg1 = HumanMessage(content=q1)
    ai_response1 = model_with_tools.invoke([msg1])

    if ai_response1.tool_calls:
        print(f"  [+] Model Decision: Live tool invocation required!")
        for call in ai_response1.tool_calls:
            print(f"      - Tool requested: {call['name']}")
            print(f"      - Tool arguments: {call['args']}")
            
            # Execute the tool
            target_tool = tools_by_name.get(call["name"])
            tool_output = target_tool.invoke(call["args"]) if target_tool else "Tool not found"
            print(f"      - Execution Output: \"{tool_output}\"")
            
            # Feed back to model for final natural-language synthesis
            tool_msg = ToolMessage(content=tool_output, tool_call_id=call["id"])
            final_ai = model_with_tools.invoke([msg1, ai_response1, tool_msg])
            print(f"\n  [Synthesized Final Answer]:\n  {extract_text(final_ai.content)}")
    else:
        print(f"  [-] Model answered directly without tool: {extract_text(ai_response1.content)}")

    # ---------------------------------------------------------
    # Test 2: Query that should NOT trigger tool (Genre question)
    # ---------------------------------------------------------
    q2 = "What genre is Dune?"
    print(f"\n[Test 2] User asks: '{q2}'")
    ai_response2 = model_with_tools.invoke([HumanMessage(content=q2)])

    if ai_response2.tool_calls:
        print(f"  [-] Model called tool unexpectedly: {ai_response2.tool_calls}")
    else:
        print("  [+] Model Decision: Answer directly from knowledge base (Zero tool calls required).")
        print(f"  [Direct Answer]:\n  {extract_text(ai_response2.content)}")

    # ---------------------------------------------------------
    # Test 3: Unavailable Book Query
    # ---------------------------------------------------------
    q3 = "Can I borrow book 2 today?"
    print(f"\n[Test 3] User asks: '{q3}'")
    msg3 = HumanMessage(content=q3)
    ai_response3 = model_with_tools.invoke([msg3])

    if ai_response3.tool_calls:
        call = ai_response3.tool_calls[0]
        tool_output = check_book_availability.invoke(call["args"])
        tool_msg = ToolMessage(content=tool_output, tool_call_id=call["id"])
        final_ai3 = model_with_tools.invoke([msg3, ai_response3, tool_msg])
        print(f"  [+] Tool result: \"{tool_output}\"")
        print(f"  [Synthesized Final Answer]:\n  {extract_text(final_ai3.content)}")


if __name__ == "__main__":
    run_tool_calling_demo()
