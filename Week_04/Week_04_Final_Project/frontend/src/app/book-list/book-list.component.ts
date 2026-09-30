import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { BookService } from '../book.service';
import { Book } from '../book.model';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-book-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './book-list.component.html',
  styleUrl: './book-list.component.css'
})
export class BookListComponent implements OnInit {
  books: Book[] = [];
  isLoading: boolean = false;
  errorMessage: string = '';

  constructor(
    private bookService: BookService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadBooks();
  }

  loadBooks(): void {
    this.isLoading = true;
    this.errorMessage = '';
    this.bookService.getBooks().subscribe({
      next: (data) => {
        this.books = data || [];
        this.isLoading = false;
      },
      error: (err) => {
        this.errorMessage = err.message || 'Failed to load books from server.';
        this.isLoading = false;
      }
    });
  }

  getAuthorName(book: Book): string {
    if (typeof book.author === 'string') return book.author;
    if (book.author && typeof book.author === 'object') return book.author.fullName;
    return `Author #${book.authorId || 'N/A'}`;
  }

  updateBook(id?: number): void {
    if (id !== undefined) {
      this.router.navigate(['/add-book', id]);
    }
  }

  deleteBook(id?: number): void {
    if (id !== undefined && confirm('Are you sure you want to delete this book?')) {
      this.isLoading = true;
      this.bookService.deleteBook(id).subscribe({
        next: () => {
          this.loadBooks();
        },
        error: (err) => {
          this.errorMessage = err.message || 'Failed to delete book.';
          this.isLoading = false;
        }
      });
    }
  }
}