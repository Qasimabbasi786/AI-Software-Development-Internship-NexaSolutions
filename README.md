# Nexa Solutions — AI Software Development Internship
### In Partnership with OriginSoft Consultancy | Engineering Portfolio

Welcome to the central repository for the **Nexa Solutions AI Software Development Internship** in technical partnership with **OriginSoft Consultancy**. This repository houses hands-on solutions, production-grade architectures, and incremental milestones demonstrating full-stack engineering proficiency spanning **C# / .NET**, **Angular & TypeScript**, **PostgreSQL / EF Core**, and **Python-driven AI solutions**.

---

## 👨‍💻 Engineer Information
- **Intern Name:** Muhammad Qasim
- **Track:** AI & Full-Stack Software Engineering
- **Organization:** Nexa Solutions (with OriginSoft Consultancy)
- **Repository Structure:** Modularized Week-by-Week Enterprise Milestones

---

## 🚀 Technology Stack Summary

```
┌────────────────────────────────────────────────────────────────────────┐
│                        Enterprise Technology Stack                     │
├─────────────────────┬───────────────────┬──────────────┬───────────────┤
│ Backend & APIs      │ Frontend & UI     │ Persistence  │ AI & Tooling  │
├─────────────────────┼───────────────────┼──────────────┼───────────────┤
│ • .NET 8 / 9 SDK    │ • Angular 18/19/22│ • PostgreSQL │ • Python 3.11+│
│ • C# 12 (Modern)    │ • TypeScript 5+   │ • EF Core 8  │ • NumPy/Pandas│
│ • ASP.NET Core API  │ • Reactive Forms  │ • In-Memory  │ • REST/OpenAPI│
│ • Controller-Service│ • RxJS Observables│ • Migrations │ • Swagger UI  │
│   -Repository tier  │ • CSS Glassmorphic│ • Connection │ • Git Workflow│
│ • LINQ & Generics   │   Modern Design   │   Pooling    │ • Node.js/npm │
└─────────────────────┴───────────────────┴──────────────┴───────────────┘
```

---

## 📊 Week-wise Progress Tracker

