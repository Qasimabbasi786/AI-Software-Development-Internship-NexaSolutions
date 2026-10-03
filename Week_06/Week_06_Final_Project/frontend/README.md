# Library Management Client (Angular 18+ Reactive UI)
### Week 3 Final Project — Frontend Application (`libraryFrontend`)

Welcome to the frontend client for the **Week 3 Final Project** in the **Nexa Solutions AI Software Development Internship Program**. This single-page application (SPA) is built with **Angular 18+ standalone components**, **Reactive Forms**, and **RxJS HttpClient** communicating with a live ASP.NET Core API backed by **PostgreSQL**.

---

## 🎨 UI/UX Features & Design Philosophy

1. **Modern Typography & Spacing**: Integrated with Google Fonts (`Inter`), modern cards, refined borders, and consistent spacing.
2. **Comprehensive State Management**:
   - **Loading Feedback**: Displays clean `⏳ Loading books from database...` states during asynchronous API round-trips.
   - **Error Handling**: Graceful error alert banners intercepting connection or backend validation failures.
   - **Empty States**: Clear messaging when no records are found in PostgreSQL.
3. **Reactive Forms Validation**: Real-time validation guards preventing empty or malformed submissions.
4. **Environment Isolation**: API endpoints are resolved dynamically via `environment.ts` without hardcoding URLs.

---

## 🏗️ Architecture & Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                 Angular SPA (Port 4200)                     │
│                                                             │
│  ┌────────────────────────┐      ┌───────────────────────┐  │
│  │   BookListComponent    │      │  BookFormComponent    │  │
│  │  - Table Roster & Cards│      │  - Reactive form      │  │
│  │  - Loading/Error states│      │  - Real-time check    │  │
│  └───────────┬────────────┘      └───────────┬───────────┘  │
│              │                               │              │
│              └───────────────┬───────────────┘              │
│                              ▼                              │
│                     BookService (RxJS)                      │
│                Base: http://localhost:5000/api              │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTP JSON Requests
                               ▼
               ASP.NET Core Web API (Port 5000)
                               │ Entity Framework Core 8
                               ▼
               PostgreSQL Database (librarydb_week3)
```

---

## 📁 Directory Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── book-form/
│   │   │   ├── book-form.component.ts      # Reactive form with Create/Edit logic
│   │   │   ├── book-form.component.html    # Form layout with validation feedback
│   │   │   └── book-form.component.css     # Modern input card styling & focus rings
│   │   ├── book-list/
│   │   │   ├── book-list.component.ts      # Table roster, loading & error state handlers
│   │   │   ├── book-list.component.html    # Responsive table, status badges, & alerts
│   │   │   └── book-list.component.css     # Table layout, button states, & shadows
│   │   ├── book.model.ts                   # Strongly-typed Book & Author interfaces
│   │   ├── book.service.ts                 # Reactive HttpClient with centralized error handling
│   │   ├── app.component.ts                # Application shell
│   │   ├── app.component.html              # Top navigation bar & <router-outlet>
│   │   ├── app.component.css               # Clean navigation bar & layout styling
│   │   ├── app.config.ts                   # Application providers (provideHttpClient, router)
│   │   └── app.routes.ts                   # Client route definitions
│   ├── environments/
│   │   ├── environment.ts                  # Development config (http://localhost:5000/api)
│   │   └── environment.prod.ts             # Production configuration
│   ├── index.html                          # Entry HTML with Inter Google Font preloaded
│   └── styles.css                          # Global styles
├── package.json                            # Angular dependencies & build scripts
└── angular.json                            # Workspace build configuration
```

---

## 🚀 Setup & Execution Guide

### Prerequisites
- Node.js (v18+)
- Running backend API on `http://localhost:5000`

### 1. Install Dependencies
```bash
cd Week_03/Week_03_Final_Project/frontend
npm install
```

### 2. Start Application
```bash
npm start
# Or: ng serve
```

Access the application in your browser at `http://localhost:4200`.
