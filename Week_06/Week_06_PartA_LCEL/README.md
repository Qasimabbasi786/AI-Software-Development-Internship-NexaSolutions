# Week 6 — Part A: LangChain Fundamentals & LCEL

## 🌟 Overview
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
                      │  Final Clean Text Response           │
                      └──────────────────────────────────────┘
```

---

## 🔍 Data Type Tracing Specification

| Step | Component / Stage | Input Type | Output Type | Responsibility |
| :--- | :--- | :--- | :--- | :--- |
| **0** | Caller Input | `dict` | `dict` | `{"question": "Which books are science fiction in the catalog?"}` |
| **1** | `RunnableLambda(guard_short_questions)` | `dict` | `dict` | Validates question length >= 3 characters. Rejects `?` or `hi` with `ValueError`. |
| **2a**| `retriever_runnable` | `dict` or `str` | `list[Document]` | Retrieves matching catalog documents based on keyword/semantic matches. |
| **2b**| `format_docs` | `list[Document]` | `str` | Formats extracted documents into a delimited context string. |
| **2c**| `RunnablePassthrough` | `dict` | `str` | Extracts and forwards original `question` string unchanged. |
| **2d**| Parallel Dict Step Output | N/A | `dict` | Maps to `{"context": str, "question": str}` matching prompt variables. |
| **3** | `ChatPromptTemplate` | `dict` | `PromptValue` | Formats systemic and human messages with contextual slots. |
| **4** | `ChatGoogleGenerativeAI` | `PromptValue` | `AIMessage` | Executes Gemini LLM inference and produces AIMessage chunk. |
| **5** | `StrOutputParser` | `AIMessage` | `str` | Extracts string content, stripping extra metadata envelopes. |

---

## 🛡️ Input Guard Verification & Stack Trace Analysis

When invoking the chain with an invalid query (such as `{"question": "?"}`), the exception is intercepted at **Step 1** before reaching the retriever or LLM:

```text
Traceback (most recent call last):
  File "lcel_rag_demo.py", line 137, in run_lcel_demo
    chain.invoke({"question": "?"})
  File "langchain_core/runnables/base.py", line 2875, in invoke
    input = step.invoke(input, config, **kwargs)
  File "lcel_rag_demo.py", line 36, in guard_short_questions
    raise ValueError(f"InputGuard: Question '{question}' is too short (< 3 chars) to answer meaningfully.")
ValueError: InputGuard: Question '?' is too short (< 3 chars) to answer meaningfully.
```

### Why LCEL Input Guards Outperform Ad-Hoc Application Logic:
1. **Zero Resource Wastage:** Expensive vector database queries and LLM API roundtrips are completely bypassed.
2. **Framework Composability:** The guard is an intrinsic step in the `RunnableSequence`, meaning it runs automatically whether invoked via `.invoke()`, `.stream()`, or `.batch()`.
3. **Decoupled Business Logic:** The guard function remains a pure, testable Python function without depending on external web controllers.

---

## 🚀 Execution

Run the demo using the active Python environment:

```powershell
& "D:\Software\PythonEnvironments\AI_env\Scripts\python.exe" lcel_rag_demo.py
```
