# Week 3 - Part E: Angular API Integration

## 📌 Overview
This module demonstrates connecting a modern standalone **Angular 18+** single-page application (SPA) to a live ASP.NET Core REST API backed by PostgreSQL (`librarydb_week3`). 

It replaces mock data services with real HTTP calls using `HttpClient`, handles asynchronous responses using RxJS `Observables`, maintains base URLs via environment configuration, and manages UI loading (`isLoading`) and error states (`errorMessage`) gracefully.

---

## 🏗️ Project Architecture & Standard Angular Layout

```text
Week_03_PartE_Angular_Integration/
├── package.json                # Project dependencies and Angular scripts
├── package-lock.json           # Locked dependency tree
├── angular.json                # Angular CLI workspace build & serve configuration
├── tsconfig.json               # TypeScript compiler configuration (strict rules)
├── README.md                   # Clean documentation (zero secrets)
└── src/
    ├── main.ts                 # Application entry point bootstrapping AppComponent
    ├── index.html              # Base HTML template with Bootstrap 5 integration
    ├── styles.css              # Global application styles & Google Fonts
    ├── environments/
    │   ├── environment.ts      # Development API configuration (http://localhost:5000/api)
    │   └── environment.prod.ts # Production environment configuration
    └── app/
        ├── app.config.ts       # Application providers (provideHttpClient, provideRouter)
        ├── app.routes.ts       # Application routing setup
        ├── app.component.ts    # Root navigation shell
        ├── services/
        │   └── book.service.ts # Reactive HTTP Service (HttpClient, Observables, catchError)
        └── components/
            └── book-list/
                └── book-list.component.ts # Reactive Form + State Management (isLoading, errorMessage)
```

---

## ⚡ Technical Highlights & Best Practices

1. **Standalone Components**: Clean modular architecture using Angular 18+ standalone components without legacy `NgModule` boilerplate.
2. **`HttpClient` Provider**: Enabled globally via `provideHttpClient(withFetch())` inside [`app.config.ts`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/Week-03_and_04/Week_03/Week_03_PartE_Angular_Integration/src/app/app.config.ts).
3. **Environment Security**: API base URL is resolved dynamically from [`environment.ts`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/Week-03_and_04/Week_03/Week_03_PartE_Angular_Integration/src/environments/environment.ts) without exposing credentials or hardcoding URLs inside components.
4. **State Management**:
   - `isLoading`: Displays animated loading feedback while waiting for API responses.
   - `errorMessage`: Intercepts network failures and renders user-friendly error banners.
5. **Reactive Form Submission**: Submits new book payloads live to the PostgreSQL backend and triggers automated UI table updates.

---

## 🚀 Execution Instructions

1. Navigate to the project directory:
   ```bash
   cd Week_03_PartE_Angular_Integration
   ```
2. Start the Angular Development Server:
   ```bash
   npm start
   ```
3. Open browser at `http://localhost:4200` to interact with the live Islamabad Library Catalogue.

---

## 📢 Git Checkpoint
```bash
git add Week_03_PartE_Angular_Integration/
git commit -m "feat: connect Angular BookService to live API with loading and error states"
```
