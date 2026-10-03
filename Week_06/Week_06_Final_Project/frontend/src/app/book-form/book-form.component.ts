import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { BookService } from '../book.service';
import { Book } from '../book.model';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-book-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './book-form.component.html',
  styleUrl: './book-form.component.css'
})
export class BookFormComponent implements OnInit {
  bookForm: FormGroup;
  isSubmitting: boolean = false;
  isEditMode: boolean = false;
  bookId: number | null = null;

  constructor(
    private fb: FormBuilder,
    private bookService: BookService,
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.bookForm = this.fb.group({
      title: ['', [Validators.required, Validators.minLength(2)]],
      author: ['', [Validators.required, Validators.minLength(2)]],
      category: ['', Validators.required]
    });
  }

  ngOnInit(): void {
    const idParam = this.route.snapshot.paramMap.get('id');
    if (idParam) {
      this.isEditMode = true;
      this.bookId = Number(idParam);
      
      // Existing book data fetch karke fields me automatically fill karna
      this.bookService.getBook(this.bookId).subscribe({
        next: (res: any) => {
          const bookData = res.data || res;
          this.bookForm.patchValue({
            title: bookData.title,
            author: bookData.author,
            category: bookData.category
          });
        },
        error: (err) => {
          console.error('Error fetching book details:', err);
        }
      });
    }
  }

  onSubmit(): void {
    if (this.bookForm.valid && !this.isSubmitting) {
      this.isSubmitting = true;

      if (this.isEditMode && this.bookId !== null) {
        // Update existing book (PUT Request)
        const updatedBook: Book = {
          bookId: this.bookId,
          title: this.bookForm.value.title,
          isbn: this.bookForm.value.category,
          authorId: 1 // Default Author ID for library system
        };
        this.bookService.updateBook(this.bookId, updatedBook).subscribe({
          next: () => {
            this.router.navigate(['/']);
          },
          error: (err) => {
            console.error('Error updating book:', err);
            this.isSubmitting = false;
          }
        });
      } else {
        // Add new book (POST Request)
        const newBook: Book = {
          title: this.bookForm.value.title,
          isbn: this.bookForm.value.category,
          publicationYear: new Date().getFullYear(),
          authorId: 1
        };
        this.bookService.addBook(newBook).subscribe({
          next: () => {
            this.router.navigate(['/']);
          },
          error: (err) => {
            console.error('Error saving book:', err);
            this.isSubmitting = false;
          }
        });
      }
    }
  }
}