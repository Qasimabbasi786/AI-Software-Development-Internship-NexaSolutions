# Week 6 — Part C: Structured Output & Conversation Memory

## 📌 Executive Summary
In enterprise AI microservices, raw string generation and stateless HTTP requests are insufficient:
1. **Unreliable String Scraping:** Relying on LLMs to return markdown or plain text and hoping custom regex or `json.loads` doesn't throw a parsing exception fails under production load.
2. **Stateless Conversational Breakdown:** Multi-turn interactions require persistent history so users can ask contextual follow-up questions (e.g., *"Who is the author?"* or *"What genre is it?"*) without repeating previous context.

This module combines **Pydantic Structured Outputs (`with_structured_output`)** with **Session-Scoped Memory (`RunnableWithMessageHistory`)** into a unified, type-safe LangChain LCEL pipeline powered by **Google Gemini**.

---

## 🏗️ Architecture: Structured Memory Pipeline

```
  User Request ──> {"question": str, session_id: "user-42"}
                         │
                         ▼
        ┌────────────────────────────────────────────────────────┐
        │        RunnableWithMessageHistory Router               │
        │                                                        │
        │  1. Lookup session_id in session_store                 │
        │  2. Load prior conversation turns: BaseChatMessageHistory│
        │  3. Inject history into MessagesPlaceholder            │
        └────────────────────────┬───────────────────────────────┘
                                 │
                                 ▼
        ┌────────────────────────────────────────────────────────┐
        │            ChatPromptTemplate Composition              │
        │  - System Prompt (Grounding & Directives)              │
        │  - MessagesPlaceholder("history")                      │
        │  - HumanMessage("{question}")                          │
        └────────────────────────┬───────────────────────────────┘
                                 │
                                 ▼
        ┌────────────────────────────────────────────────────────┐
        │       Google Gemini with_structured_output             │
        │  - Enforces Pydantic BookAnswer schema                 │
        │  - Validates answer, confidence, sources               │
        └────────────────────────┬───────────────────────────────┘
                                 │
                                 ▼
        ┌────────────────────────────────────────────────────────┐
        │    Strongly Typed Output Object: BookAnswer            │
        │    {                                                   │
        │      answer: "Dune is a science fiction classic...",   │
        │      confidence: "high",                               │
        │      sources: ["Dune"]                                 │
        │    }                                                   │
        └────────────────────────────────────────────────────────┘
```

---

## 🔑 Core Concepts Mastered

### 1. Pydantic Structured Output
```python
class BookAnswer(BaseModel):
    answer: str = Field(description="Direct response to the question.")
    confidence: str = Field(description="'high', 'medium', or 'low'.")
    sources: List[str] = Field(description="Book titles referenced.")

structured_llm = llm.with_structured_output(BookAnswer)
```
Guarantees the model returns typed objects adhering strictly to schema rules.

### 2. Session-Scoped Memory Isolation
`RunnableWithMessageHistory` wraps an LCEL chain, resolving history dynamically via a factory function:
```python
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in session_store:
        session_store[session_id] = InMemoryChatMessageHistory()
    return session_store[session_id]
```
Enables accurate pronoun resolution (*"What genre is it?"* $\rightarrow$ resolves *"it"* to the previously discussed book).

---

## 🛠️ Implementation Details (`structured_memory_demo.py`)

- **Model:** Google Gemini (`gemini-3.5-flash-lite`).
- **Memory Store:** In-memory dictionary store keyed by `session_id`.
- **Verification Command:**
  ```bash
  python Week_06_PartC_StructuredMemory/structured_memory_demo.py
  ```
