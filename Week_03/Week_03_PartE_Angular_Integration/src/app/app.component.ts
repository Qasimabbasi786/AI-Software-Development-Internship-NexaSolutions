import { Component } from '@angular/core';
import { BookListComponent } from './components/book-list/book-list.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [BookListComponent],
  template: `
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">
      <div class="container">
        <a class="navbar-brand font-monospace" href="#">📖 Islamabad Library Portal</a>
        <span class="navbar-text text-light">Week 3 Part E: Live Angular + .NET Integration</span>
      </div>
    </nav>
    <main class="py-4">
      <app-book-list></app-book-list>
    </main>
  `
})
export class AppComponent {}
