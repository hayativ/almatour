import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService, AuthError } from '../services/auth.service';
import { TranslationService } from '../services/translation.service';

@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './signup.html',
  styleUrl: './signup.css'
})
export class Signup {
  readonly translationService = inject(TranslationService);
  
  email = '';
  password = '';
  confirmPassword = '';
  isLoading = false;
  errorMessage = '';

  // Validation state for real-time feedback
  emailError = '';
  passwordError = '';
  confirmPasswordError = '';

  get t() {
    return this.translationService.translations().signup;
  }

  constructor(
    private readonly authService: AuthService,
    private readonly router: Router
  ) {}

  // Email validation regex pattern
  private readonly emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

  // Password must have: 8+ chars, 1 special char, 1 number
  private readonly passwordMinLength = 8;
  private readonly specialCharPattern = /[!@#$%^&*(),.?":{}|<>[\]\\;'`~_+=\-/]/;
  private readonly numberPattern = /\d/;

  validateEmail(): boolean {
    if (!this.email) {
      this.emailError = 'Email is required';
      return false;
    }
    if (!this.emailPattern.test(this.email)) {
      this.emailError = 'Please enter a valid email address';
      return false;
    }
    this.emailError = '';
    return true;
  }

  validatePassword(): boolean {
    const errors: string[] = [];

    if (!this.password) {
      this.passwordError = 'Password is required';
      return false;
    }

    if (this.password.length < this.passwordMinLength) {
      errors.push(`at least ${this.passwordMinLength} characters`);
    }

    if (!this.specialCharPattern.test(this.password)) {
      errors.push('at least one special character');
    }

    if (!this.numberPattern.test(this.password)) {
      errors.push('at least one number');
    }

    if (errors.length > 0) {
      this.passwordError = `Password must contain ${errors.join(', ')}`;
      return false;
    }

    this.passwordError = '';
    return true;
  }

  validateConfirmPassword(): boolean {
    if (!this.confirmPassword) {
      this.confirmPasswordError = 'Please confirm your password';
      return false;
    }
    if (this.password !== this.confirmPassword) {
      this.confirmPasswordError = 'Passwords do not match';
      return false;
    }
    this.confirmPasswordError = '';
    return true;
  }

  onEmailChange() {
    this.validateEmail();
  }

  onPasswordChange() {
    this.validatePassword();
    if (this.confirmPassword) {
      this.validateConfirmPassword();
    }
  }

  onConfirmPasswordChange() {
    this.validateConfirmPassword();
  }

  onSubmit() {
    // Validate all fields
    const isEmailValid = this.validateEmail();
    const isPasswordValid = this.validatePassword();
    const isConfirmPasswordValid = this.validateConfirmPassword();

    if (!isEmailValid || !isPasswordValid || !isConfirmPasswordValid) {
      this.errorMessage = 'Please fix the validation errors above';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    this.authService.signup(this.email, this.password)
      .then(() => {
        this.router.navigate(['/profile']);
      })
      .catch((error: AuthError) => {
        this.errorMessage = error.message;
      })
      .finally(() => {
        this.isLoading = false;
      });
  }
}