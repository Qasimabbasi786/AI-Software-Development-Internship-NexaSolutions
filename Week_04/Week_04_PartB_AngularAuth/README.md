# Week 4 - Part B: Angular Auth Integration

## 📌 Executive Summary
In Week 4 - Part B, we integrate end-to-end authentication and client-side access control into the Angular 18+ Single Page Application (SPA). This mirrors enterprise patterns:
1. **Centralized Authentication Service (`AuthService`)**: Manages login/logout state, stores JWT tokens in `localStorage`, and reactive state broadcasting via RxJS `BehaviorSubject`.
2. **Functional HTTP Interceptor (`authInterceptor`)**: Intercepts all outgoing HTTP calls to seamlessly append `Authorization: Bearer <token>` without boilerplate code across service methods.
3. **Functional Route Guards (`authGuard`)**: Enforces access control on protected routes (`/add-book`, `/add-book/:id`), seamlessly redirecting unauthenticated users to `/login`.
4. **Reactive Login UI (`LoginComponent`)**: Provides a responsive, accessible sign-in form with real-time field validation, error alerts, and quick demo role selection.
5. **Role-Based UI Gating**: Granularly controls component rendering:
   - **"Add Book" Button**: Rendered only when authenticated as an `Admin`.
   - **"Delete" Button**: Rendered only for users with the `Admin` role.
   - **Public Users**: Browse the book catalog in read-only mode.

---

## 🏗️ Angular Authentication Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                        Angular 18+ Client SPA                          │
│                                                                        │
│   ┌─────────────────────┐   CanActivate    ┌────────────────────────┐  │
│   │   Browser URL Bar   ├── [authGuard] ──►│   BookFormComponent    │  │
│   │   /add-book         │   (Checks Token) │   (Protected Action)   │  │
│   └──────────┬──────────┘                  └────────────────────────┘  │
│              │ Token Missing                                           │
│              ▼ Redirect                                                │
│   ┌─────────────────────┐      login()     ┌────────────────────────┐  │
│   │   LoginComponent    ├─────────────────►│      AuthService       │  │
│   │  (Reactive Form)    │                  │  - token in localStorage│ │
│   └─────────────────────┘                  │  - decode claims (role)│  │
│                                            └───────────┬────────────┘  │
│                                                        │               │
│                                                        ▼ inject()      │
│   ┌────────────────────────────────────────────────────────────┐       │
│   │               authInterceptor (HttpInterceptorFn)          │       │
│   │               req.clone({ setHeaders: Bearer <token> })    │       │
│   └────────────────────────────┬───────────────────────────────┘       │
└────────────────────────────────┼───────────────────────────────────────┘
                                 │ HTTP JSON with Bearer Token
                                 ▼
                     ASP.NET Core Web API (:5000)
                     [Authorize] Middleware Pipeline
```

---

## 🔒 Security Concepts & LocalStorage Trade-offs

### Where to Store the JWT?
In this architecture, the token is saved in the browser's `localStorage` (`library_jwt_token`) alongside basic user claims in `library_user_info`.

| Storage Mechanism | Pros | Cons / Vulnerability | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **`localStorage`** | • Persists across browser tab refreshes.<br>• Easily accessible in JavaScript.<br>• No server state needed. | • Vulnerable to Cross-Site Scripting (**XSS**). Any compromised third-party script running on the page can access `localStorage.getItem()`. | • Sanitize all HTML inputs.<br>• Implement strict Content Security Policy (CSP).<br>• Short token expiration times (120 mins). |
| **`httpOnly` Cookies** | • Completely inaccessible to JavaScript (XSS immune).<br>• Browser transmits cookie automatically. | • Vulnerable to Cross-Site Request Forgery (**CSRF**). Requires Anti-Forgery tokens. | • SameSite=Strict cookies with CSRF token exchange. |

> [!NOTE]
> For this phase of the internship, `localStorage` combined with an Angular functional interceptor provides the clean, standard client-side architecture required before introducing refresh tokens and cookie authentication in later weeks.

---

## 🛠️ Step-by-Step Implementation Files

### 1. Centralized Authentication Service (`src/app/auth.service.ts`)
```typescript
@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly TOKEN_KEY = 'library_jwt_token';
  private readonly USER_KEY = 'library_user_info';
  
  private currentUserSubject = new BehaviorSubject<UserInfo | null>(this.getStoredUser());
  public currentUser$ = this.currentUserSubject.asObservable();

  login(credentials): Observable<AuthResponse> { ... }
  logout(): void { ... }
  isLoggedIn(): boolean { ... }
  getUserRole(): string | null { ... }
  isAdmin(): boolean { return this.getUserRole()?.toLowerCase() === 'admin'; }
}
```

### 2. Functional HTTP Interceptor (`src/app/auth.interceptor.ts`)
```typescript
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const token = authService.getToken();

  if (!token) {
    return next(req);
  }

  const authReq = req.clone({
    setHeaders: {
      Authorization: `Bearer ${token}`
    }
  });

  return next(authReq);
};
```

### 3. Application Config Registration (`src/app/app.config.ts`)
```typescript
export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    provideHttpClient(withInterceptors([authInterceptor])) // Functional interceptor registration
  ]
};
```

### 4. Functional Route Guard (`src/app/auth.guard.ts`)
```typescript
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

### 5. Role-Gated UI Elements
In `src/app/book-list/book-list.component.html`:
- The **+ Add New Book** button is conditionally displayed with `*ngIf="authService.isAdmin()"`.
- The **Delete** action button is displayed only if `*ngIf="authService.isAdmin()"`.
- Unauthenticated visitors see an informative banner: `"You are browsing in Public Read-Only Mode"`.

---

## 🧪 Testing & Verification Guide

### 1. Launching the Full Stack
```powershell
# Terminal 1: Backend (.NET Web API)
cd "Week_04/Week_04_Final_Project/backend"
& "D:\Software\dotnet\dotnet.exe" run

# Terminal 2: Frontend (Angular Client)
cd "Week_04/Week_04_Final_Project/frontend"
npm start
```
Access client in browser: `http://localhost:4200/`

### 2. Verification Checklist
- [x] **Route Guard:** Attempt navigating directly to `http://localhost:4200/add-book` while logged out. Verify the browser automatically redirects to `http://localhost:4200/login?returnUrl=%2Fadd-book`.
- [x] **Sign In Flow:** Sign in using an Admin account. Verify the navbar updates with the username and `ADMIN` badge, and redirection back to the intended URL succeeds.
- [x] **Network Tab Inspection:** In Browser DevTools (F12) -> Network tab, create a book. Inspect the request headers and verify `Authorization: Bearer ey...` is attached automatically.
- [x] **Role-Based UI:**
  - When logged in as **Standard User (`User`)**: The "+ Add New Book" and "Delete" buttons are hidden from the UI.
  - When logged in as **Administrator (`Admin`)**: Both "+ Add New Book" and "Delete" buttons are active.
- [x] **Sign Out Flow:** Click **Sign Out** in the top navbar. Verify `localStorage` token is destroyed and the UI reverts back to public read-only mode.

---

## 🌿 Git Checkpoint
```bash
git checkout -b feature/angular-auth
git add .
git commit -m "feat: add Angular login, auth interceptor, and route guards"
```
