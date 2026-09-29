# Library Management Client (Angular 18+ Reactive UI)
### Week 2 Final Project — Frontend Application (`libraryFrontend`)

Welcome to the frontend client for the **Week 2 Capstone Project** in the **Nexa Solutions Internship Program**. This application is an interactive single-page application (SPA) built with **Angular 18+ standalone components**, **Reactive Forms**, **RxJS Observables**, and **HttpClient** to communicate with the ASP.NET Core Library API.

---

## Table of Contents
1. [Application Architecture & Data Flow](#1-application-architecture--data-flow)
2. [Project Scaffolding & Directory Tree](#2-project-scaffolding--directory-tree)
3. [Domain Model (`book.model.ts`)](#3-domain-model-bookmodelts)
4. [HTTP API Integration (`book.service.ts`)](#4-http-api-integration-bookservicets)
5. [Reactive Forms: `BookFormComponent`](#5-reactive-forms-bookformcomponent)
   - [Form Setup & Synchronous Validation](#form-setup--synchronous-validation)
   - [Dual Operation Mode (Create vs. Edit)](#dual-operation-mode-create-vs-edit)
6. [Library Roster: `BookListComponent`](#6-library-roster-booklistcomponent)
7. [Client-Side Routing (`app.routes.ts`)](#7-client-side-routing-approutests)
8. [Setup, Execution & Build Instructions](#8-setup-execution--build-instructions)
9. [Key Features & Frontend Best Practices](#9-key-features--frontend-best-practices)

---

## 1. Application Architecture & Data Flow

```
┌────────────────────────────────────────────────────────────────────────┐
│                   Angular Single Page Application                      │
│                                                                        │
│  ┌────────────────────────┐              ┌──────────────────────────┐  │
│  │   BookListComponent    │              │    BookFormComponent     │  │
│  │  - Displays book cards │              │  - Reactive form model   │  │
│  │  - Triggers Edit/Delete│              │  - Real-time validation  │  │
│  └───────────┬────────────┘              └────────────┬─────────────┘  │
│              │                                        │                │
│              │     router.navigate(['/add-book', id])  │                │
│              ├────────────────────────────────────────┘                │
│              ▼                                                         │
│     BookService (HttpClient)                                           │
│     Base URL: http://localhost:5184/api/Books                          │
└──────────────────────┬─────────────────────────────────────────────────┘
                       │ HTTP Requests (GET, POST, PUT, DELETE)
                       ▼
         ASP.NET Core Backend API (Port 5184)
```

---

## 2. Project Scaffolding & Directory Tree

```
libraryFrontend/
├── src/
│   ├── app/
│   │   ├── book-form/
│   │   │   ├── book-form.component.ts      # Reactive form with Create/Edit logic
│   │   │   ├── book-form.component.html    # Form layout and contextual error feedback
│   │   │   └── book-form.component.css     # Form aesthetics & input states
│   │   ├── book-list/
│   │   │   ├── book-list.component.ts      # Roster view & action handlers
│   │   │   ├── book-list.component.html    # Book card list & empty-state placeholders
│   │   │   └── book-list.component.css     # Card styling & badge formatting
│   │   ├── book.model.ts                   # TypeScript Book interface
│   │   ├── book.service.ts                 # HttpClient wrapper for REST API
│   │   ├── app.component.ts                # Root container
│   │   ├── app.component.html              # Top navigation bar & <router-outlet>
│   │   ├── app.component.css               # Global application layout & theme
│   │   ├── app.config.ts                   # App-wide providers (provideHttpClient, router)
│   │   └── app.routes.ts                   # Angular route configuration
│   ├── styles.css                          # Global styles & theme variables
│   └── index.html                          # Entry HTML document
├── angular.json                            # Angular workspace configuration
├── package.json                            # NPM dependencies & scripts
└── tsconfig.json                           # TypeScript compiler configuration
```

---

## 3. Domain Model (`book.model.ts`)

Located in [`src/app/book.model.ts`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_02/Week_02_Final_Project/libraryFrontend/src/app/book.model.ts):

```typescript
export interface Book {
  id?: number;
  title: string;
  author: string;
  category: string;
  createdAt?: string;
}
```

The optional `id` attribute accommodates both newly authored books (which have not yet been assigned a database ID) and retrieved records.

---

## 4. HTTP API Integration (`book.service.ts`)

Located in [`src/app/book.service.ts`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_02/Week_02_Final_Project/libraryFrontend/src/app/book.service.ts). It centralizes all communication with the ASP.NET Core API at `http://localhost:5184/api/Books`:

```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Book } from './book.model';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class BookService {
  private apiUrl = 'http://localhost:5184/api/Books';

  constructor(private http: HttpClient) { }

  // GET: Fetch all books and unwrap the 'data' property
  getBooks(): Observable<Book[]> {
    return this.http.get<any>(this.apiUrl).pipe(
      map(response => response.data)
    );
  }

  // GET by ID: Fetch a single book record
  getBook(id: number): Observable<Book> {
    return this.http.get<any>(`${this.apiUrl}/${id}`).pipe(
      map(response => response.data)
    );
  }

  // POST: Add a new book to the catalog
  addBook(book: Omit<Book, 'id'>): Observable<any> {
    return this.http.post<any>(this.apiUrl, book);
  }

  // PUT: Update an existing book record
  updateBook(id: number, book: Book): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}/${id}`, book);
  }

  // DELETE: Remove a book from the catalog
  deleteBook(id: number): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/${id}`);
  }
}
```

---

## 5. Reactive Forms: `BookFormComponent`

Located in [`src/app/book-form/book-form.component.ts`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_02/Week_02_Final_Project/libraryFrontend/src/app/book-form/book-form.component.ts).

### Form Setup & Synchronous Validation
The component builds a strongly typed `FormGroup` with explicit validators:
```typescript
this.bookForm = this.fb.group({
  title: ['', [Validators.required, Validators.minLength(2)]],
  author: ['', [Validators.required, Validators.minLength(2)]],
  category: ['', Validators.required]
});
```

### Dual Operation Mode (Create vs. Edit)
The component automatically inspects the route parameters in `ngOnInit`:
- If an `:id` parameter exists, it switches to **Edit Mode**, calls `bookService.getBook(id)`, and populates the controls using `patchValue()`.
- If no `:id` exists, it remains in **Create Mode**.

```typescript
ngOnInit(): void {
  const idParam = this.route.snapshot.paramMap.get('id');
  if (idParam) {
    this.isEditMode = true;
    this.bookId = Number(idParam);
    
    this.bookService.getBook(this.bookId).subscribe({
      next: (res: any) => {
        const bookData = res.data || res;
        this.bookForm.patchValue({
          title: bookData.title,
          author: bookData.author,
          category: bookData.category
        });
      },
      error: (err) => console.error('Error fetching book details:', err)
    });
  }
}
```

On submit, it routes to `bookService.updateBook()` or `bookService.addBook()`, navigating back to `/` upon completion.

---

## 6. Library Roster: `BookListComponent`

Located in [`src/app/book-list/book-list.component.ts`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_02/Week_02_Final_Project/libraryFrontend/src/app/book-list/book-list.component.ts).

- Holds an `Observable<Book[]>` stream (`books$`).
- Handles update clicks by routing to `/add-book/:id`.
- Executes deletion using `deleteBook(id)` and triggers `loadBooks()` upon success to refresh the UI.

---

## 7. Client-Side Routing (`app.routes.ts`)

Located in [`src/app/app.routes.ts`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_02/Week_02_Final_Project/libraryFrontend/src/app/app.routes.ts):

```typescript
import { Routes } from '@angular/router';
import { BookListComponent } from './book-list/book-list.component';
import { BookFormComponent } from './book-form/book-form.component';

export const routes: Routes = [
  { path: '', component: BookListComponent },
  { path: 'add-book', component: BookFormComponent },
  { path: 'add-book/:id', component: BookFormComponent }
];
```

---

## 8. Setup, Execution & Build Instructions

Ensure you have [Node.js](https://nodejs.org/) (v18+) and [Angular CLI](https://angular.dev/tools/cli) installed.

```bash
# Navigate to the frontend directory
cd "Week_02/Week_02_Final_Project/libraryFrontend"

# Install dependencies (first time only)
npm install

# Start development server
npm start
# or: ng serve --open
```

*The application launches at `http://localhost:4200/`.*

### Building Production Assets
```bash
npm run build
```
Compiled production bundles are saved into the `dist/library-frontend` folder.

---

## 9. Key Features & Frontend Best Practices

1. **Standalone Components**: Clean architecture without legacy `NgModule` declarations.
2. **Synchronous Validation Guard**: Submit buttons are disabled when `bookForm.invalid || isSubmitting` to prevent invalid or duplicate submissions.
3. **Reactive Patching**: `patchValue()` populates fields smoothly during edits without recreating form controls.
4. **Clean Navigation Feedback**: Uses Angular's `Router` for navigation between catalog and form views.
