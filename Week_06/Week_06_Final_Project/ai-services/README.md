# Week 4 - AI Track: FastAPI Microservice with Engineered Prompts
### Google GenAI SDK (`google-genai` + `gemini-3.8-flash`)

Welcome to the AI Microservice for the **Week 4 Final Project** in the **Nexa Solutions AI Software Development Internship Program**.

This service upgrades the standalone script from Week 3 into a production-ready, asynchronous **FastAPI microservice** featuring Pydantic schema validation, resilient JSON parsing error boundaries, and engineered few-shot prompt templates with prompt injection protection.

---

## 📌 Architecture & Design Decisions

### Why the .NET API & AI Service Remain Independent This Week
Connecting the .NET Core backend directly to the AI service now would mean the .NET API trusts a service that hasn't been evaluated for enterprise reliability, rate limiting, and vector embeddings yet. 
- **Weeks 5 & 6** introduce embeddings, RAG (Retrieval-Augmented Generation), vector databases, and orchestration.
- **Week 6** is where the real Angular → .NET API → FastAPI AI Service full-stack integration gets constructed on top of that robust foundation.
- For Week 4, both services operate independently and can be verified side-by-side.

```
┌────────────────────────────────────────────────────────┐
│             FastAPI AI Microservice (:8000)            │
│  - /health              -> Diagnostic status & provider│
│  - /summarize           -> Pydantic JSON + Gemini Flash│
│  - /genre-suggestion    -> Multi-category taxonomy     │
└──────────────────────────┬─────────────────────────────┘
                           │ Engineered Prompt + Defense
                           ▼
┌────────────────────────────────────────────────────────┐
│             Google GenAI SDK (google-genai)            │
│  - Model: gemini-3.8-flash                             │
│  - Persona: Senior Literary Cataloguer                 │
│  - Defense: Untrusted user data sandbox                │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
               Structured Validated JSON
```

---

## 📁 Directory Structure

```
ai-services/
├── main.py                     # Production FastAPI application
├── requirements.txt            # Python dependencies (fastapi, uvicorn, pydantic, google-genai)
├── summarize_book.py           # Standalone CLI execution script (gemini-3.8-flash)
├── .env.example                # Safe environment variable template
├── .env                        # Local secret key file (gitignored)
└── README.md                   # Technical documentation and execution guide
```

---

## 🔒 Configuration & Environment (`.env`)

A dedicated `.env` file is placed inside this directory containing the Gemini API key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

---

## 🚀 Execution Guide

Run the AI Microservice using our dedicated virtual environment:

```powershell
# 1. Navigate to ai-services directory
cd "Week_04/Week_04_Final_Project/ai-services"

# 2. Install dependencies (if not already installed)
& "D:\Software\PythonEnvironments\AI_env\Scripts\pip.exe" install -r requirements.txt

# 3. Start the FastAPI microservice with live reload
& "D:\Software\PythonEnvironments\AI_env\Scripts\python.exe" -m uvicorn main:app --reload --port 8000
```

### 📡 Testing the Endpoints

#### A. Health Probe
```bash
curl -X GET "http://localhost:8000/health"
```

#### B. Summarize & Genre Request
```bash
curl -X POST "http://localhost:8000/summarize" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Clean Architecture",
       "description": "A Craftsman Guide to Software Structure and Design by Robert C. Martin."
     }'
```

#### C. Interactive OpenAPI Documentation
Open your browser to:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
