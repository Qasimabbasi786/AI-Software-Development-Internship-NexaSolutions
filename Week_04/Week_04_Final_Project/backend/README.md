# Week 3 Final Project — Backend API Service (`libraryAPI`)
### Enterprise ASP.NET Core 8 Web API + PostgreSQL + EF Core

Welcome to the backend service for the **Week 3 Final Project** in the **Nexa Solutions AI Software Development Internship Program**. This service transitions our Week 2 in-memory architecture into a production-grade, relational-database-backed RESTful API leveraging **Entity Framework Core 8** and **PostgreSQL (`librarydb_week3`)**.

---

## 🏗️ Architecture & Data Flow

```
 HTTP Request (Angular Client :4200 / Postman / Swagger)
                     │
                     ▼
┌────────────────────────────────────────────────────────┐
│            Controllers (Presentation Layer)            │
│  - BooksController: CRUD endpoints                     │
│  - AuthController: Login / Register skeleton           │
└──────────────────────────┬─────────────────────────────┘
                           │ Dependency Injection
                           ▼
┌────────────────────────────────────────────────────────┐
│            Repositories (Data Access Layer)            │
│  - IBookRepository & BookRepository                    │
│  - Asynchronous LINQ queries with EF Core              │
└──────────────────────────┬─────────────────────────────┘
                           │ Entity Framework Core 8
                           ▼
┌────────────────────────────────────────────────────────┐
│               LibraryDbContext (ORM Session)           │
│  - Authors, Books, Categories, BookCategories, Users   │
│  - Dynamically configured via secure local .env        │
└──────────────────────────┬─────────────────────────────┘
                           │ Npgsql Driver
                           ▼
┌────────────────────────────────────────────────────────┐
│               PostgreSQL Database                      │
│  - Database: librarydb_week3 (localhost:5432)          │
│  - Tables: "Books", "Authors", "Categories", "Users"   │
└────────────────────────────────────────────────────────┘
```

---

## 📁 Directory Structure

```
backend/
├── Controllers/
│   ├── BooksController.cs         # RESTful HTTP endpoints for Books
│   └── AuthController.cs          # Login & registration skeleton endpoints
├── Data/
│   └── LibraryDbContext.cs        # EF Core DbContext with relationship mappings
├── Models/
│   ├── Author.cs                  # Author entity (1:N with Book)
│   ├── Book.cs                    # Book entity (N:1 Author, M:N Category)
│   ├── Category.cs                # Category entity
│   ├── BookCategory.cs            # Junction join entity
│   └── User.cs                    # Lightweight user auth skeleton entity
├── Repositories/
│   ├── IBookRepository.cs         # Repository contract abstraction
│   └── BookRepository.cs          # EF Core implementation with PostgreSQL
├── Properties/
│   └── launchSettings.json        # Configured for Port 5000 (HTTP)
├── .env.example                   # Non-sensitive environment variable template
├── appsettings.json               # Logging and core framework settings
└── Program.cs                     # Startup configuration, CORS, and .env parser
```

---

## 🔒 Environment Configuration (`.env`)

To protect credentials from source control, database secrets are read dynamically from `.env` in the backend root:

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=librarydb_week3
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_actual_password_here
```

A template file [`.env.example`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_03/Week_03_Final_Project/backend/.env.example) is committed to Git while `.env` is protected via `.gitignore`.

---

## 📡 API Endpoints

### Books API (`/api/books`)
| Method | Endpoint | Description | Status Codes |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/books` | Fetch all books with authors | `200 OK` |
| `GET` | `/api/books/{id}` | Fetch book by primary key ID | `200 OK`, `404 Not Found` |
| `POST` | `/api/books` | Create new book in PostgreSQL | `201 Created`, `400 Bad Request` |
| `PUT` | `/api/books/{id}` | Update existing book entity | `204 No Content`, `404 Not Found` |
| `DELETE`| `/api/books/{id}` | Delete book from database | `204 No Content`, `404 Not Found` |

### Auth Skeleton API (`/api/auth`)
| Method | Endpoint | Description | Status Codes |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/register` | Register new user in Users table | `200 OK`, `400 Bad Request` |
| `POST` | `/api/auth/login` | Validate user credentials skeleton | `200 OK`, `401 Unauthorized` |

---

## 🚀 How to Run & Verify

1. **Restore & Build**:
   ```bash
   dotnet restore
   dotnet build
   ```

2. **Run Server**:
   ```bash
   dotnet run
   ```

3. **Explore via Swagger**:
   Open browser at `http://localhost:5000` to interact with Swagger UI.
