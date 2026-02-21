import { Component, OnInit, OnDestroy, inject, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { Subscription } from 'rxjs';
import { AuthService } from '../services/auth.service';
import { ProfileService } from '../services/profile.service';
import { TranslationService } from '../services/translation.service';
import { LanguageSelector } from '../language-selector/language-selector';

@Component({
    selector: 'app-navbar',
    standalone: true,
    imports: [CommonModule, RouterLink, RouterLinkActive, LanguageSelector],
    templateUrl: './navbar.html',
    styleUrl: './navbar.css'
})
export class Navbar implements OnInit, OnDestroy {
    private readonly authService = inject(AuthService);
    private readonly profileService = inject(ProfileService);
    readonly translationService = inject(TranslationService);
    
    isLoggedIn = false;
    userPhotoURL: string | null = null;
    userInitial = '';
    
    private subscription?: Subscription;

    // Computed nav links based on current translation
    navLinks = computed(() => {
        const t = this.translationService.translations().nav;
        return [
            { path: '/', label: t.home, exact: true },
            { path: '/paintings', label: t.paintings, exact: false },
            { path: '/favorites', label: t.favorites, exact: false },
            { path: '/about', label: t.about, exact: false }
        ];
    });

    get title() {
        return this.translationService.translations().nav.title;
    }

    get loginText() {
        return this.translationService.translations().nav.login;
    }

    get profileText() {
        return this.translationService.translations().nav.profile;
    }

    ngOnInit(): void {
        this.subscription = this.authService.currentUser$.subscribe(async (user) => {
            this.isLoggedIn = !!user;
            if (user) {
                this.userInitial = (user.displayName || user.email || 'U')[0].toUpperCase();
                // Check for custom photo URL in Firestore
                const profileData = await this.profileService.getProfileData(user.uid);
                this.userPhotoURL = profileData?.photoURL || user.photoURL || null;
            } else {
                this.userPhotoURL = null;
                this.userInitial = '';
            }
        });
    }

    ngOnDestroy(): void {
        this.subscription?.unsubscribe();
    }
}
