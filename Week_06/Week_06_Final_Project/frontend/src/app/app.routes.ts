import { Routes } from '@angular/router';
import { BookListComponent } from './book-list/book-list.component';
import { BookFormComponent } from './book-form/book-form.component';
import { LoginComponent } from './login/login.component';
import { authGuard } from './auth.guard';

export const routes: Routes = [
  { path: '', component: BookListComponent },
  { path: 'login', component: LoginComponent },
  { path: 'add-book', component: BookFormComponent, canActivate: [authGuard] },
  { path: 'add-book/:id', component: BookFormComponent, canActivate: [authGuard] },
  { path: '**', redirectTo: '' }
];
