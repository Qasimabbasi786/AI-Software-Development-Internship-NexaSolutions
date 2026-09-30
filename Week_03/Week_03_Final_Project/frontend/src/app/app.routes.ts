import { Routes } from '@angular/router';
import { BookListComponent } from './book-list/book-list.component';
import { BookFormComponent } from './book-form/book-form.component';

export const routes: Routes = [
  { path: '', component: BookListComponent },
  { path: 'add-book', component: BookFormComponent },
  { path: 'add-book/:id', component: BookFormComponent }
];
