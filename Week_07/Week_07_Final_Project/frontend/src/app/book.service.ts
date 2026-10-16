import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Book } from './book.model';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class BookService {
  private readonly apiUrl = `${environment.apiUrl}/books`;

  constructor(private http: HttpClient) { }

  getBooks(): Observable<Book[]> {
    return this.http.get<Book[]>(this.apiUrl).pipe(
      catchError(this.handleError)
    );
  }

  getBook(id: number): Observable<Book> {
    return this.http.get<Book>(`${this.apiUrl}/${id}`).pipe(
      catchError(this.handleError)
    );
  }

  addBook(book: Book): Observable<Book> {
    return this.http.post<Book>(this.apiUrl, book).pipe(
      catchError(this.handleError)
    );
  }

  updateBook(id: number, book: Book): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}/${id}`, book).pipe(
      catchError(this.handleError)
    );
  }

  deleteBook(id: number): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/${id}`).pipe(
      catchError(this.handleError)
    );
  }

  private handleError(error: HttpErrorResponse): Observable<never> {
    let clientMessage = 'An unexpected network error occurred.';
    if (error.error instanceof ErrorEvent) {
      clientMessage = `Network error: ${error.error.message}`;
    } else {
      clientMessage = error.status === 0
        ? 'Could not connect to backend server. Please verify .NET API is running on http://localhost:5000.'
        : `Server returned code ${error.status}: ${error.error?.message || error.message}`;
    }
    return throwError(() => new Error(clientMessage));
  }
}