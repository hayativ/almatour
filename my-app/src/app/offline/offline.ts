import { Component, inject, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { TranslationService } from '../services/translation.service';

@Component({
    selector: 'app-offline',
    standalone: true,
    imports: [CommonModule, RouterLink],
    templateUrl: './offline.html',
    styleUrl: './offline.css'
})
export class Offline {
    readonly translationService = inject(TranslationService);

    get t() {
        return this.translationService.translations().offline;
    }

    features = computed(() => {
        const t = this.t;
        return [
            {
                icon: '🖼️',
                title: t.cachedArtworks,
                description: t.cachedArtworksDesc
            },
            {
                icon: '❤️',
                title: t.yourFavorites,
                description: t.yourFavoritesDesc
            },
            {
                icon: '🔄',
                title: t.autoReconnect,
                description: t.autoReconnectDesc
            }
        ];
    });

    retryConnection(): void {
        window.location.reload();
    }
}
