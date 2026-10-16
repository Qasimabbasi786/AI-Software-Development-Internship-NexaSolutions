import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, ActivatedRoute, RouterLink } from '@angular/router';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup;
  isSubmitting: boolean = false;
  errorMessage: string = '';
  returnUrl: string = '/';

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.loginForm = this.fb.group({
      username: ['', [Validators.required, Validators.minLength(2)]],
      password: ['', [Validators.required, Validators.minLength(4)]]
    });
  }

  ngOnInit(): void {
    this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/';
    // If already logged in, redirect immediately
    if (this.authService.isLoggedIn()) {
      this.router.navigate([this.returnUrl]);
    }
  }

  onSubmit(): void {
    if (this.loginForm.invalid || this.isSubmitting) {
      return;
    }

    this.isSubmitting = true;
    this.errorMessage = '';

    const { username, password } = this.loginForm.value;
    this.authService.login({ username, password }).subscribe({
      next: () => {
        this.isSubmitting = false;
        this.router.navigateByUrl(this.returnUrl);
      },
      error: (err) => {
        this.isSubmitting = false;
        this.errorMessage = err.error?.message || 'Invalid username or password. Please try again.';
      }
    });
  }

  fillQuickDemo(role: 'admin' | 'user'): void {
    if (role === 'admin') {
      this.loginForm.patchValue({
        username: 'admin',
        password: 'AdminPassword123!'
      });
    } else {
      this.loginForm.patchValue({
        username: 'sam',
        password: 'UserPassword123!'
      });
    }
  }
}
