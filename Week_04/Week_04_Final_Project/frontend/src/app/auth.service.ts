import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject, tap } from 'rxjs';
import { environment } from '../environments/environment';

export interface UserInfo {
  userId?: number;
  username: string;
  email?: string;
  role: string;
}

export interface AuthResponse {
  message: string;
  token: string;
  user: UserInfo;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly TOKEN_KEY = 'library_jwt_token';
  private readonly USER_KEY = 'library_user_info';
  private readonly authApiUrl = `${environment.apiUrl}/auth`;

  private currentUserSubject = new BehaviorSubject<UserInfo | null>(this.getStoredUser());
  public currentUser$ = this.currentUserSubject.asObservable();

  constructor(private http: HttpClient) {}

  login(credentials: { username: string; password: string }): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.authApiUrl}/login`, credentials).pipe(
      tap((res) => {
        if (res && res.token) {
          localStorage.setItem(this.TOKEN_KEY, res.token);
          const userInfo = res.user || this.decodeToken(res.token);
          localStorage.setItem(this.USER_KEY, JSON.stringify(userInfo));
          this.currentUserSubject.next(userInfo);
        }
      })
    );
  }

  register(userData: { username: string; email?: string; password: string; role?: string }): Observable<any> {
    return this.http.post(`${this.authApiUrl}/register`, userData);
  }

  logout(): void {
    localStorage.removeItem(this.TOKEN_KEY);
    localStorage.removeItem(this.USER_KEY);
    this.currentUserSubject.next(null);
  }

  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  isLoggedIn(): boolean {
    const token = this.getToken();
    if (!token) return false;

    // Check expiration if possible
    try {
      const payload = this.decodeToken(token);
      if (payload && payload.exp) {
        const isExpired = Date.now() >= payload.exp * 1000;
        if (isExpired) {
          this.logout();
          return false;
        }
      }
      return true;
    } catch {
      return true;
    }
  }

  getUserRole(): string | null {
    const currentUser = this.currentUserSubject.value;
    if (currentUser && currentUser.role) {
      return currentUser.role;
    }

    const token = this.getToken();
    if (token) {
      const decoded = this.decodeToken(token);
      return decoded?.role || decoded?.['http://schemas.microsoft.com/ws/2008/06/identity/claims/role'] || null;
    }
    return null;
  }

  isAdmin(): boolean {
    const role = this.getUserRole();
    return role?.toLowerCase() === 'admin';
  }

  getUsername(): string | null {
    const user = this.currentUserSubject.value;
    return user ? user.username : null;
  }

  private getStoredUser(): UserInfo | null {
    const userJson = localStorage.getItem(this.USER_KEY);
    if (userJson) {
      try {
        return JSON.parse(userJson);
      } catch {
        return null;
      }
    }
    return null;
  }

  private decodeToken(token: string): any {
    try {
      const parts = token.split('.');
      if (parts.length !== 3) return null;
      const base64Url = parts[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      );
      return JSON.parse(jsonPayload);
    } catch {
      return null;
    }
  }
}
