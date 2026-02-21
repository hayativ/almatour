import { Injectable } from '@angular/core';
import { Auth, user, signInWithEmailAndPassword, createUserWithEmailAndPassword, signOut } from '@angular/fire/auth';
import { Observable, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

export interface AuthError {
  code: string;
  message: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  public readonly currentUser$: Observable<any | null>;

  constructor(private readonly auth: Auth) {
    this.currentUser$ = user(this.auth);
  }

  signup(email: string, password: string): Promise<void> {
    return createUserWithEmailAndPassword(this.auth, email, password)
      .then((userCredential) => {
        if (userCredential.user) {
          console.log('User signed up successfully:', userCredential.user.email);
        }
      })
      .catch((error) => {
        const authError = this.formatAuthError(error);
        console.error('Signup error:', authError);
        throw authError;
      });
  }

  login(email: string, password: string): Promise<void> {
    return signInWithEmailAndPassword(this.auth, email, password)
      .then((userCredential) => {
        if (userCredential.user) {
          console.log('User logged in successfully:', userCredential.user.email);
        }
      })
      .catch((error) => {
        const authError = this.formatAuthError(error);
        console.error('Login error:', authError);
        throw authError;
      });
  }

  logout(): Promise<void> {
    return signOut(this.auth)
      .then(() => {
        console.log('User logged out successfully');
      })
      .catch((error) => {
        const authError = this.formatAuthError(error);
        console.error('Logout error:', authError);
        throw authError;
      });
  }

  getCurrentUser(): Observable<any | null> {
    return this.currentUser$;
  }

  isAuthenticated(): Observable<boolean> {
    return this.currentUser$.pipe(
      map(user => user !== null),
      catchError(() => of(false))
    );
  }

  private formatAuthError(error: any): AuthError {
    const commonErrors: { [key: string]: string } = {
      'auth/email-already-in-use': 'This email is already registered. Please use a different email.',
      'auth/invalid-email': 'Please enter a valid email address.',
      'auth/operation-not-allowed': 'Email/password accounts are not enabled. Please contact support.',
      'auth/weak-password': 'Password is too weak. Please choose a stronger password.',
      'auth/user-disabled': 'This account has been disabled. Please contact support.',
      'auth/user-not-found': 'No account found with this email address.',
      'auth/wrong-password': 'Incorrect password. Please try again.',
      'auth/too-many-requests': 'Too many failed attempts. Please try again later.',
      'auth/network-request-failed': 'Network error. Please check your connection and try again.',
      'auth/requires-recent-login': 'This operation requires recent authentication. Please log in again.'
    };

    return {
      code: error.code || 'auth/unknown-error',
      message: commonErrors[error.code] || error.message || 'An unknown error occurred during authentication.'
    };
  }
}