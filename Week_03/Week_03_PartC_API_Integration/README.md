# Week 3 - Part C: API + Database Integration

## 📌 Overview
This module demonstrates swapping out a temporary in-memory repository (`List<Book>`) with an EF Core / PostgreSQL-backed repository pattern in ASP.NET Core Web API while maintaining a clean, layered architecture without altering API response contracts or client endpoint URLs.

---

## 🏗️ Layered Architecture & Integration Strategy

```text
Angular SPA Frontend (http://localhost:4200)
   │
   ▼ (CORS Allowed)
[ BooksController ] ── (Uses IBookRepository interface)
   │
   ▼
[ BookRepository ]  ── (Injects LibraryDbContext via DI)
   │
   ▼
[ LibraryDbContext ] ── (Npgsql Provider & JSON Reference Cycles Ignored)
   │
   ▼
[ PostgreSQL Database (librarydb_week3) ]
```

- **Contract Stability**: The API routes (`GET /api/books`, `GET /api/books/{id}`, `POST /api/books`, etc.) and JSON request/response DTO payload shapes remain identical.
- **Dependency Injection**: Registered `IBookRepository` -> `BookRepository` in `Program.cs`.
- **CORS Policy Enabled**: Configured `AllowAngularApp` policy enabling `http://localhost:4200` to fetch and post data safely without browser cross-origin blocking.
- **JSON Cycle Handling**: Configured `ReferenceHandler.IgnoreCycles` to serialize entity navigation properties safely.
- **Environment Security**: Database credentials are dynamically resolved from system/local `.env` configurations without committing secrets.

---

## 🛡️ Error & Exception Handling Matrix

| Scenario | Database Behavior | HTTP Response Code | Handled In Layer |
| :--- | :--- | :--- | :--- |
| **Fetch missing Book ID** | `FirstOrDefaultAsync()` returns `null` | `404 Not Found` | `BooksController.cs` |
| **Delete missing Book ID** | `FindAsync()` returns `null` | `404 Not Found` | `BooksController.cs` |
| **Duplicate ISBN / Bad FK** | `DbUpdateException` thrown | `400 Bad Request` | `BookRepository.cs` / Controller |
| **Database Connection Fail**| Connection timeout / Exception | `500 Internal Error` logged gracefully | Global exception middleware / Logger |

---

## 📁 Key Implementation Files

- [`Week_03_PartC_API_Integration.csproj`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/Week-03_and_04/Week_03/Week_03_PartC_API_Integration/Week_03_PartC_API_Integration.csproj): Web API project file.
- [`Program.cs`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/Week-03_and_04/Week_03/Week_03_PartC_API_Integration/Program.cs): ASP.NET Core startup registering `LibraryDbContext`, `IBookRepository`, CORS policy, and Swagger UI.
- [`Data/LibraryDbContext.cs`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/Week-03_and_04/Week_03/Week_03_PartC_API_Integration/Data/LibraryDbContext.cs): PostgreSQL DbContext.
- [`Repositories/IBookRepository.cs`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/Week-03_and_04/Week_03/Week_03_PartC_API_Integration/Repositories/IBookRepository.cs): Repository interface abstraction.
- [`Repositories/BookRepository.cs`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/Week-03_and_04/Week_03/Week_03_PartC_API_Integration/Repositories/BookRepository.cs): EF Core-backed PostgreSQL repository implementation.
- [`Controllers/BooksController.cs`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/Week-03_and_04/Week_03/Week_03_PartC_API_Integration/Controllers/BooksController.cs): REST API Controller mapping repository calls to HTTP ActionResults.

---

## 📢 Git Checkpoint
```bash
git add Week_03_PartC_API_Integration/
git commit -m "feat: configure CORS for Angular integration and update README"
```
