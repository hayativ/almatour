import { inject, Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { of } from 'rxjs';
import { map, switchMap, catchError } from 'rxjs/operators';
import { PaintingsService } from '../../services/paintings.service';
import * as PaintingActions from './painting.actions';

@Injectable()
export class PaintingEffects {
    private readonly actions$ = inject(Actions);
    private readonly paintingsService = inject(PaintingsService);

    // Using switchMap to cancel previous requests when a new search is triggered
    loadPaintings$ = createEffect(() =>
        this.actions$.pipe(
            ofType(PaintingActions.loadPaintings),
            switchMap(({ query, page, limit }) =>
                this.paintingsService.getPaintings(query, page, limit).pipe(
                    map((response) => PaintingActions.loadPaintingsSuccess({ 
                        paintings: response.paintings,
                        totalCount: response.totalCount,
                        currentPage: response.currentPage,
                        totalPages: response.totalPages
                    })),
                    catchError((error) => of(PaintingActions.loadPaintingsFailure({ error: error.message || 'Failed to load paintings' })))
                )
            )
        )
    );

    loadPainting$ = createEffect(() =>
        this.actions$.pipe(
            ofType(PaintingActions.loadPainting),
            switchMap(({ id }) =>
                this.paintingsService.getPaintingById(id).pipe(
                    map((painting) => PaintingActions.loadPaintingSuccess({ painting })),
                    catchError((error) => of(PaintingActions.loadPaintingFailure({ error: error.message || 'Failed to load painting' })))
                )
            )
        )
    );
}
