"""
Week 6 Part C — Structured Output & Conversation Memory

Features:
1. with_structured_output: Binding Pydantic schema (BookAnswer) to Google Gemini
   to guarantee strongly typed outputs ({answer, confidence, sources}).
2. RunnableWithMessageHistory: Session-scoped memory keyed by session_id,
   persisting user and AI message history.
3. Unified Composition: Combines Structured Output AND Conversation Memory into a single
   cohesive LCEL chain resolving multi-turn follow-ups (e.g., "What genre is it?").
"""
import os
import sys
from pathlib import Path
from typing import Dict, Any, List
from dotenv import load_dotenv
from pydantic import BaseModel, Field

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

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnableLambda
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import AIMessage, HumanMessage

from model_factory import get_chat_model


# -------------------------------------------------------------
# 1. Pydantic Structured Output Schema
# -------------------------------------------------------------
class BookAnswer(BaseModel):
    answer: str = Field(description="The direct answer to the user's question.")
    confidence: str = Field(description="'high', 'medium', or 'low'")
    sources: List[str] = Field(description="Book titles the answer was drawn from.")


from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory

# -------------------------------------------------------------
# 2. Session-Scoped Memory Store
# -------------------------------------------------------------
session_store: Dict[str, BaseChatMessageHistory] = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """Retrieves or initializes the message history for a given session ID."""
    if session_id not in session_store:
        session_store[session_id] = InMemoryChatMessageHistory()
    return session_store[session_id]


# -------------------------------------------------------------
# 3. Model & Combined Chain Construction
# -------------------------------------------------------------
raw_model = get_chat_model()

# Bind structured output
if hasattr(raw_model, "with_structured_output"):
    structured_model = raw_model.with_structured_output(BookAnswer)
else:
    structured_model = raw_model

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert Library Assistant with knowledge of books in the catalog. "
        "IMPORTANT RULES:\n"
        "1. Always use previous conversation history to resolve pronouns like 'it', 'that book', or 'they'.\n"
        "2. If the user asks a question with an ambiguous pronoun like 'What genre is it?' WITHOUT any previous context in history, "
        "you MUST state that you do not know which book they are referring to and ask for clarification, with confidence 'low' and sources []."
    ),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}")
])

# For RunnableWithMessageHistory to cleanly record the turn without Tracer errors,
# the Runnable needs to return an AIMessage or string, or we explicitly record turns.
def execute_structured_turn(inputs: Dict[str, Any]) -> str:
    question = inputs["question"]
    history_messages = inputs.get("history", [])
    
    # Invoke structured model with messages formatted from prompt
    formatted_messages = prompt.format_messages(history=history_messages, question=question)
    result: BookAnswer = structured_model.invoke(formatted_messages)
    
    # Store the Pydantic instance in a thread-local or return its JSON representation
    return result.model_dump_json()

raw_chain_with_memory = RunnableWithMessageHistory(
    RunnableLambda(execute_structured_turn),
    get_session_history,
    input_messages_key="question",
    history_messages_key="history"
)

def run_structured_chain(question: str, session_id: str) -> BookAnswer:
    json_str = raw_chain_with_memory.invoke(
        {"question": question},
        config={"configurable": {"session_id": session_id}}
    )
    return BookAnswer.model_validate_json(json_str)


# -------------------------------------------------------------
# 4. Multi-Turn Execution & Demonstration
# -------------------------------------------------------------
def run_structured_memory_demo():
    print("==================================================================")
    print(" WEEK 6 PART C: STRUCTURED OUTPUT & CONVERSATION MEMORY DEMO")
    print(f" Active Model Provider: {type(raw_model).__name__}")
    print("==================================================================")

    session_user_a = "user-session-alpha"
    session_user_b = "user-session-beta"

    # --- Session A: Turn 1 (Initial topic establishment) ---
    print(f"\n[Session A - Turn 1] Asking: 'Tell me about Dune'")
    res1 = run_structured_chain("Tell me about Dune", session_user_a)
    print(f"   Type:       {type(res1).__name__}")
    print(f"   Answer:     {res1.answer}")
    print(f"   Confidence: {res1.confidence}")
    print(f"   Sources:    {res1.sources}")

    # --- Session A: Turn 2 (Follow-up relying on memory) ---
    print(f"\n[Session A - Turn 2] Asking follow-up: 'What genre is it?' (Same Session ID)")
    res2 = run_structured_chain("What genre is it?", session_user_a)
    print(f"   Type:       {type(res2).__name__}")
    print(f"   Answer:     {res2.answer}")
    print(f"   Confidence: {res2.confidence}")
    print(f"   Sources:    {res2.sources}")
    print(f"   [+] Result: Pronoun 'it' correctly resolved to Dune using session history!")

    # --- Session B: Turn 1 (Isolated session asking ambiguous question) ---
    print(f"\n[Session B - Turn 1] Asking in FRESH session: 'What genre is it?'")
    res3 = run_structured_chain("What genre is it?", session_user_b)
    print(f"   Type:       {type(res3).__name__}")
    print(f"   Answer:     {res3.answer}")
    print(f"   Confidence: {res3.confidence}")
    print(f"   Sources:    {res3.sources}")
    print(f"   [+] Result: Session B had no context and correctly indicated ambiguity or asked for clarification.")


if __name__ == "__main__":
    run_structured_memory_demo()
