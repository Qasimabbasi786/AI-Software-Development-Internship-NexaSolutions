# Week 4: JWT Authentication, Angular Auth & AI FastAPI Microservice

Welcome to **Week 4** of the **Nexa Solutions AI Software Development Internship** (in technical partnership with OriginSoft Consultancy).

Week 4 marks a significant transition:
- Moving from an authentication vocabulary/skeleton in Week 3 to a full, production-ready **JWT Authentication & Password Hashing** implementation in ASP.NET Core and PostgreSQL.
- Integrating end-to-end authentication in **Angular** using a centralized `AuthService`, functional HTTP interceptors (`authInterceptor`), and route guards (`authGuard`).
- Transitioning Python AI scripts from standalone command-line scripts to a structured **FastAPI Microservice** with Pydantic validations, LLM conversation memory, streaming, structured JSON output, and prompt injection defense.
- Leveling up the **Git & GitHub Workflow** through deliberate merge conflict creation and resolution, standardizing `.github/PULL_REQUEST_TEMPLATE.md`, and enforcing repository branch protection rules on `main`.

---

## 📁 Week 4 Architecture & Module Breakdown

```text
Week_04/
├── Week_04_Final_Project/           # Capstone: Integrated Secured Library App & FastAPI AI Microservice
│   ├── backend/                     # ASP.NET Core 8 Web API with JWT & Claims Authorization
│   ├── frontend/                    # Angular Standalone SPA with AuthService & Guards
│   ├── ai-services/                 # Dedicated AI service integration
│   └── README.md                    # Capstone documentation & data flow diagram
├── Week_04_PartA_AuthBackend/       # ASP.NET Core JWT Auth, Password Hashing & Role Authorization
│   └── README.md                    # In-depth guide for password hashing & JWT Bearer tokens
├── Week_04_PartB_AngularAuth/       # Angular Auth Integration (Service, Interceptor, Guards)
│   └── README.md                    # In-depth guide for Angular security flow & UI role gating
├── Week_04_PartC_FastAPIService/    # FastAPI AI Microservice (Google GenAI SDK)
│   ├── main.py                      # FastAPI app with /health, /summarize, and /genre-suggestion
│   ├── requirements.txt             # FastAPI, Uvicorn, Pydantic, google-genai
│   ├── .env.example                 # Environment configuration template (GEMINI_API_KEY)
│   └── README.md                    # Microservice setup & OpenAPI documentation
├── Week_04_PartD_LLMAPIs/           # Google Gemini API Deep-Dive
│   ├── 01_conversation_history.py   # Multi-turn conversational memory pattern
│   ├── 02_streaming.py              # Real-time token streaming with Gemini
│   ├── 03_structured_output.py      # Resilient JSON extraction and defensive parsing
│   ├── requirements.txt             # Dependencies for AI scripts
│   ├── .env.example                 # Gemini API key template
│   └── README.md                    # LLM API concepts guide
├── Week_04_PartE_PromptEngineering/ # Prompt Engineering & Injection Defense
│   ├── prompt_templates.py          # Production system prompts & few-shot templates
│   ├── prompt_comparison.py         # Zero-shot vs Few-shot vs Role-based demonstration
│   └── README.md                    # Prompt engineering patterns & adversarial testing
└── Week_04_PartF_GitPractice/       # Advanced Git Workflows
    └── README.md                    # Merge conflict resolution & Branch protection guide
```

---

## ⚙️ Environment & Tooling Prerequisites

For all operations during Week 4, use the following verified toolchain paths:

| Tool | Designated Executable / Environment Path |
| :--- | :--- |
| **Git** | `D:\Software\Git\cmd\git.exe` |
| **.NET SDK** | `D:\Software\dotnet\dotnet.exe` |
| **Python Interpreter** | `D:\Software\PythonEnvironments\AI_env\Scripts\python.exe` |
| **Python Pip** | `D:\Software\PythonEnvironments\AI_env\Scripts\pip.exe` |
| **PostgreSQL Database** | Host: `localhost:5432`, DB: `librarydb_week3`, User: `postgres` |

---

## 🎯 Weekly Milestones & Branch Strategy

| Part | Feature Branch | Deliverables |
| :--- | :--- | :--- |
| **Part A** | `feature/jwt-auth-backend` | ASP.NET Core JWT Bearer authentication, PBKDF2 `PasswordHasher<User>`, AuthController (`register`/`login`), and role-based endpoint protection. |
| **Part B** | `feature/angular-auth` | Angular `AuthService`, functional HTTP `authInterceptor`, `authGuard`, Login component, and dynamic role-based UI buttons (Add/Delete). |
| **Part C** | `feature/ai-fastapi-service` | FastAPI AI microservice with `/health` and `/summarize` Pydantic models and Swagger interactive docs. |
| **Part D & E**| `feature/prompt-engineering` | LLM conversation memory, streaming, resilient JSON parsing, few-shot prompt templates, and prompt injection defense. |
| **Part F** | `chore/pull-request-template` | GitHub PR template (`.github/PULL_REQUEST_TEMPLATE.md`), merge conflict resolution demo, and branch protection setup. |
