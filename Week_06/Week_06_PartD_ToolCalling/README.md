# Week 6 — Part D: Tool Calling with LangChain & .NET Endpoint

## 🌟 Overview
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
                              ▼ Returns ToolCall schema:
                              │ {"name": "check_book_availability", "args": {"book_id": 4}}
                              │
   ┌──────────────────────────┴─────────────────────────────┐
   │            Application Tool Execution Step             │
   │                                                        │
   │  GET http://localhost:5000/api/books/4/availability    │
   │  -> Calls .NET 8 Web API / EF Core PostgreSQL          │
   │  -> Returns: {"bookId": 4, "isAvailable": true}        │
   └──────────────────────────┬─────────────────────────────┘
                              │
                              ▼ ToolMessage(content="Available to borrow")
                              │
   ┌──────────────────────────┴─────────────────────────────┐
   │             Model Synthesis Round-Trip                 │
   │                                                        │
   │  Input: [HumanMessage, AIMessage(ToolCall), ToolMsg]   │
   │  Output: "Yes, book 4 (Dune) is currently available    │
   │           to borrow."                                  │
   └────────────────────────────────────────────────────────┘
```

---

## 🔍 Tool Calling vs. Manual Function Execution

| Feature | Manual Programmatic Function Call | LangChain Autonomous Tool Calling |
| :--- | :--- | :--- |
| **Decision Maker** | The developer hardcodes `if "available" in query: check()` | The LLM decides dynamically based on context, semantics, and tool descriptions. |
| **Argument Extraction** | Brittle regex parsing to extract book IDs from unstructured text | Native JSON argument extraction matching the function's type annotations (`book_id: int`). |
| **Multi-Turn Synthesis** | Code must assemble a template string manually | Model receives tool output as context and crafts an empathetic, natural-sounding response. |

---

## 💻 .NET 8 Availability Endpoint
The .NET backend in `Week_06_Final_Project/backend` exposes:
- **Endpoint:** `GET /api/books/{id}/availability`
- **Controller Action:** [BooksController.cs](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_06/Week_06_Final_Project/backend/Controllers/BooksController.cs)
- **Response Format:**
  ```json
  {
    "bookId": 4,
    "isAvailable": true,
    "title": "Dune"
  }
  ```

---

## 📊 Live Verification Output

```text
==================================================================
 WEEK 6 PART D: LANGCHAIN TOOL CALLING & .NET AVAILABILITY DEMO
 Active Model Provider: ChatGoogleGenerativeAI
==================================================================

[Test 1] User asks: 'Is book 4 available right now to borrow?'
  [+] Model Decision: Live tool invocation required!
      - Tool requested: check_book_availability
      - Tool arguments: {'book_id': 4}
      - Execution Output: "Book 'Dune' (ID: 4) is currently Available to borrow."

  [Synthesized Final Answer]:
  Yes, book 4 (*Dune*) is currently available to borrow.

[Test 2] User asks: 'What genre is Dune?'
  [+] Model Decision: Answer directly from knowledge base (Zero tool calls required).
  [Direct Answer]:
  *Dune*, written by Frank Herbert and published in 1965, is widely considered a masterpiece of science fiction...

[Test 3] User asks: 'Can I borrow book 2 today?'
  [+] Tool result: "Book 'Designing Data-Intensive Applications' (ID: 2) is currently Checked out / borrowed."
  [Synthesized Final Answer]:
  No, book 2 ("Designing Data-Intensive Applications") is currently checked out and not available to borrow today.
```

---

## 🚀 Execution

Run the Part D demonstration using the active virtual environment:

```powershell
& "D:\Software\PythonEnvironments\AI_env\Scripts\python.exe" tool_calling_demo.py
```
