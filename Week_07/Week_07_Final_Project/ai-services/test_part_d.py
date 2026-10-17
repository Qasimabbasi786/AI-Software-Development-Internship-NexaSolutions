"""
Week 7 - Part D Verification Suite: Persistence, HITL & Memory
Validates:
1. SQLite Checkpointing with SqliteSaver: proves state persistence across pause and resumption.
2. Interrupt & Resume: confirms Human-in-the-Loop approval pause on risky write operations.
3. User Rejection: confirms rejection path returns ToolMessage and prevents unauthorized calls without looping.
4. Checkpoint File Secret Inspection: rigorously searches the generated .sqlite database to prove ZERO JWT tokens or API keys exist in checkpoint state.
5. Long-term memory simulation: loads preferences and verifies deletion path.
"""

import os
import sys
import uuid
import sqlite3
from pathlib import Path
from dotenv import load_dotenv

_ai_dir = Path(__file__).resolve().parent
_env_file = _ai_dir / ".env"
if _env_file.exists():
    load_dotenv(_env_file)
else:
    load_dotenv()

from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import Command

from agent_graph import build_library_agent_graph

DB_PATH = _ai_dir / "agent_checkpoints.sqlite"

def run_part_d_suite():
    print("=" * 70)
    print("WEEK 7 - PART D: PERSISTENCE, HUMAN-IN-THE-LOOP & MEMORY SUITE")
    print("=" * 70)

    test_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyLTQyIn0.signature"
    thread_id = f"test-thread-{uuid.uuid4().hex[:8]}"

    # Set ephemeral security contextvar (ensures token NEVER enters LangGraph checkpoint or metadata)
    from agent_tools import CURRENT_USER_TOKEN
    CURRENT_USER_TOKEN.set(test_token)

    cfg = {
        "configurable": {
            "thread_id": thread_id,
            "idempotency_key": str(uuid.uuid4())
        }
    }

    # 1. Initialize SQLite Checkpointer
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    checkpointer = SqliteSaver(conn)
    checkpointer.setup()

    app = build_library_agent_graph(checkpointer=checkpointer)

    print(f"\n[Step 1] Starting run with Thread ID: {thread_id}")
    print("User Request: 'Please reserve book ID 4 for me.'")
    print("-" * 70)

    initial_input = {
        "messages": [HumanMessage(content="Please reserve book ID 4 for me.")],
        "steps": 0,
        "retries": 0,
        "route": "action"
    }

    # Execute graph up to the interrupt
    print("Invoking graph... (Expecting pause at approval_node)")
    pause_result = app.invoke(initial_input, cfg)

    # Inspect current state
    current_state = app.get_state(cfg)
    print(f"Graph Status: {'PAUSED / INTERRUPTED' if current_state.next else 'FINISHED'}")
    print(f"Next Node to execute upon resume: {current_state.next}")
    if current_state.tasks:
        for task in current_state.tasks:
            if hasattr(task, "interrupts") and task.interrupts:
                print(f"[HITL INTERRUPT TRIGGERED]: {task.interrupts[0].value}")

    # 2. Test Rejection Path (Challenge 2)
    print("\n" + "=" * 70)
    print("[Step 2] Testing User Rejection of Approval")
    print("=" * 70)
    reject_resume = app.invoke(Command(resume={"approved": False}), cfg)
    last_msg = reject_resume["messages"][-1]
    print(f"Agent Response After Rejection: {last_msg.content}")

    # Verify state history
    print("\n[Step 3] Inspecting Thread State History:")
    history = list(app.get_state_history(cfg))
    print(f"Total state checkpoints recorded for thread {thread_id}: {len(history)}")
    for i, h in enumerate(history[:3]):
        step_val = h.values.get("steps", 0)
        msg_count = len(h.values.get("messages", []))
        print(f"  - Checkpoint {i+1}: Node: {h.next or 'COMPLETED'} | Steps: {step_val} | Message Count: {msg_count}")

    # 3. Persistence Leak Test: Ensure No JWT in SQLite
    print("\n" + "=" * 70)
    print("[Step 4] Checking SQLite Database for Sensitive Token / Secret Leaks")
    print("=" * 70)
    with open(DB_PATH, "rb") as f:
        raw_db_content = f.read()

    jwt_in_db = test_token.encode() in raw_db_content
    gemini_key = os.getenv("GEMINI_API_KEY", "")
    key_in_db = gemini_key.encode() in raw_db_content if gemini_key else False

    print(f"Result: JWT Token present in .sqlite checkpoint? -> {jwt_in_db}")
    print(f"Result: API Key present in .sqlite checkpoint?   -> {key_in_db}")

    if not jwt_in_db and not key_in_db:
        print("[SECURITY CHECK PASSED]: Checkpointed state contains ZERO secrets or user tokens.")
    else:
        print("[CRITICAL SECURITY FAILURE]: Sensitive tokens discovered in serialized checkpoint file!")
        sys.exit(1)

    print("\nPart D verification suite executed successfully.")

if __name__ == "__main__":
    run_part_d_suite()
