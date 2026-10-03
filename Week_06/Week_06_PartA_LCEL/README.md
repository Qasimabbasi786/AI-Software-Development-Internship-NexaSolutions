# Week 6 — Part A: LangChain Fundamentals & LCEL

## 📌 Executive Summary
LangChain Expression Language (LCEL) standardizes models, prompts, retrievers, and parsers behind common `Runnable` interfaces composed with the declarative pipe operator (`|`).

This module implements:
1. **Dynamic Multi-Provider Model Factory**: Google Gemini (`ChatGoogleGenerativeAI`) as the primary default, backed by OpenAI / Anthropic fallbacks and offline deterministic mocks.
2. **`RunnableLambda` Input Guard**: Immediate rejection of trivial queries (< 3 chars) before reaching LLM or retrieval stages.
3. **`RunnablePassthrough` & Parallel Composition**: Forwarding context and raw questions concurrently.
4. **Data Type Tracing**: Precise tracking of type transitions across all chain hops.

---

## 🏗️ Architecture & Data Type Flow

```
                      ┌──────────────────────────────────────┐
                      │  Input: dict {"question": str}       │
                      └──────────────────┬───────────────────┘
                                         │
                                         ▼
                      ┌──────────────────────────────────────┐
                      │  RunnableLambda(guard_short_questions│
                      │  Validates len(question) >= 3        │
                      └──────────────────┬───────────────────┘
                                         │  Returns: dict {"question": str}
                                         ▼
                      ┌──────────────────────────────────────┐
                      │     Dict-of-Runnables Parallel       │
                      │ ┌──────────────────┬───────────────┐ │
                      │ │ retriever_runnable│ Runnable      │ │
                      │ │   | format_docs  │ Passthrough   │ │
                      │ └────────┬─────────┴───────┬───────┘ │
                      └──────────┼─────────────────┼─────────┘
        Returns: str (context)   │                 │ Returns: str (question)
                                 └────────┬────────┘
                                          │
                                          ▼
                      ┌──────────────────────────────────────┐
                      │  Output: dict {"context", "question"}│
                      └──────────────────┬───────────────────┘
                                         │
                                         ▼
                      ┌──────────────────────────────────────┐
                      │  ChatPromptTemplate.from_template    │
                      └──────────────────┬───────────────────┘
                                         │  Returns: PromptValue (ChatPromptValue)
                                         ▼
                      ┌──────────────────────────────────────┐
                      │  ChatGoogleGenerativeAI (Gemini)     │
                      │  (Configured via Model Factory)      │
                      └──────────────────┬───────────────────┘
                                         │  Returns: AIMessage
                                         ▼
                      ┌──────────────────────────────────────┐
                      │  StrOutputParser()                   │
                      └──────────────────┬───────────────────┘
                                         │  Returns: str
                                         ▼
                      ┌──────────────────────────────────────┐
                      │  Final Clean Natural Language Answer │
                      └──────────────────────────────────────┘
```

---

## 🔑 Core Concepts Mastered

### 1. Unified Runnable Protocol
Every component implements standard methods:
- `invoke()`: Synchronous processing.
- `ainvoke()`: Asynchronous processing.
- `stream()`: Synchronous token streaming.
- `astream()`: Asynchronous token streaming.
- `batch()`: Parallel batch evaluation.

### 2. Composable Pipe Syntax (`|`)
Instead of nesting functions like `parser(model(prompt(input)))`, LCEL chains them sequentially:
```python
chain = (
    RunnableLambda(guard_short_questions)
    | {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)
```

### 3. Early Failure & Input Guarding
By placing `RunnableLambda(guard_short_questions)` at the start of the sequence, empty or sub-3-character inputs fail fast before incurring latency, database lookups, or API usage costs.

---

## 🛠️ Implementation Details (`lcel_rag_demo.py`)

- **Model Factory:** `model_factory.py` loads `GEMINI_API_KEY` from local `.env` and defaults to `gemini-3.5-flash-lite`.
- **Offline Deterministic Fallback:** Automatically activated if no API keys are present.
- **Verification Command:**
  ```bash
  python Week_06_PartA_LCEL/lcel_rag_demo.py
  ```
