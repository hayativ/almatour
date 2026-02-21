import { Component, OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { Store } from '@ngrx/store';
import { Subscription } from 'rxjs';
import { PaintingsService, Painting } from '../services/paintings.service';
import * as PaintingActions from '../painting/state/painting.actions';
import * as PaintingSelectors from '../painting/state/painting.selectors';

@Component({
    selector: 'app-painting-details',
    standalone: true,
    imports: [CommonModule, RouterLink],
    templateUrl: './painting-details.html',
    styleUrl: './painting-details.css'
})
export class PaintingDetails implements OnInit, OnDestroy {
    painting: Painting | null = null;
    errorMessage: string | null = null;
    isLoading = false;
    private storeSubscription?: Subscription;

    constructor(
        private readonly route: ActivatedRoute,
        private readonly router: Router,
        private readonly paintingsService: PaintingsService,
        private readonly cdr: ChangeDetectorRef,
        private readonly store: Store
    ) { }

    ngOnInit() {
        const id = this.route.snapshot.paramMap.get('id');

        this.storeSubscription = this.store.select(PaintingSelectors.selectPaintingState).subscribe(state => {
            this.painting = state.selectedPainting;
            this.isLoading = state.loadingDetails;
            this.errorMessage = state.errorDetails;
            this.cdr.detectChanges();
        });

        if (id) {
            this.loadPainting(id);
        } else {
            this.errorMessage = 'No painting ID provided';
        }
    }

    ngOnDestroy() {
        if (this.storeSubscription) {
            this.storeSubscription.unsubscribe();
        }
    }

    loadPainting(id: string | number) {
        this.store.dispatch(PaintingActions.loadPainting({ id }));
    }

    getImageUrl(imageId: string): string {
        return this.paintingsService.getImageUrl(imageId);
    }

    goBack() {
        this.router.navigate(['/paintings']);
    }
}
