# Week 6 — Part D: Tool Calling with LangChain & .NET Endpoint

## 📌 Executive Summary
Static RAG vector stores only contain historical context and cannot answer real-time questions about transactional state (such as whether a book is checked out or available right now).

**Tool Calling** enables the model to:
1. Recognize when user queries require live or transactional data that does not exist in vector embeddings.
2. Formulate and return structured function invocation arguments without executing the function itself.
3. Allow the application to execute the tool securely against the backend and feed the result back to synthesize a natural-language response.

---

## 🏗️ Architecture: Autonomous Tool-Calling Flow

```
   User Query: "Is book 4 available to borrow?"
                      │
                      ▼
   ┌────────────────────────────────────────────────────────┐
   │        Google Gemini with bind_tools([@tool])          │
   │                                                        │
   │  - Evaluates intent against tool schemas & docstrings  │
   │  - Autonomously determines tool necessity              │
   └──────────────────────────┬─────────────────────────────┘
                              │
               Tool Call Needed?
              ┌───────────────┴───────────────┐
              │ Yes                           │ No (General Q)
              ▼                               ▼
   ┌──────────────────────────┐    ┌──────────────────────────┐
   │ Returns Tool Call Object │    │ Direct Generation Answer │
   │ name: check_availability │    └──────────────────────────┘
   │ args: {"book_id": 4}     │
   └──────────┬───────────────┘
              │
              ▼
   ┌────────────────────────────────────────────────────────┐
   │      Execute Tool: GET /api/books/4/availability       │
   │      Result: "Dune (ID 4) is currently AVAILABLE"      │
   └──────────────────────────┬─────────────────────────────┘
                              │
                              ▼ ToolMessage(content=...)
   ┌────────────────────────────────────────────────────────┐
   │      Final LLM Synthesis (Natural Response)            │
   │ "Yes! Dune is currently available on the shelf."       │
   └────────────────────────────────────────────────────────┘
```

---

## 🔑 Core Concepts Mastered

### 1. The `@tool` Decorator
```python
@tool
def check_book_availability(book_id: int) -> str:
    """
    Check whether a specific library book (by its numeric ID) is currently available to borrow.
    Always use this tool when the user asks about availability, checkout status, or borrowing state.
    """
    ...
```
Docstrings and type hints serve as the LLM's system prompt instructions explaining when and how to call the function.

### 2. Binding Tools to Models
```python
model_with_tools = llm.bind_tools([check_book_availability])
```
Attaches OpenAPI-style JSON schemas to Gemini API requests.

### 3. Tool Execution Round-Trip
Feeding the tool result back into the prompt history as a `ToolMessage` gives the model the factual grounding needed to generate a clean final answer.

---

## 🛠️ Implementation Details (`tool_calling_demo.py`)

- **Backend Integration:** Calls .NET endpoint `GET /api/books/{id}/availability` with local catalog fallback.
- **Verification Command:**
  ```bash
  python Week_06_PartD_ToolCalling/tool_calling_demo.py
  ```
