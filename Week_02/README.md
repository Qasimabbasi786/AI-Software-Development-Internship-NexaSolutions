# Week 2: Structured C# + ASP.NET Core Basics + Angular Forms
### Nexa Solutions Internship Program — Technical Documentation

Welcome to **Week 2** of the Nexa Solutions Software Engineering Internship. This week elevates your full-stack engineering proficiency: structuring intermediate C# code, designing enterprise-grade **ASP.NET Core Web APIs** with dependency injection, and building dynamic, validated frontends using **Angular Reactive Forms**.

---

## 📑 Week 2 Curriculum Navigation

| Module Directory | Topic Focus | Key Concepts & Implementations |
| :--- | :--- | :--- |
| **[Week_02_PartA](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_02/Week_02_PartA/README.md)** | **Intermediate C# & Clean Architecture** | Namespaces, project tiering, interfaces, Dependency Inversion (DIP), generic algorithms (`Swap<T>`), nullable reference types, enums, asynchronous programming (`async`/`await`), single responsibility principle (SRP), and small method pipelines. |
| **[Week_02_PartB](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_02/Week_02_PartB/README.md)** | **ASP.NET Core Web API Fundamentals** | HTTP REST protocol, request/response lifecycle, middleware pipeline, standard HTTP status codes (`200`, `201`, `400`, `404`), controller routing, DI lifetimes (Transient, Scoped, Singleton), `appsettings.json`, and interactive Swagger/OpenAPI documentation. |
| **[Week_02_PartD](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_02/Week_02_PartD/README.md)** | **Production Angular & Reactive Forms** | Singleton Angular services, RxJS `BehaviorSubject` reactive streams, Reactive Forms vs Template-Driven Forms, `FormBuilder`, synchronous validators (`required`, `email`, `minLength`), client-side routing (`router-outlet`, `routerLink`), and `HttpClient` concepts. |
| **[Week_02_Final_Project](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_02/Week_02_Final_Project/README.md)** | **Capstone: Library Management Suite** | Full-stack production architecture: ASP.NET Core API using the Controller-Service-Repository pattern, in-memory asynchronous persistence, CORS configuration, alongside an Angular client supporting complete CRUD with dual-mode (Create/Edit) reactive forms. |

---

## 🏗️ Architectural Flow & Integration

Week 2 connects backend services and web clients into a unified full-stack architecture:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        Angular Frontend Client                         │
│  ┌────────────────────────┐              ┌──────────────────────────┐  │
│  │    List Component      │              │ Reactive Form Component  │  │
│  │ (Display & Triggers)   │              │   (Validations & DTOs)   │  │
│  └───────────┬────────────┘              └────────────┬─────────────┘  │
│              │                                        │                │
│              └───────────────────┬────────────────────┘                │
│                                  ▼                                     │
│                     Angular Service (HttpClient)                       │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ HTTP / JSON (RESTful API)
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        ASP.NET Core Web API                            │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │     API Controller Layer (HTTP Verbs, Route Matching, Status)    │  │
│  └───────────────────────────────┬──────────────────────────────────┘  │
│                                  ▼                                     │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │     Service Layer (Business Logic & Validation Rules)            │  │
│  └───────────────────────────────┬──────────────────────────────────┘  │
│                                  ▼                                     │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │     Repository Layer (In-Memory / Persistence Abstraction)       │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack & Prerequisites

* **Backend:** [.NET 8.0 SDK](https://dotnet.microsoft.com/)
* **Frontend:** [Node.js](https://nodejs.org/) (v18+) & [Angular CLI](https://angular.dev/tools/cli) (v19/v22)
* **API Documentation:** Swagger / OpenAPI
* **Languages:** C# 12, TypeScript 5+, HTML5, CSS3

---

## 🚀 Quick Execution Guide

### 1. Running Part A (Intermediate C# Console)
```bash
cd "Week_02/Week_02_PartA"
dotnet run
```

### 2. Running Part B (ASP.NET Core Greeting API)
```bash
cd "Week_02/Week_02_PartB"
dotnet run
# Open browser to view Swagger at http://localhost:5xxx/
```

### 3. Running Part D (Angular Student Registration App)
```bash
cd "Week_02/Week_02_PartD"
npm install
npm start
# Navigate to http://localhost:4200/
```

### 4. Running the Week 2 Final Project (Library API + Angular Frontend)
```bash
# Terminal 1: Start Backend API (Port 5184)
cd "Week_02/Week_02_Final_Project/libraryAPI"
dotnet run

# Terminal 2: Start Frontend Application (Port 4200)
cd "Week_02/Week_02_Final_Project/libraryFrontend"
npm install
npm start
```

---

## 🎯 Key Learning Outcomes & Competencies

By completing Week 2, interns have demonstrated:
1. **Clean Code & Inversion of Control**: Applying Single Responsibility Principle, small orchestration methods, and dependency injection across both C# and Angular.
2. **RESTful API Engineering**: Designing predictable HTTP endpoints adhering to standard verbs (`GET`, `POST`, `PUT`, `DELETE`) and semantic HTTP status codes.
3. **Multi-Tiered Backend Systems**: Structuring backend applications using Controller-Service-Repository tiers for testability and maintainability.
4. **Enterprise Form UX**: Building robust Reactive Forms with synchronous validators, contextual error messaging, and dual-mode Create/Edit logic.
5. **Cross-Origin Client-Server Communication**: Configuring CORS policies in ASP.NET Core and consuming endpoints via Angular's `HttpClient`.
