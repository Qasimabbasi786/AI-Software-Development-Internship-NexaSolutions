# Week 4 - Part B: Angular Auth Integration

## 🎯 Objectives
- Build a dedicated `AuthService` handling login, logout, token storage, and authentication state (`isLoggedIn`, current user role).
- Understand token storage in `localStorage` vs `httpOnly` cookies and their security tradeoffs (XSS vs CSRF).
- Implement a functional HTTP interceptor (`authInterceptor`) using `HttpInterceptorFn` to automatically attach the `Authorization: Bearer <token>` header to all outgoing HTTP requests.
- Implement a functional Route Guard (`authGuard`) using `CanActivateFn` to guard protected routes (e.g. `/books/new`, `/books/edit/:id`).
- Build a reactive Login component (`login.component.ts`) with form validation, error display, and redirect on successful login.
- Show / hide UI controls (such as the **Add Book** and **Delete** buttons) based on whether the logged-in user has the `Admin` role.

## 🛠️ Step-by-Step Implementation Guide

### 1. Create `AuthService`
```typescript
@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly TOKEN_KEY = 'library_jwt_token';
  // login(), logout(), getToken(), isLoggedIn(), getUserRole(), decodeToken()
}
```

### 2. Implement Functional `authInterceptor` (`auth.interceptor.ts`)
```typescript
import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from './services/auth.service';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const token = authService.getToken();

  if (!token) {
    return next(req);
  }

  const cloned = req.clone({
    setHeaders: {
      Authorization: `Bearer ${token}`
    }
  });

  return next(cloned);
};
```

### 3. Register Interceptor in `app.config.ts`
```typescript
export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideHttpClient(withInterceptors([authInterceptor]))
  ]
};
```

### 4. Implement Functional `authGuard` (`auth.guard.ts`)
```typescript
import { CanActivateFn, Router } from '@angular/router';
import { inject } from '@angular/core';
import { AuthService } from './services/auth.service';

export const authGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  const router = inject(Router);

  if (authService.isLoggedIn()) {
    return true;
  }

  router.navigate(['/login'], { queryParams: { returnUrl: state.url } });
  return false;
};
```

### 5. Practice Exercises
- [ ] Log in through the Angular UI and verify in the Browser DevTools Network tab that the `Authorization: Bearer ...` header is attached to book creation requests.
- [ ] Attempt navigating to a guarded route when logged out and verify automatic redirection to `/login`.
- [ ] Test Logout button to ensure token is cleared from `localStorage` and UI state resets.
- [ ] Conditionally display the "Delete" button only for users with the `Admin` role.

## 🌿 Git Checkpoint
```bash
git checkout -b feature/angular-auth
git commit -m "feat: add Angular login, auth interceptor, and route guards"
```
