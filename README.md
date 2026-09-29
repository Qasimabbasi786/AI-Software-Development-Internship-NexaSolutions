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
| **[Week 03](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_03)** | **Enterprise Persistence, EF Core & Integration** | `In Progress (Parts A–E Done)` ⏳ | • Part A: PostgreSQL schema design, indexes, and queries.<br>• Part B: Entity Framework Core Code-First migrations & relations.<br>• Part C: Complete API integration with persistent storage.<br>• Part D: Authentication & Authorization architecture (JWT notes).<br>• Part E: Angular frontend client consuming persistent API.<br>• Parts F & G (Git Workflow & AI Scripts): Upcoming finalization. |

---

## 🗂️ Repository Directory Blueprint

```
All Week Tasks Sol/
├── .gitignore                                # Master ignore rules (bin, obj, node_modules, .env)
├── README.md                                 # Primary landing page & curriculum tracker
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
└── Week_03/                                  # WEEK 3: PERSISTENCE, EF CORE & AI (IN PROGRESS)
    ├── Week_03_PartA_PostgreSQL/             # Relational database setup & SQL scripts
    ├── Week_03_PartB_EFCore/                 # EF Core DBContext, models, migrations
    ├── Week_03_PartC_API_Integration/        # Persistent API endpoints
    ├── Week_03_PartD_Auth_Notes/             # Security, JWT tokens, auth architecture
    ├── Week_03_PartE_Angular_Integration/    # Frontend integration with persistent database
    ├── Week_03_PartF_Git_Workflow/           # Branching strategies & CI/CD workflow
    ├── Week_03_PartG_AIScripts/              # Python AI scripts & data automation
    └── Week_03_Final_Project/                # Enterprise integrated capstone
```

---

## ⚡ Quick Execution Guidelines

### 1. Launching .NET Backend Applications
```bash
# Example: Week 2 Library API
cd "Week_02/Week_02_Final_Project/libraryAPI"
dotnet restore
dotnet run
# Access interactive Swagger UI at http://localhost:5184/
```

### 2. Launching Angular Frontend Clients
```bash
# Example: Week 2 Library Management Client
cd "Week_02/Week_02_Final_Project/libraryFrontend"
npm install
npm start
# Access interactive application at http://localhost:4200/
```

---

## 🛡️ Engineering Values & Code Quality Standards
- **Clean Architecture:** Strict adherence to separation of concerns (Presentation $\to$ Service $\to$ Repository $\to$ Data Store).
- **Type Safety:** Nullable reference types enabled across C# projects, strict typing across TypeScript interfaces.
- **Defensive Programming:** Safe numeric parsing (`TryParse`), early input validation, structured status codes (`200`, `201`, `400`, `404`), and contextual form error states.
- **Git Hygiene:** Clean commit logs, complete documentation, and zero commit leakage of build binaries (`bin/`, `obj/`, `node_modules/`, secrets).

---
*Maintained by **Muhammad Qasim** | Nexa Solutions AI Software Development Internship.*
