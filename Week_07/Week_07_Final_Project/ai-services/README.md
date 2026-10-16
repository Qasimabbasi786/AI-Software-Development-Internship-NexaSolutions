# Week 6 — AI Track: FastAPI Microservice (LangChain LCEL & Streaming)
### Google Gemini Standard (`langchain-google-genai` + `gemini-3.5-flash-lite`)

**Author:** Muhammad Qasim  
**Program:** AI Software Development Internship (.NET + Angular + AI)  
**Milestone:** Week 6 Final Project AI Microservice  

---

## 📌 Executive Summary
Welcome to the AI Microservice for the **Week 6 Final Project** in the **Nexa Solutions AI Software Development Internship Program**.

This service upgrades the basic prompt engineering and RAG pipeline from Weeks 4 & 5 into a composable, production-ready **LangChain LCEL microservice** featuring declarative pipe composition, semantic text splitting, `MultiQueryRetriever`, Pydantic structured output, session-scoped conversation memory, dynamic database tool calling, and low-latency Server-Sent Events (SSE) live streaming.

---

## 🏗️ Architecture & Component Workflow

```
┌────────────────────────────────────────────────────────┐
│             FastAPI AI Microservice (:8000)            │
│  - /health              -> Liveness & provider probe   │
│  - /ask                 -> Synchronous structured RAG  │
│  - /ask/stream          -> Live Server-Sent Events SSE │
└──────────────────────────┬─────────────────────────────┘
                           │ LCEL Pipeline (|)
                           ▼
┌────────────────────────────────────────────────────────┐
│               LangChain LCEL RAG Pipeline              │
│  - RunnableLambda(input_guard): Rejects queries < 3 ch │
│  - RecursiveCharacterTextSplitter: Semantic chunking   │
│  - MultiQueryRetriever: ChromaDB multi-perspective     │
│  - RunnableWithMessageHistory: Session memory isolation│
│  - @tool check_book_availability: Dynamic DB inquiry   │
└──────────────────────────┬─────────────────────────────┘
                           │ Google Gemini
                           ▼
┌────────────────────────────────────────────────────────┐
│             Google Gemini Model Integration            │
│  - Chat: gemini-3.5-flash-lite                         │
│  - Embeddings: models/gemini-embedding-001             │
│  - Async Generator (astream): Streaming chunks         │
└────────────────────────────────────────────────────────┘
```

---

## 📁 Directory Structure

```
ai-services/
├── main.py                     # Production FastAPI microservice with LCEL pipeline
├── model_factory.py            # Multi-provider model & embedding factory (Gemini primary)
├── requirements.txt            # Python dependencies (fastapi, langchain, chromadb, etc.)
├── summarize_book.py           # Standalone CLI book analysis tool
├── .env.example                # Safe environment variable template
├── .env                        # Local secret key file (gitignored)
└── README.md                   # Technical documentation and execution guide
```

---

## 🔒 Configuration & Environment (`.env`)

A dedicated `.env` file is placed inside this directory containing the Gemini API key and model configurations:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
GEMINI_MODEL=gemini-3.5-flash-lite
GEMINI_EMBEDDING_MODEL=models/gemini-embedding-001
DOTNET_API_URL=http://localhost:5000
```

---

## 🚀 Execution Guide

Run the AI Microservice using our dedicated virtual environment:

```powershell
# 1. Navigate to ai-services directory
cd "Week_06/Week_06_Final_Project/ai-services"

# 2. Start the FastAPI microservice with live reload
& "D:\Software\PythonEnvironments\AI_env\Scripts\python.exe" -m uvicorn main:app --reload --port 8000
```

### 📡 Available Endpoints

#### 1. Health Probe
```bash
curl -X GET "http://localhost:8000/health"
```

#### 2. Synchronous RAG with Tool Calling & Memory
```bash
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{
       "question": "Is book 4 available to borrow?",
       "session_id": "session_001"
     }'
```

#### 3. Real-Time Server-Sent Events (SSE) Streaming
```bash
curl -N -X POST "http://localhost:8000/ask/stream" \
     -H "Content-Type: application/json" \
     -d '{
       "question": "What does Clean Code teach?",
       "session_id": "session_001"
     }'
```

#### 4. Interactive OpenAPI Documentation
Open your browser to:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