| Milestone | Curriculum Focus | Status | Key Deliverables & Highlights |
| :--- | :--- | :---: | :--- |
| **[Week 01](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_01/README.md)** | **Programming Foundations (C#/.NET + Angular/TS)** | `Completed` ✅ | • C# syntax, type safety, control flow, loops & algorithms.<br>• OOP principles: inheritance (`Person` -> `Student`/`Teacher`), interfaces (`IPrintable`).<br>• Generic collections (`List<T>`), defensive `try/catch`, and LINQ querying.<br>• Angular standalone components, two-way data binding, and glassmorphic UI.<br>• **Capstone:** Student Management Console + Angular Directory Portal. |
| **[Week 02](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_02/README.md)** | **Structured C# + ASP.NET Core + Angular Forms** | `Completed` ✅ | • Dependency Inversion (DIP), generic algorithms, async/await.<br>• ASP.NET Core REST API: HTTP verbs, status codes, Swagger/OpenAPI.<br>• Angular Reactive Forms with synchronous validators (`required`, `email`).<br>• Centralized state with RxJS `BehaviorSubject` & client routing.<br>• **Capstone:** Full-Stack Library Management System (ASP.NET Core API + Angular Reactive UI). |
| **[Week 03](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_03)** | **Enterprise Persistence, EF Core & Integration** | `Completed` ✅ | • Part A: PostgreSQL schema design, indexes, and queries.<br>• Part B: Entity Framework Core Code-First migrations & relations.<br>• Part C: Complete API integration with persistent storage.<br>• Part D: Authentication & Authorization architecture (JWT notes).<br>• Part E: Angular frontend client consuming persistent API.<br>• Parts F & G (Git Workflow & AI Scripts): Finalized and integrated into Capstone. |
| **[Week 04](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_04)** | **JWT Auth (.NET + Angular) & FastAPI AI Microservice** | `Completed` ✅ | • Part A: Real JWT issuing, password hashing (`PasswordHasher<User>`), and role-based endpoint authorization.<br>• Part B: Angular `AuthService`, functional HTTP interceptor, and `authGuard`.<br>• Part C: FastAPI AI Microservice with Pydantic validations & OpenAPI docs.<br>• Part D & E: LLM APIs in depth (`google-genai` + `gemini-3.8-flash`, history, streaming, prompt injection defenses).<br>• Part F: Git merge conflict resolution, branch protection, & PR template.<br>• **Capstone:** Secured Library App + AI Microservice with Engineered Prompts. |
| **[Week 05](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_05)** | **Embeddings, Vector Databases & Manual RAG Pipeline** | `In Progress` 🚀 | • Part A: Vector embeddings fundamentals, Cosine Similarity & top-$k$ semantic search.<br>• Part B: Local ChromaDB vector storage, collections & metadata filtering.<br>• Part C: Complete 8-stage manual RAG pipeline (chunking, embedding, storage, retrieval, context, generation, attribution).<br>• Part D: RAG quality evaluation, hallucination reduction & chunk trade-offs.<br>• Part E: FastAPI `/ask` endpoint wiring manual RAG pipeline.<br>• Part F: Safe Git commit undoing (`git revert`) on protected branches.<br>• **Capstone:** Library Knowledge Assistant with real .NET catalog corpus. |

---

## 🗂️ Repository Directory Blueprint

```
All Week Tasks Sol/
├── .gitignore                                # Master ignore rules (bin, obj, node_modules, .env)
├── README.md                                 # Primary landing page & curriculum tracker
├── .github/
│   └── PULL_REQUEST_TEMPLATE.md              # Standardized GitHub Pull Request Template
│
├── Week_01/                                  # WEEK 1: PROGRAMMING FOUNDATIONS
│   ├── README.md                             # Week 1 Executive Summary
│   ├── Week_01_PartA/                        # C# syntax, CLI, loops, calculator, FizzBuzz
│   ├── Week_01_PartB/                        # OOP, inheritance, interfaces (IPrintable)
│   ├── Week_01_PartC/                        # Collections, exceptions, and LINQ queries
│   ├── Week_01_PartD/                        # Angular standalone basics & glassmorphic roster
│   └── Week_01_Final_Project/                # Capstone: Student Management Suite (Console + Angular)
│
├── Week_02/                                  # WEEK 2: STRUCTURED APIS & REACTIVE FORMS
│   ├── README.md                             # Week 2 Executive Summary
│   ├── Week_02_PartA/                        # Advanced C#, DIP, generics, async/await pipelines
│   ├── Week_02_PartB/                        # ASP.NET Core API, HTTP codes, Swagger UI
│   ├── Week_02_PartD/                        # Angular Reactive Forms, validation, RxJS state
│   └── Week_02_Final_Project/                # Capstone: Library Management System
│       ├── libraryAPI/                       # Tiered ASP.NET Core Web API (Port 5184)
│       └── libraryFrontend/                  # Reactive Angular client with CRUD (Port 4200)
│
├── Week_03/                                  # WEEK 3: PERSISTENCE, EF CORE & AI
│   ├── Week_03_PartA_PostgreSQL/             # Relational database setup & SQL scripts
│   ├── Week_03_PartB_EFCore/                 # EF Core DBContext, models, migrations
│   ├── Week_03_PartC_API_Integration/        # Persistent API endpoints
│   ├── Week_03_PartD_Auth_Notes/             # Security, JWT tokens, auth architecture
│   ├── Week_03_PartE_Angular_Integration/    # Frontend integration with persistent database
│   ├── Week_03_PartF_Git_Workflow/           # Branching strategies & CI/CD workflow
│   ├── Week_03_PartG_AIScripts/              # Python AI scripts & data automation
│   └── Week_03_Final_Project/                # Enterprise integrated capstone
│
├── Week_04/                                  # WEEK 4: JWT AUTH & FASTAPI AI MICROSERVICE
│   ├── README.md                             # Week 4 Executive Summary & Overview
│   ├── Week_04_PartA_AuthBackend/            # ASP.NET Core JWT Auth, Password Hashing & Role Authorization
│   ├── Week_04_PartB_AngularAuth/            # Angular Auth Integration (Service, Interceptor, Guards)
│   ├── Week_04_PartC_FastAPIService/         # FastAPI AI Microservice with Pydantic Validations
│   ├── Week_04_PartD_LLMAPIs/                # Google GenAI SDK Deep-Dive (Parameters, History, Streaming)
│   ├── Week_04_PartE_PromptEngineering/      # Prompt Engineering, Few-Shot Templates & Injection Defense
│   ├── Week_04_PartF_GitPractice/            # Merge Conflict Simulation & Branch Protection Setup
│   └── Week_04_Final_Project/                # Capstone: Secured Library App + Independent AI Microservice
│       ├── backend/                          # Secured ASP.NET Core 8 Web API (:5000)
│       ├── frontend/                         # Role-Gated Angular 18/19 SPA (:4200)
│       └── ai-services/                      # FastAPI AI Microservice with Engineered Prompts (:8000)
│
└── Week_05/                                  # WEEK 5: EMBEDDINGS, VECTOR DBS & MANUAL RAG (GEMINI)
    ├── README.md                             # Week 5 Architecture & Guide (Google Gemini Standard)
    ├── requirements.txt                      # Dependencies (chromadb, google-genai, fastapi, uvicorn, numpy)
    ├── Week_05_PartA_Embeddings/             # Gemini text-embedding-004, Cosine Similarity & semantic search
    ├── Week_05_PartB_VectorDatabases/        # ChromaDB collections, L2 distance & metadata filtering
    ├── Week_05_PartC_RAGPipeline/            # Manual 8-stage RAG pipeline (chunking to source attribution)
    ├── Week_05_PartD_RAGEvaluation/          # RAG evaluation suite, chunk trade-offs & hit rate metrics
    ├── Week_05_PartE_FastAPIAsk/             # FastAPI microservice exposing grounded /ask endpoint
    ├── Week_05_PartF_GitRevert/              # Safe commit rollback walkthroughs using git revert
    └── Week_05_Final_Project/                # Library Knowledge Assistant & catalog grounding test suite
```

---

## ⚡ Quick Execution Guidelines

### 1. Launching .NET Backend Applications
```bash
# Example: Week 4 Secured Library API
cd "Week_04/Week_04_Final_Project/backend"
& "D:\Software\dotnet\dotnet.exe" restore
& "D:\Software\dotnet\dotnet.exe" run
# Access interactive Swagger UI at http://localhost:5000/swagger
```

### 2. Launching Angular Frontend Clients
```bash
# Example: Week 4 Secured Angular Client
cd "Week_04/Week_04_Final_Project/frontend"
npm install
npm start
# Access interactive application at http://localhost:4200/
```

### 3. Launching FastAPI AI Microservice
```powershell
# Example: Week 4 Final Project AI Microservice
cd "Week_04/Week_04_Final_Project/ai-services"

# Activate dedicated virtual environment and launch uvicorn
& "D:\Software\PythonEnvironments\AI_env\Scripts\python.exe" -m uvicorn main:app --reload --port 8000
# Access interactive OpenAPI Swagger UI at http://localhost:8000/docs
```

> [!NOTE]
> **Architectural Independence Note:** In Week 4, the .NET Web API and the FastAPI AI microservice operate as independent microservices. The direct Angular → .NET API → FastAPI AI integration pipeline will be connected in Week 6 after RAG and vector embeddings are integrated in Week 5.

---

## 🛡️ Engineering Values & Code Quality Standards
- **Clean Architecture:** Strict adherence to separation of concerns (Presentation $\to$ Service $\to$ Repository $\to$ Data Store).
- **Type Safety:** Nullable reference types enabled across C# projects, strict typing across TypeScript interfaces.
- **Defensive Programming:** Safe numeric parsing (`TryParse`), early input validation, structured status codes (`200`, `201`, `400`, `404`), and contextual form error states.
- **Git Hygiene:** Clean commit logs, complete documentation, and zero commit leakage of build binaries (`bin/`, `obj/`, `node_modules/`, secrets).

---
*Maintained by **Muhammad Qasim** | Nexa Solutions AI Software Development Internship.*
