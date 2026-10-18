import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from './auth.service';

/**
 * Functional HTTP Interceptor for Angular 18+
 * Automatically attaches Authorization: Bearer <token> header to all outgoing requests
 * if a valid token is present in the AuthService / localStorage.
 */
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const token = authService.getToken();

  // Week 8 Part C: Generate or propagate X-Correlation-Id across all Angular requests
  const correlationId = req.headers.get('X-Correlation-Id') || 'ang_' + Math.random().toString(36).substring(2, 12);

  const headers: Record<string, string> = {
    'X-Correlation-Id': correlationId
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const enhancedReq = req.clone({
    setHeaders: headers
  });

  return next(enhancedReq);
};

