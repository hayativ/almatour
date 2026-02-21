import { createAction, props } from '@ngrx/store';
import { Painting } from '../../services/paintings.service';

export const loadPaintings = createAction(
    '[Painting List] Load Paintings',
    props<{ query?: string; page?: number; limit?: number }>()
);

export const loadPaintingsSuccess = createAction(
    '[Painting API] Load Paintings Success',
    props<{ paintings: Painting[]; totalCount: number; currentPage: number; totalPages: number }>()
);

export const loadPaintingsFailure = createAction(
    '[Painting API] Load Paintings Failure',
    props<{ error: string }>()
);

export const loadPainting = createAction(
    '[Painting Details] Load Painting',
    props<{ id: string | number }>()
);

export const loadPaintingSuccess = createAction(
    '[Painting API] Load Painting Success',
    props<{ painting: Painting }>()
);

export const loadPaintingFailure = createAction(
    '[Painting API] Load Painting Failure',
    props<{ error: string }>()
);
