# Week 5 — Part E: FastAPI /ask Microservice Integration

## 📌 Executive Summary
**Week 5 — Part E** productionizes the manual RAG pipeline from Parts C & D by exposing it as a resilient, asynchronous HTTP microservice built on **FastAPI** and **Pydantic**. This endpoint accepts user queries, retrieves relevant vector chunks from ChromaDB, constructs a grounded prompt, invokes the model with defensive error handling, and returns structured answers with source attribution.

---

## 🏗️ Microservice Architecture & Data Flow

```
                      Client HTTP Request
                   POST http://127.0.0.1:8000/ask
                    { "question": "..." }
                               │
                               ▼
                    ┌─────────────────────┐
                    │ FastAPI Application │  (Pydantic Validation & CORS)
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ ChromaDB Vector DB  │  retrieve(question, k=3)
                    └──────────┬──────────┘
                               │
                               ▼ Top-3 Chunks + Metadata
                    ┌─────────────────────┐
                    │ build_prompt()      │  (Inject negative grounding constraint)
                    └──────────┬──────────┘
                               │
                               ▼ Bounded Prompt
                    ┌─────────────────────┐
                    │ LLM Service         │  (Google Gemini / Resilient Engine)
                    └──────────┬──────────┘
                               │
                               ▼ Grounded Answer + Source Metadata
                    ┌─────────────────────┐
                    │ HTTP 200 OK JSON    │  { "answer": "...", "sources": [...] }
                    └─────────────────────┘
```

---

## 🔑 Endpoint Specification

### `POST /ask`
- **Request Body (`application/json`):**
  ```json
  {
    "question": "Which books are science fiction in our library and what are they about?"
  }
  ```
- **Response Body (`200 OK`):**
  ```json
  {
    "answer": "Our library includes Dune by Frank Herbert, a science fiction novel set on the desert planet Arrakis revolving around Paul Atreides and the spice melange.",
    "sources": [
      "Dune"
    ]
  }
  ```
- **Out-of-Domain Response (`200 OK`):**
  ```json
  {
    "answer": "I don't have that information.",
    "sources": []
  }
  ```

---

## 🛡️ Defensive Engineering: Try/Except & Error Boundaries
To prevent server crashes on upstream LLM network timeouts or quota exhaustion:
```python
try:
    answer = generate_llm_response(prompt)
except Exception as ex:
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Upstream inference failed: {str(ex)}"
    )
```

---

## 🛠️ Execution & Interactive Documentation

### 1. Launch Server
```bash
# & "D:\Software\PythonEnvironments\AI_env\Scripts\python.exe" -m uvicorn app:app --reload --port 8000
```

### 2. Swagger / OpenAPI Documentation
Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser to interactively test the endpoint.

---

## 🎯 Task Sheet Checklist (Part E)
- [x] Defined Pydantic models: `AskRequest` and `AskResponse`.
- [x] Implemented `@app.post("/ask")` wiring retrieval, prompt construction, and generation.
- [x] Added clean try/except exception handling around the LLM call.
- [x] Verified `sources` field is populated with referenced books.
- [x] Ready for git checkpoint: `feat: add /ask endpoint wiring RAG pipeline into FastAPI service`.
