# 🚀 Programming Foundations: C#/.NET & Angular
### Week 1: Type Safety, OOP, LINQ & Standalone Components

**Author:** Muhammad Qasim  
**Program:** AI Software Development Internship (.NET + Angular + AI)  
**Milestone:** Week 1 — Engineering Foundations  

[![.NET 8](https://img.shields.io/badge/.NET-8.0-512BD4?logo=dotnet&logoColor=white)](https://dotnet.microsoft.com/)
[![C# 12](https://img.shields.io/badge/C%23-12.0-239120?logo=csharp&logoColor=white)](https://learn.microsoft.com/dotnet/csharp/)
[![Angular](https://img.shields.io/badge/Angular-18-DD0031?logo=angular&logoColor=white)](https://angular.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Status: Completed](https://img.shields.io/badge/Status-Completed_%E2%9C%85-success)](https://github.com/)

---

Welcome to **Week 1** of the Nexa Solutions Software Engineering Internship. This week establishes foundational skills across modern full-stack web and enterprise development, bridging **C#/.NET** on the backend with **Angular/TypeScript** on the frontend.

---

## 📑 Week 1 Curriculum Navigation

| Module Directory | Topic Focus | Key Concepts & Exercises |
| :--- | :--- | :--- |
| **[Week_01_PartA](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_01/Week_01_PartA/README.md)** | **C# and .NET Basics** | .NET SDK vs Runtime, CLI lifecycle, primitive types, loops, defensive parsing (`TryParse`), Calculator, Even/Odd, FizzBuzz, Marks to Grade, Array Min/Max. |
| **[Week_01_PartB](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_01/Week_01_PartB/README.md)** | **Object-Oriented Programming (OOP)** | Classes vs Objects, properties, access modifiers, constructors, inheritance (`Person` -> `Student`/`Teacher`), interfaces (`IPrintable`), inheritance vs composition. |
| **[Week_01_PartC](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_01/Week_01_PartC/README.md)** | **Collections, Exceptions & LINQ** | Generic collections (`List<T>`, `Dictionary`, `HashSet`), `try/catch/finally` error handling, declarative querying with LINQ (`Where`, `Select`, `OrderByDescending`, `FirstOrDefault`). |
| **[Week_01_PartD](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_01/Week_01_PartD/README.md)** | **Angular & TypeScript Web Basics** | HTML5 semantic structure, CSS glassmorphism, TypeScript types & interfaces, Angular CLI, standalone components, data binding (interpolation, properties, events), services & DI. |
| **[Week_01_Final_Project](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_01/Week_01_Final_Project/README.md)** | **Capstone: Student Management System** | Complete dual-subsystem project: full CRUD C# Console management portal with analytics dashboard, alongside an interactive Angular client with live search and master-detail views. |

---

## 🏗️ Architecture Overview

The curriculum is structured to build skills progressively, moving from low-level procedural logic to modular enterprise web applications:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        Week 1 Learning Roadmap                         │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
       ┌────────────────────────────┼────────────────────────────┐
       ▼                            ▼                            ▼
┌──────────────┐             ┌──────────────┐             ┌──────────────┐
│    Part A    │             │    Part B    │             │    Part C    │
│  C# & .NET   │────────────►│  OOP Models  │────────────►│ Collections, │
│  Basics & CLI│             │  & Contracts │             │ Errors & LINQ│
└──────────────┘             └──────────────┘             └──────────────┘
                                                                 │
                                                                 ▼
       ┌─────────────────────────────────────────────────────────┴───────┐
       ▼                                                                 ▼
┌──────────────┐                                                  ┌──────────────┐
│    Part D    │                                                  │Final Project │
│ Angular & TS │─────────────────────────────────────────────────►│ Dual Portal  │
│ Web UI Engine│                                                  │ Suite (C#+Ng)│
└──────────────┘                                                  └──────────────┘
```

---

## 🛠️ Tech Stack & Prerequisites

* **Backend / Runtime:** [.NET 8.0 SDK](https://dotnet.microsoft.com/)
* **Frontend / Framework:** [Node.js](https://nodejs.org/) (v18+) & [Angular CLI](https://angular.dev/tools/cli) (v22+)
* **Languages:** C# 12, TypeScript 5+, HTML5, Vanilla CSS3
* **Development Environment:** Visual Studio Code / Visual Studio 2022 / JetBrains Rider

---

## 🚀 Quick Start Guide

### 1. Running the C# Console Modules (Parts A, B, C)
```bash
# Part A: Basics & Exercises
cd "Week_01/Week_01_PartA"
dotnet run

# Part B: Object-Oriented Practice
cd "../Week_01_PartB"
dotnet run

# Part C: Collections & LINQ
cd "../Week_01_PartC"
dotnet run
```

### 2. Running the Angular Web Modules (Part D & Final Project UI)
```bash
# Part D: Angular & TypeScript Roster
cd "Week_01/Week_01_PartD"
npm install
npm start
# Visit http://localhost:4200/

# Final Project: Angular Web Portal
cd "../Week_01_Final_Project/Student_Page_Angular"
npm install
npm start
# Visit http://localhost:4200/
```

### 3. Running the Final Project Console Portal
```bash
cd "Week_01/Week_01_Final_Project/Students_Management_Console"
dotnet run
```

---

## 🎯 Key Learning Outcomes & Competencies

By completing Week 1, interns have developed proficiency in:
1. **Strong Typing & Memory Models**: Differentiating between stack allocations and heap references in both C# and TypeScript.
2. **Defensive Coding Practices**: Utilizing non-throwing validation patterns (`TryParse`), structured exception cascades (`try/catch/finally`), and optional chaining in TypeScript (`?.`).
3. **Declarative Data Processing**: Replacing manual loops with declarative query pipelines using C# LINQ and TypeScript Array operators (`filter`, `map`, `reduce`).
4. **Architectural Separation**: Decoupling domain entities, manager services, and presentation components.
5. **Modern Reactive Frontends**: Structuring Angular standalone components using `@Input()`, `@Output()`, two-way binding (`[(ngModel)]`), and glassmorphic UI design.
