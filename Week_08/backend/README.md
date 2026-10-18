# Week 6 Final Project — Backend API Service (`libraryAPI`)
### Enterprise ASP.NET Core 8 Web API + PostgreSQL + Polly Resilience + SSE Streaming Proxy

**Author:** Muhammad Qasim  
**Program:** AI Software Development Internship (.NET + Angular + AI)  
**Milestone:** Week 6 Final Project — Resilient Gateway & Streaming Proxy  

[![.NET: 8.0](https://img.shields.io/badge/.NET-8.0_Web_API-512BD4?logo=dotnet&logoColor=white)](https://dotnet.microsoft.com/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL_16-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Polly](https://img.shields.io/badge/Resilience-Polly_C%23-4CAF50)](https://github.com/App-vNext/Polly)
[![Status: Completed](https://img.shields.io/badge/Status-Completed_%E2%9C%85-success)](https://github.com/)

---

## 🏗️ Architecture & Data Flow

```
 HTTP Request (Angular Client :4200 / Postman / Swagger)
                     │
                     ▼
┌────────────────────────────────────────────────────────┐
│            Controllers (Presentation Layer)            │
│  - BooksController: CRUD + /availability endpoint      │
│  - AssistantController: /ask & /ask/stream proxy       │
│  - AuthController: JWT Authentication & User Claims    │
└──────────────────────────┬─────────────────────────────┘
                           │
       ┌───────────────────┴───────────────────┐
       ▼                                       ▼
┌──────────────────────────────┐ ┌──────────────────────────────┐
│  Repositories & Data Layer   │ │ Resilient Polly HTTP Client  │
│  - IBookRepository           │ │  - Typed IAiServiceClient    │
│  - LibraryDbContext (EF Core)│ │  - Exponential Retry (3x)    │
│  - PostgreSQL (5432)         │ │  - Circuit Breaker (30s break│
└──────────────────────────────┘ └─────────────┬────────────────┘
                                               │ HTTP / SSE Stream
                                               ▼
                                 ┌──────────────────────────────┐
                                 │ FastAPI AI Service (:8000)   │
                                 │ LangChain LCEL RAG + Gemini  │
                                 └──────────────────────────────┘
```

---

## 📁 Directory Structure

```
backend/
├── Controllers/
│   ├── AssistantController.cs     # Resilient proxy for /ask & /ask/stream (SSE)
│   ├── BooksController.cs         # RESTful CRUD + GET /api/books/{id}/availability
│   └── AuthController.cs          # JWT login & registration endpoints
├── Data/
│   └── LibraryDbContext.cs        # EF Core DbContext with relationship mappings
├── Models/
│   ├── Book.cs                    # Book entity with IsAvailable boolean
│   ├── Author.cs                  # Author entity (1:N with Book)
│   ├── Category.cs                # Category taxonomy entity
│   ├── BookCategory.cs            # Junction join entity
│   └── User.cs                    # User auth credentials entity
├── Repositories/
│   ├── IBookRepository.cs         # Repository contract abstraction
│   └── BookRepository.cs          # EF Core asynchronous data access methods
├── Services/
│   ├── IAiServiceClient.cs        # Typed client interface & DTOs
│   └── AiServiceClient.cs         # HttpClient proxy calling upstream FastAPI
├── appsettings.json               # Application settings
├── libraryAPI.csproj              # Project dependencies including Polly
└── Program.cs                     # DI container, JWT auth, and Polly policies
```

---

## 🔑 Key Capabilities Mastered

1. **Book Availability Tool Endpoint:**
   - Public endpoint `GET /api/books/{id}/availability` querying the `IsAvailable` flag in PostgreSQL for dynamic LangChain tool execution.
2. **Polly Resilience Policies:**
   - **Retry Policy:** Exponential backoff with 3 retry attempts for transient HTTP faults.
   - **Circuit Breaker Policy:** Breaks after 3 consecutive failures for 30 seconds, returning an immediate `503 Service Unavailable` response.
3. **End-to-End SSE Streaming Proxy:**
   - `POST /api/assistant/ask/stream` forwards live tokens from FastAPI directly to the client.
   - Leverages `HttpCompletionOption.ResponseHeadersRead` and `await Response.Body.FlushAsync()` to prevent internal socket buffering.

---

## 🚀 Execution Guide

```powershell
# 1. Navigate to backend directory
cd "Week_06/Week_06_Final_Project/backend"

# 2. Build the project
& "D:\Software\dotnet\dotnet.exe" build

# 3. Run the API on port 5000
& "D:\Software\dotnet\dotnet.exe" run --urls "http://localhost:5000"
```
- **Swagger Documentation:** `http://localhost:5000`
