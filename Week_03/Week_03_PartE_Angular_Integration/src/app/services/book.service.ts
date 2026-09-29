import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { environment } from '../../environments/environment';

export interface Author {
  authorId: number;
  fullName: string;
  city: string;
}

export interface Book {
  bookId?: number;
  title: string;
  isbn?: string;
  publicationYear?: number;
  authorId: number;
  author?: Author;
}

@Injectable({
  providedIn: 'root'
})
export class BookService {
  private readonly baseUrl = `${environment.apiUrl}/books`;

  constructor(private http: HttpClient) {}

  /**
   * GET: Fetch all books from live .NET API backed by PostgreSQL
   */
  getBooks(): Observable<Book[]> {
    return this.http.get<Book[]>(this.baseUrl).pipe(
      catchError(this.handleError)
    );
  }

  /**
   * GET: Fetch single book by ID
   */
  getBookById(id: number): Observable<Book> {
    return this.http.get<Book>(`${this.baseUrl}/${id}`).pipe(
      catchError(this.handleError)
    );
  }

  /**
   * POST: Create a new book record
   */
  createBook(book: Book): Observable<Book> {
    return this.http.post<Book>(this.baseUrl, book).pipe(
      catchError(this.handleError)
    );
  }

  /**
   * Centralized HTTP error transformer
   */
  private handleError(error: HttpErrorResponse): Observable<never> {
    let clientMessage = 'An unexpected network error occurred.';
    if (error.error instanceof ErrorEvent) {
      // Client-side / network error
      clientMessage = `Network error: ${error.error.message}`;
    } else {
      // Backend returned unsuccessful response code
      clientMessage = error.status === 0
        ? 'Could not connect to backend server. Please verify .NET API is running.'
        : `Backend returned code ${error.status}: ${error.error?.message || error.message}`;
    }
    return throwError(() => new Error(clientMessage));
  }
}
