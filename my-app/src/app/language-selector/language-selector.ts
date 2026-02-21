import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TranslationService, Language } from '../services/translation.service';

@Component({
    selector: 'app-language-selector',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './language-selector.html',
    styleUrl: './language-selector.css'
})
export class LanguageSelector {
    readonly translationService = inject(TranslationService);
    
    isOpen = false;

    get currentLanguage() {
        return this.translationService.availableLanguages.find(
            lang => lang.code === this.translationService.currentLanguage()
        );
    }

    toggleDropdown(): void {
        this.isOpen = !this.isOpen;
    }

    selectLanguage(code: Language): void {
        this.translationService.setLanguage(code);
        this.isOpen = false;
    }

    closeDropdown(): void {
        this.isOpen = false;
    }
}
