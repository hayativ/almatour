import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { Store } from '@ngrx/store';
import { Observable } from 'rxjs';
import { Painting, PaintingsService } from '../services/paintings.service';
import { TranslationService } from '../services/translation.service';
import * as PaintingActions from '../painting/state/painting.actions';
import * as PaintingSelectors from '../painting/state/painting.selectors';

@Component({
    selector: 'app-home',
    standalone: true,
    imports: [CommonModule, RouterLink],
    templateUrl: './home.html',
    styleUrl: './home.css'
})
export class Home implements OnInit {
    readonly translationService = inject(TranslationService);
    featuredPaintings$: Observable<Painting[]>;
    loading$: Observable<boolean>;

    get t() {
        return this.translationService.translations().home;
    }

    constructor(
        private readonly paintingsService: PaintingsService,
        private readonly store: Store
    ) {
        this.featuredPaintings$ = this.store.select(PaintingSelectors.selectPaintingList);
        this.loading$ = this.store.select(PaintingSelectors.selectListLoading);
    }

    ngOnInit() {
        this.store.dispatch(PaintingActions.loadPaintings({ query: '' }));
    }

    getImageUrl(imageId: string): string {
        return this.paintingsService.getImageUrl(imageId);
    }

    onImageError(event: Event) {
        const img = event.target as HTMLImageElement;
        img.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="400" height="300"%3E%3Crect fill="%23ddd" width="400" height="300"/%3E%3Ctext fill="%23999" x="50%25" y="50%25" dominant-baseline="middle" text-anchor="middle" font-family="sans-serif" font-size="18"%3EImage Unavailable%3C/text%3E%3C/svg%3E';
    }
}
