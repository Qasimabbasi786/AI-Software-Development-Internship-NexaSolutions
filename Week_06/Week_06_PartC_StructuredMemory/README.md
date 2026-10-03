# Week 6 — Part C: Structured Output & Conversation Memory

## 🌟 Overview
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
        │                                                        │
        │  [SystemMessage]: "Expert Library Assistant..."        │
        │  [MessagesPlaceholder]: (Turn 1 User + Turn 1 AI...)   │
        │  [HumanMessage]: Current Question                      │
        └────────────────────────┬───────────────────────────────┘
                                 │
                                 ▼
        ┌────────────────────────────────────────────────────────┐
        │       Google Gemini (with_structured_output)           │
        │                                                        │
        │  Target Schema: class BookAnswer(BaseModel)            │
        │  - answer: str                                         │
        │  - confidence: Literal['high', 'medium', 'low']        │
        │  - sources: list[str]                                  │
        └────────────────────────┬───────────────────────────────┘
                                 │
                                 ▼
        ┌────────────────────────────────────────────────────────┐
        │       Auto-Validated Pydantic Instance Output          │
        │                                                        │
        │  BookAnswer(                                           │
        │    answer="Dune belongs to the science fiction genre.", │
        │    confidence="high",                                  │
        │    sources=["Dune"]                                    │
        │  )                                                     │
        └────────────────────────────────────────────────────────┘
```

---

## 🔍 Why `with_structured_output` Outperforms Manual Prompting

| Feature | Manual JSON Prompting (`json.loads`) | LangChain `with_structured_output` |
| :--- | :--- | :--- |
| **Output Guarantees** | Text output might contain markdown code blocks (````json ... ````), conversational chatter, or trailing commas. | Strictly enforced via schema binding and model function/tool calling protocol. |
| **Parsing Failures** | High under load or with complex multi-paragraph answers. Throws `JSONDecodeError`. | Built-in retry/repair parsing logic; yields strongly-typed Pydantic model instances. |
| **Type Validation** | Manual runtime validation needed for nested types, lists, and required keys. | Automatic Pydantic type validation and field documentation injection into model system prompts. |

---

## 👥 Multi-Turn Session Memory Comparison

We tested multi-turn follow-up queries across isolated user sessions:

```text
[Session A - Turn 1] Query: "Tell me about Dune"
   Type:       BookAnswer
   Answer:     Dune is a science fiction novel by Frank Herbert...
   Confidence: high
   Sources:    ['Dune']

[Session A - Turn 2] Follow-up: "What genre is it?" (Same Session ID)
   Type:       BookAnswer
   Answer:     Dune is a science fiction novel.
   Confidence: high
   Sources:    ['Dune']
   [+] Verification: The model resolved "it" directly to "Dune" via session history.

[Session B - Turn 1] Query: "What genre is it?" (FRESH Session ID)
   Type:       BookAnswer
   Answer:     I do not know which book you are referring to. Could you please specify the title of the book you are asking about?
   Confidence: low
   Sources:    []
   [+] Verification: Completely isolated from Session A; lacks prior turns, accurately requesting clarification.
```

---

## ⚠️ Known Limitations: In-Memory Session Storage

> [!WARNING]
> **Production Note on `InMemoryChatMessageHistory`**:
> The session store in this module uses an in-memory dictionary (`dict[str, BaseChatMessageHistory]`). 
> - **Process Lifetime:** Any server restart, deployment, or auto-scaling worker recycle destroys all active session states.
> - **Multi-Instance Scaling:** In a horizontally-scaled multi-container environment (Kubernetes / load-balanced FastAPI instances), requests from the same user hitting different nodes will fail to find prior turns.
> - **Production Requirement:** In enterprise deployments, this dictionary must be swapped for persistent, centralized storage such as **Redis** (`RedisChatMessageHistory`), **PostgreSQL**, or **DynamoDB**.

---

## 🚀 Execution

Run the Part C demonstration using the active virtual environment:

```powershell
& "D:\Software\PythonEnvironments\AI_env\Scripts\python.exe" structured_memory_demo.py
```
