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
  books$!: Observable<Book[]>;

  constructor(
    private bookService: BookService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadBooks();
  }

  loadBooks(): void {
    this.books$ = this.bookService.getBooks();
  }

  updateBook(id: number): void {
    this.router.navigate(['/add-book', id]);
  }



  deleteBook(id: number): void {
    this.deleteBookAction(id);
  }

  private deleteBookAction(id: number): void {
    this.bookService.deleteBook(id).subscribe(() => {
      this.loadBooks();
    });
  }
}