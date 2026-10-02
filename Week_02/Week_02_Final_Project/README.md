# 📚 Full-Stack Library Management Suite
### Week 2 — Capstone Project: ASP.NET Core Web API + Angular Reactive Forms

**Author:** Muhammad Qasim  
**Program:** AI Software Development Internship (.NET + Angular + AI)  
**Milestone:** Week 2 Final Project — Tiered Full-Stack Architecture  

[![.NET 8](https://img.shields.io/badge/.NET-8.0-512BD4?logo=dotnet&logoColor=white)](https://dotnet.microsoft.com/)
[![ASP.NET Core](https://img.shields.io/badge/ASP.NET_Core-Web_API-512BD4?logo=dotnet&logoColor=white)](https://learn.microsoft.com/aspnet/core/)
[![Angular](https://img.shields.io/badge/Angular-19%2F22-DD0031?logo=angular&logoColor=white)](https://angular.dev/)
[![RxJS](https://img.shields.io/badge/Reactive-RxJS_Forms-B7178C?logo=reactivex&logoColor=white)](https://rxjs.dev/)
[![Status: Completed](https://img.shields.io/badge/Status-Completed_%E2%9C%85-success)](https://github.com/)

---

Welcome to the **Week 2 Capstone Project** for the **Nexa Solutions Internship Program**. This project delivers a full-stack, enterprise-patterned Library Management application combining an **ASP.NET Core Web API** (employing the Controller-Service-Repository pattern) with an **Angular 19/22** frontend powered by **Reactive Forms**, client-side routing, and real-time HTTP integration via `HttpClient`.

---

## Table of Contents
1. [End-to-End System Architecture](#1-end-to-end-system-architecture)
2. [Backend Architecture (`libraryAPI`)](#2-backend-architecture-libraryapi)
   - [Domain Model (`Book.cs`)](#domain-model-bookcs)
   - [Repository Pattern (`IBookRepository` & `BookRepository`)](#repository-pattern-ibookrepository--bookrepository)
   - [Service Layer (`IBookService` & `BookService`)](#service-layer-ibookservice--bookservice)
   - [API Controller (`BooksController.cs`)](#api-controller-bookscontrollercs)
   - [Dependency Injection & CORS Registration](#dependency-injection--cors-registration)
3. [Frontend Architecture (`libraryFrontend`)](#3-frontend-architecture-libraryfrontend)
   - [Data Modeling (`book.model.ts`)](#data-modeling-bookmodelts)
   - [HTTP Service Integration (`book.service.ts`)](#http-service-integration-bookservicets)
   - [Reactive Forms Component (`BookFormComponent`)](#reactive-forms-component-bookformcomponent)
   - [Book Roster Component (`BookListComponent`)](#book-roster-component-booklistcomponent)
   - [Client-Side Routing Setup](#client-side-routing-setup)
4. [Step-by-Step Execution Guide](#4-step-by-step-execution-guide)
   - [1. Starting the ASP.NET Core API](#1-starting-the-aspnet-core-api)
   - [2. Starting the Angular Application](#2-starting-the-angular-application)
5. [API Endpoint Contract & Swagger Reference](#5-api-endpoint-contract--swagger-reference)
6. [Architectural Highlights & Best Practices](#6-architectural-highlights--best-practices)

---

## 1. End-to-End System Architecture

The project cleanly separates frontend presentation from backend domain persistence:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        Angular Frontend (Port 4200)                    │
│                                                                        │
│  ┌────────────────────────┐              ┌──────────────────────────┐  │
│  │   BookListComponent    │              │    BookFormComponent     │  │
│  │  (Roster, Edit/Delete) │              │ (Reactive Forms & Valid) │  │
│  └───────────┬────────────┘              └────────────┬─────────────┘  │
│              │                                        │                │
│              └───────────────────┬────────────────────┘                │
│                                  ▼                                     │
│                         BookService (HttpClient)                      │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ HTTP (CORS: http://localhost:4200)
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     ASP.NET Core Web API (Port 5184)                   │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │               BooksController (HTTP Routing & Statuses)          │  │
│  └───────────────────────────────┬──────────────────────────────────┘  │
│                                  ▼                                     │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │               IBookService / BookService (Business Logic)        │  │
│  └───────────────────────────────┬──────────────────────────────────┘  │
│                                  ▼                                     │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │         IBookRepository / BookRepository (In-Memory Store)       │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Backend Architecture (`libraryAPI`)

Located at: [`libraryAPI/`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_02/Week_02_Final_Project/libraryAPI)

### Domain Model (`Book.cs`)
```csharp
namespace libraryAPI.Models
{
    public class Book
    {
        public int Id { get; set; }
        public string Title { get; set; } = string.Empty;
        public string Author { get; set; } = string.Empty;
        public string Category { get; set; } = string.Empty;
        public DateTime CreatedAt { get; set; } = DateTime.Now;
    }
}
```

### Repository Pattern (`IBookRepository` & `BookRepository`)
Decouples data access from business logic. The `BookRepository` manages an in-memory collection wrapped in asynchronous `Task.FromResult`:

```csharp
public interface IBookRepository
{
    Task<IEnumerable<Book>> GetAllAsync();
    Task<Book?> GetByIdAsync(int id);
    Task<Book> AddAsync(Book book);
    Task<bool> UpdateAsync(Book book);
    Task<bool> DeleteAsync(int id);
}
```

### Service Layer (`IBookService` & `BookService`)
Enforces business rules and abstracts data operations for the controller:
```csharp
public class BookService : IBookService
{
    private readonly IBookRepository _repository;

    public BookService(IBookRepository repository)
    {
        _repository = repository;
    }

    public Task<IEnumerable<Book>> GetAllBooksAsync() => _repository.GetAllAsync();
    public Task<Book?> GetBookByIdAsync(int id) => _repository.GetByIdAsync(id);
    public Task<Book> AddBookAsync(Book book) => _repository.AddAsync(book);
    public Task<bool> UpdateBookAsync(Book book) => _repository.UpdateAsync(book);
    public Task<bool> DeleteBookAsync(int id) => _repository.DeleteAsync(id);
}
```

### API Controller (`BooksController.cs`)
Exposes RESTful endpoints, returning standardized HTTP status codes:
- **`GET /api/Books`**: `200 OK` with list of books.
- **`GET /api/Books/{id}`**: `200 OK` or `404 Not Found`.
- **`POST /api/Books`**: Validates required fields, returns `201 Created` with a `CreatedAtAction` location header.
- **`PUT /api/Books/{id}`**: Validates ID match, returns `200 OK` or `404 Not Found`.
- **`DELETE /api/Books/{id}`**: Removes book, returns `200 OK` or `404 Not Found`.

### Dependency Injection & CORS Registration
In [Program.cs](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_02/Week_02_Final_Project/libraryAPI/Program.cs):
```csharp
// Register in-memory repository as Singleton so state persists across requests
builder.Services.AddSingleton<IBookRepository, BookRepository>();

// Register Service as Scoped
builder.Services.AddScoped<IBookService, BookService>();

// Enable CORS for Angular frontend
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAngular", policy =>
    {
        policy.WithOrigins("http://localhost:4200")
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});
```

---

## 3. Frontend Architecture (`libraryFrontend`)

Located at: [`libraryFrontend/`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_02/Week_02_Final_Project/libraryFrontend)

### Data Modeling (`book.model.ts`)
```typescript
export interface Book {
  id?: number;
  title: string;
  author: string;
  category: string;
  createdAt?: string;
}
```

### HTTP Service Integration (`book.service.ts`)
Encapsulates all backend REST calls using Angular's `HttpClient`:
```typescript
@Injectable({ providedIn: 'root' })
export class BookService {
  private apiUrl = 'http://localhost:5184/api/Books';

  constructor(private http: HttpClient) { }

  getBooks(): Observable<Book[]> {
    return this.http.get<any>(this.apiUrl).pipe(map(res => res.data));
  }

  getBook(id: number): Observable<Book> {
    return this.http.get<any>(`${this.apiUrl}/${id}`).pipe(map(res => res.data));
  }

  addBook(book: Omit<Book, 'id'>): Observable<any> {
    return this.http.post<any>(this.apiUrl, book);
  }

  updateBook(id: number, book: Book): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}/${id}`, book);
  }

  deleteBook(id: number): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/${id}`);
  }
}
```

### Reactive Forms Component (`BookFormComponent`)
Supports both **Create Mode** (`/add-book`) and **Edit Mode** (`/add-book/:id`):
```typescript
ngOnInit(): void {
  const idParam = this.route.snapshot.paramMap.get('id');
  if (idParam) {
    this.isEditMode = true;
    this.bookId = Number(idParam);
    
    // Automatically pre-populate form for editing
    this.bookService.getBook(this.bookId).subscribe({
      next: (book) => this.bookForm.patchValue(book)
    });
  }
}
```

### Book Roster Component (`BookListComponent`)
Renders book records with action triggers to update or delete records, immediately refreshing the view.

### Client-Side Routing Setup
```typescript
export const routes: Routes = [
  { path: '', component: BookListComponent },
  { path: 'add-book', component: BookFormComponent },
  { path: 'add-book/:id', component: BookFormComponent }
];
```

---

## 4. Step-by-Step Execution Guide

### 1. Starting the ASP.NET Core API
```bash
# Navigate to the backend directory
cd "Week_02/Week_02_Final_Project/libraryAPI"

# Build and run the server
dotnet run
```
*API Swagger documentation will be available at `http://localhost:5184/` (or port indicated in console).*

### 2. Starting the Angular Application
Open a second terminal window:
```bash
# Navigate to the frontend directory
cd "Week_02/Week_02_Final_Project/libraryFrontend"

# Install dependencies (first time only)
npm install

# Start development server
npm start
# or: ng serve
```
*Access the library frontend portal at `http://localhost:4200/`.*

---

## 5. API Endpoint Contract & Swagger Reference

| Method | Endpoint | Description | Expected Status Codes |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/Books` | Retrieve all books | `200 OK` |
| `GET` | `/api/Books/{id}` | Get book by primary key | `200 OK`, `404 Not Found` |
| `POST` | `/api/Books` | Add new book | `201 Created`, `400 Bad Request` |
| `PUT` | `/api/Books/{id}` | Update book details | `200 OK`, `400 Bad Request`, `404 Not Found` |
| `DELETE`| `/api/Books/{id}` | Delete book from inventory | `200 OK`, `404 Not Found` |

---

## 6. Architectural Highlights & Best Practices

1. **Separation of Concerns**: Controllers handle HTTP concerns, Services manage business flow, and Repositories handle data access.
2. **CORS Security**: Cross-Origin Resource Sharing is explicitly configured in .NET Core to allow requests from the Angular development origin.
3. **Dual-Mode Reactive Forms**: A single `BookFormComponent` handles both creation and updates using route parameter detection and `patchValue()`.
4. **Resilient Error Logging**: Frontend HTTP subscriptions capture and log network or validation errors without breaking the UI state.

---

## 👤 Author

- **Name:** Muhammad Qasim  
- **Internship:** AI Software Development Internship (.NET + Angular + AI)

