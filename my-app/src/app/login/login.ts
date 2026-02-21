import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService, AuthError } from '../services/auth.service';
import { TranslationService } from '../services/translation.service';

@Component({
    selector: 'app-login',
    standalone: true,
    imports: [CommonModule, FormsModule, RouterLink],
    templateUrl: './login.html',
    styleUrl: './login.css'
})
export class Login {
    readonly translationService = inject(TranslationService);
    
    email = '';
    password = '';
    isLoading = false;
    errorMessage = '';

    get t() {
        return this.translationService.translations().login;
    }

    constructor(
        private readonly authService: AuthService,
        private readonly router: Router
    ) {}

    onSubmit() {
        if (!this.email || !this.password) {
            this.errorMessage = 'Please enter both email and password';
            return;
        }

        this.isLoading = true;
        this.errorMessage = '';

        this.authService.login(this.email, this.password)
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
