import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Book, BookService } from '../../services/book.service';

@Component({
  selector: 'app-book-list',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  template: `
    <div class="container mt-4">
      <h2>📚 Islamabad Library - Live Books Catalogue</h2>
      
      <!-- Error State Banner -->
      <div *ngIf="errorMessage" class="alert alert-danger alert-dismissible fade show" role="alert">
        <strong>⚠️ Connection / Data Error:</strong> {{ errorMessage }}
        <button type="button" class="btn-close" (click)="errorMessage = ''"></button>
      </div>

      <!-- Loading State Spinner -->
      <div *ngIf="isLoading" class="d-flex align-items-center my-4">
        <div class="spinner-border text-primary me-3" role="status"></div>
        <span>Loading books from PostgreSQL API...</span>
      </div>

      <!-- Reactive Form: Add Book -->
      <div class="card my-4 p-3 shadow-sm">
        <h4>Add New Book</h4>
        <form [formGroup]="bookForm" (ngSubmit)="onSubmit()">
          <div class="row g-3">
            <div class="col-md-5">
              <input type="text" formControlName="title" class="form-control" placeholder="Book Title (e.g. Nuskha-Hai-Wafa)" />
            </div>
            <div class="col-md-3">
              <input type="text" formControlName="isbn" class="form-control" placeholder="ISBN (e.g. 978-969-0-01501-1)" />
            </div>
            <div class="col-md-2">
              <input type="number" formControlName="publicationYear" class="form-control" placeholder="Year" />
            </div>
            <div class="col-md-2">
              <button type="submit" class="btn btn-success w-100" [disabled]="bookForm.invalid || isSubmitting">
                {{ isSubmitting ? 'Saving...' : 'Add Book' }}
              </button>
            </div>
          </div>
        </form>
      </div>

      <!-- Data Table -->
      <table *ngIf="!isLoading && books.length > 0" class="table table-striped table-hover shadow-sm">
        <thead class="table-dark">
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>ISBN</th>
            <th>Year</th>
            <th>Author</th>
          </tr>
        </thead>
        <tbody>
          <tr *ngFor="let b of books">
            <td>{{ b.bookId }}</td>
            <td><strong>{{ b.title }}</strong></td>
            <td><code>{{ b.isbn || 'N/A' }}</code></td>
            <td>{{ b.publicationYear || 'N/A' }}</td>
            <td><span class="badge bg-info text-dark">{{ b.author?.fullName || 'Author ID: ' + b.authorId }}</span></td>
          </tr>
        </tbody>
      </table>

      <!-- Empty State -->
      <div *ngIf="!isLoading && books.length === 0 && !errorMessage" class="alert alert-warning">
        No books found in PostgreSQL database.
      </div>
    </div>
  `
})
export class BookListComponent implements OnInit {
  books: Book[] = [];
  isLoading = false;
  isSubmitting = false;
  errorMessage = '';
  bookForm: FormGroup;

  constructor(private bookService: BookService, private fb: FormBuilder) {
    this.bookForm = this.fb.group({
      title: ['', Validators.required],
      isbn: [''],
      publicationYear: [new Date().getFullYear()],
      authorId: [1, Validators.required] // Default Author ID
    });
  }

  ngOnInit(): void {
    this.fetchBooks();
  }

  fetchBooks(): void {
    this.isLoading = true;
    this.errorMessage = '';

    this.bookService.getBooks().subscribe({
      next: (data) => {
        this.books = data;
        this.isLoading = false;
      },
      error: (err) => {
        this.errorMessage = err.message || 'Could not load books from server.';
        this.isLoading = false;
      }
    });
  }

  onSubmit(): void {
    if (this.bookForm.invalid) return;

    this.isSubmitting = true;
    const newBook: Book = this.bookForm.value;

    this.bookService.createBook(newBook).subscribe({
      next: () => {
        this.isSubmitting = false;
        this.bookForm.patchValue({ title: '', isbn: '' });
        this.fetchBooks(); // Refresh table live
      },
      error: (err) => {
        this.errorMessage = err.message || 'Failed to save book.';
        this.isSubmitting = false;
      }
    });
  }
}
