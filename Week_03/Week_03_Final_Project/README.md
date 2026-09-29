# Week 3 Final Project - Database-Backed Library API + Angular Client + AI Script

## 📌 Overview
This directory serves as the integrated project workspace combining all components mastered in Parts A through G into a unified solution.

## 🏗️ Architecture & Data Flow
```text
Angular SPA (Frontend) 
  └── HTTP Requests (HttpClient) 
       └── ASP.NET Core Web API (Controllers & Services) 
            └── Repository Layer 
                 └── EF Core (Npgsql Provider) 
                      └── PostgreSQL Database (LibraryDb_Week3)

Standalone Python AI Script ── (LLM API) ──> Summaries & Genre Recommendations
```

## 🛠️ Tech Stack
- **Backend**: C# / .NET ASP.NET Core Web API
- **Database**: PostgreSQL with EF Core (`Npgsql.EntityFrameworkCore.PostgreSQL`)
- **Frontend**: Angular SPA with Reactive Forms & RxJS `HttpClient`
- **AI Track**: Python 3.x standalone script with dotenv & API SDK

## 📁 Project Structure Layout
```text
Week_03_Project/
├── README.md
├── backend/            # ASP.NET Core Web API Project
├── frontend/           # Angular SPA Client Application
└── ai-services/        # Python AI Summary Script
```

## 🚀 Execution Guide
Detailed step-by-step instructions for running the backend API, frontend client, and standalone AI script will be updated as each module is implemented.
