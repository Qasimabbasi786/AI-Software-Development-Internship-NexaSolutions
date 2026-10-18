import { CanActivateFn, Router } from '@angular/router';
import { inject } from '@angular/core';
import { AuthService } from './auth.service';

/**
 * Functional Route Guard for Angular 18+
 * Guards write and administrative routes, redirecting unauthenticated users to /login.
 */
export const authGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  const router = inject(Router);

  if (authService.isLoggedIn()) {
    return true;
  }

  // Preserve attempted URL for redirect after successful login
  router.navigate(['/login'], { queryParams: { returnUrl: state.url } });
  return false;
};
