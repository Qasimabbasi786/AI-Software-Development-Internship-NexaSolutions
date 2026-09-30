# Week 4 - Part C: FastAPI Foundations (Python AI Backend)

## 📌 Executive Summary
In Week 3, the AI track was executed as a standalone command-line Python script. In **Week 4 - Part C**, we architect and stand up a structured, production-ready **FastAPI AI Microservice**. This microservice introduces automatic Pydantic request/response validation, interactive Swagger/OpenAPI documentation, prompt-engineered book summarization, and genre classification backed by **Google Gemini API (`gemini-1.5-flash`)**.

---

## 🏗️ Architecture & Endpoint Overview

```
                      FastAPI AI Microservice (:8000)
┌────────────────────────────────────────────────────────────────────────┐
│                                                                        │
│   GET  /health            ──► Returns liveness status & service docs   │
│                                                                        │
│   POST /summarize         ──► Pydantic Validation: SummaryRequest      │
│                               ├── Title (min_length=1)                 │
│                               └── Description (min_length=10)          │
│                                          │                             │
│                                          ▼                             │
│                               Engineered Prompt Template               │
│                               (Few-Shot + System Persona)              │
│                                          │                             │
│                                          ▼                             │
│                               Google Gemini API Call                   │
│                                          │                             │
│                                          ▼                             │
│                               Defensive JSON Parser                    │
│                               (Markdown Stripper + Fallback)           │
│                                          │                             │
│                                          ▼                             │
│                               SummaryResponse                          │
│                               { "title", "genre", "summary", ... }     │
│                                                                        │
│   POST /genre-suggestion  ──► Secondary Pydantic validation route      │
│                               Taxonomy classification & confidence     │
│                                                                        │
│   GET  /docs              ──► Interactive OpenAPI / Swagger UI         │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Step-by-Step Execution Guide

### 1. Dedicated Python Virtual Environment
All dependencies (`fastapi`, `uvicorn`, `pydantic`, `google-genai`, `python-dotenv`) are installed strictly in the dedicated virtual environment:
- **Python Interpreter:** `D:\Software\PythonEnvironments\AI_env\Scripts\python.exe`
- **Pip Executable:** `D:\Software\PythonEnvironments\AI_env\Scripts\pip.exe`

### 2. Environment Configuration (`.env`)
The `.env` file is present in `Week_04_PartC_FastAPIService/.env` and securely excluded from Git commits via `.gitignore`:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```
An `.env.example` file is provided for environment documentation:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 3. Launching the FastAPI Microservice
Run the following PowerShell command inside this directory:
```powershell
cd "Week_04/Week_04_PartC_FastAPIService"

# Start Uvicorn ASGI server with hot-reload enabled
& "D:\Software\PythonEnvironments\AI_env\Scripts\python.exe" -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Once running, access:
- **Interactive Swagger Documentation:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc Documentation:** [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Health Probe:** [http://localhost:8000/health](http://localhost:8000/health)

---

## 📡 API Endpoints Reference

### 1. `GET /health`
Verifies microservice availability and provider details.
- **Response (`200 OK`):**
```json
{
  "status": "ok",
  "service": "Nexa Solutions Library AI Microservice",
  "provider": "Google Gemini API (gemini-1.5-flash)",
  "version": "1.0.0",
  "docs_url": "/docs"
}
```

### 2. `POST /summarize`
Generates a structured literary summary and genre classification.
- **Request Body (`SummaryRequest`):**
```json
{
  "title": "Clean Code",
  "description": "A handbook of agile software craftsmanship explaining naming conventions, error handling, refactoring, and code hygiene."
}
```
- **Response (`200 OK`):**
```json
{
  "title": "Clean Code",
  "genre": "Software Engineering",
  "summary": "Clean Code teaches software craftsmanship principles, refactoring techniques, and naming conventions to write readable and maintainable code.",
  "model": "gemini-1.5-flash",
  "provider": "Google Gemini AI",
  "resilient_parsing": true,
  "status": "success"
}
```
- **Automatic Validation Error (`422 Unprocessable Entity`):**
  If `description` is omitted or too short, FastAPI automatically returns:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "description"],
      "msg": "Field required"
    }
  ]
}
```

### 3. `POST /genre-suggestion`
Accepts a title and synopsis to classify literary domains with a confidence score.
- **Request Body (`GenreSuggestionRequest`):**
```json
{
  "title": "The Pragmatic Programmer",
  "description": "Journeyman to master: modern techniques, tips, and career advice for programmers."
}
```
- **Response (`200 OK`):**
```json
{
  "title": "The Pragmatic Programmer",
  "suggested_genre": "Computer Science & Programming",
  "confidence": 0.98,
  "categories": ["Technology", "Software Engineering", "Education"],
  "status": "success"
}
```

---

## 🛡️ Resilience & Defensive Parsing
Even when an LLM returns stray conversational tokens or markdown code blocks (` ```json ... ``` `), `main.py` uses `parse_llm_json_defensive`:
1. Strips markdown fences.
2. Extracts balanced JSON brackets via regular expressions.
3. Fallbacks safely to structured defaults if parsing fails, completely preventing internal `500 Server Errors`.

---

## 🌿 Git Checkpoint
```bash
git checkout -b feature/ai-fastapi-service
git add .
git commit -m "feat: scaffold FastAPI AI service with health and summarize endpoints"
```
