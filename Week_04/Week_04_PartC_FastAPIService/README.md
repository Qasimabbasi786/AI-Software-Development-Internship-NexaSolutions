# Week 4 - Part C: FastAPI Foundations (Python AI Backend)

## 🎯 Objectives
- Transform standalone AI scripts into a dedicated, modular **FastAPI** web service.
- Understand automatic request/response validation using **Pydantic** models.
- Explore automatic interactive API documentation with **Swagger UI** (`/docs`) and **ReDoc** (`/redoc`).
- Run the service asynchronously using **Uvicorn**.

## 🚀 How to Run the Service

```bash
cd Week4_PartC_FastAPIService

# 1. Create and activate virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure .env file
copy .env.example .env

# 4. Start the server
uvicorn main:app --reload --port 8000
```

### 📖 Interactive Swagger Documentation
Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser.

## 📡 Endpoints Overview
- `GET /health` : Service health status
- `POST /summarize` : Structured JSON summary and genre extraction
- `POST /genre-suggestion` : Genre prediction based on book synopsis

## 🌿 Git Checkpoint
```bash
git checkout -b feature/ai-fastapi-service
git commit -m "feat: scaffold FastAPI AI service with health and summarize endpoints"
```
