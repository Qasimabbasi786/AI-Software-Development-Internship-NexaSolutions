# 💾 Enterprise Persistence, Relational Design & EF Core
### Week 3: PostgreSQL Schema Design, EF Core Migrations & Angular API Client

**Author:** Muhammad Qasim  
**Program:** AI Software Development Internship (.NET + Angular + AI)  
**Milestone:** Week 3 — Persistence & Enterprise Architecture  

[![.NET 8](https://img.shields.io/badge/.NET-8.0-512BD4?logo=dotnet&logoColor=white)](https://dotnet.microsoft.com/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL_16-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![EF Core](https://img.shields.io/badge/ORM-Entity_Framework_Core-512BD4?logo=dotnet&logoColor=white)](https://learn.microsoft.com/ef/core/)
[![Angular](https://img.shields.io/badge/Angular-18-DD0031?logo=angular&logoColor=white)](https://angular.dev/)
[![Status: Completed](https://img.shields.io/badge/Status-Completed_%E2%9C%85-success)](https://github.com/)

---

## 📌 Internship Overview & Scope
This repository folder contains the complete, production-ready technical implementations for **Week 3** of the 8-Week AI Software Development Internship. 

Week 3 transitions from basic single-table concepts into normalized relational database design, Entity Framework Core ORM with PostgreSQL, RESTful API integration, Angular SPA frontend connectivity, professional Git feature-branching workflows, and foundational AI/LLM Python scripting.

---

## 🏗️ Master Repository Structure

```text
Week_03/
├── README.md                           # Master Week 3 technical overview
├── .gitignore                          # Root ignore file (.NET binaries, node_modules, .venv, .env)
├── Week_03_PartA_PostgreSQL/           # Relational Database Design (DDL, DML, DQL Scripts)
├── Week_03_PartB_EFCore/               # Entity Framework Core ORM with Npgsql Provider
├── Week_03_PartC_API_Integration/      # ASP.NET Core Web API + PostgreSQL Repository Swap
├── Week_03_PartD_Auth_Notes/           # Authentication & Authorization Theory, JWT, Hashing
├── Week_03_PartE_Angular_Integration/  # Angular 18+ SPA Client + RxJS HttpClient Integration
├── Week_03_PartF_Git_Workflow/         # Professional Git Branching & Conventional Commits
├── Week_03_PartG_AIScripts/            # Python LLM Foundation Script & Prompt Experiments
└── Week_03_Project/                    # Integrated Database-Backed Library Portal Solution
```

---

## 🛠️ Summary of Week 3 Modules & Implementations

### 1. Part A — Relational Database Design (PostgreSQL)
- **Folder**: [`Week_03_PartA_PostgreSQL`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/Week-03_and_04/Week_03/Week_03_PartA_PostgreSQL/README.md)
- **Highlights**: Localized database schema (`librarydb_week3`) for Islamabad literature (Faiz Ahmed Faiz, Bapsi Sidhwa, Dr. Tariq Rahman).
- **Key Concepts**: Primary/Foreign Keys, One-to-Many (`Authors` -> `Books`), Many-to-Many (`BookCategories` junction table), `INNER JOIN` queries, and referential integrity (`ON DELETE RESTRICT`).

### 2. Part B — Entity Framework Core with PostgreSQL
- **Folder**: [`Week_03_PartB_EFCore`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/Week-03_and_04/Week_03/Week_03_PartB_EFCore/README.md)
- **Highlights**: Object-Relational Mapping configured using `Npgsql.EntityFrameworkCore.PostgreSQL`.
- **Key Concepts**: Domain entity modeling, `LibraryDbContext` session management, dynamic `.env` connection loading, LINQ CRUD operations, and EF Core migration commands (`dotnet ef migrations add InitialCreate`).

### 3. Part C — API & Database Integration
- **Folder**: [`Week_03_PartC_API_Integration`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/Week-03_and_04/Week_03/Week_03_PartC_API_Integration/README.md)
- **Highlights**: Swapped temporary in-memory list storage with EF Core PostgreSQL `BookRepository`.
- **Key Concepts**: Layered architecture contract preservation, Dependency Injection (`IBookRepository`), CORS policy enabling (`AllowAngularApp`), JSON cycle reference suppression (`ReferenceHandler.IgnoreCycles`), and graceful `404 Not Found` error handling.

### 4. Part D — Authentication Concepts (Understand First, Build Later)
- **Folder**: [`Week_03_PartD_Auth_Notes`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/Week-03_and_04/Week_03/Week_03_PartD_Auth_Notes/README.md)
- **Highlights**: Comprehensive security documentation and sequence flow diagrams.
- **Key Concepts**: AuthN vs. AuthZ, One-Way Cryptographic Hashing with Salt (BCrypt), JWT Anatomy (Header, Payload/Claims, Signature), Base64Url decoding, and Role-Based Access Control (RBAC).

### 5. Part E — Angular API Integration
- **Folder**: [`Week_03_PartE_Angular_Integration`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/Week-03_and_04/Week_03/Week_03_PartE_Angular_Integration/README.md)
- **Highlights**: Angular 18+ standalone frontend SPA connected to live ASP.NET Core API.
- **Key Concepts**: Global `provideHttpClient(withFetch())`, `BookService` with RxJS `Observables`, `catchError` handlers, component state management (`isLoading`, `errorMessage`), Bootstrap 5 UI styling, and Reactive Forms for submitting new books.

### 6. Part F — Professional Git & GitHub Workflow
- **Folder**: [`Week_03_PartF_Git_Workflow`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/Week-03_and_04/Week_03/Week_03_PartF_Git_Workflow/README.md)
- **Highlights**: Standards for enterprise version control and pull request reviews.
- **Key Concepts**: Feature branching (`feature/*`), Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`), `.gitignore` secret protection, and release milestone tagging (`v0.3-week3`).

### 7. Part G — AI & Python Foundations (Kickoff)
- **Folder**: [`Week_03_PartG_AIScripts`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/Week-03_and_04/Week_03/Week_03_PartG_AIScripts/README.md)
- **Highlights**: Standalone Python script using `anthropic` SDK and `python-dotenv`.
- **Key Concepts**: AI/ML/DL/NLP/Generative AI hierarchy, LLMs, Training vs. Inference, Tokens, Context Windows, Hallucination analysis on fictional queries, and prompt engineering variations.

---

## 🔒 Security & Secret Management
All local configuration files (`.env`, `appsettings.Development.json`) containing real credentials or API keys are strictly excluded from source control via root [`.gitignore`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/Week-03_and_04/Week_03/.gitignore). Public `.env.example` templates are provided in relevant subfolders for environment setup.

---

## 📢 Milestone Tagging
```bash
git add .
git commit -m "feat: complete all Week 3 tasks including AI Python scripts and root README documentation"
git tag -a v0.3-week3 -m "Week 3 Completed: EF Core, PostgreSQL, Angular integration, and AI script"
git push origin main --tags
```
