import { createFeatureSelector, createSelector } from '@ngrx/store';
import { PaintingState } from './painting.reducer';

export const selectPaintingState = createFeatureSelector<PaintingState>('paintings');

export const selectPaintingList = createSelector(
    selectPaintingState,
    (state) => state.paintings
);

export const selectListLoading = createSelector(
    selectPaintingState,
    (state) => state.loadingList
);

export const selectListError = createSelector(
    selectPaintingState,
    (state) => state.errorList
);

export const selectSelectedPainting = createSelector(
    selectPaintingState,
    (state) => state.selectedPainting
);

export const selectDetailsLoading = createSelector(
    selectPaintingState,
    (state) => state.loadingDetails
);

export const selectDetailsError = createSelector(
    selectPaintingState,
    (state) => state.errorDetails
);

// Pagination selectors
export const selectTotalCount = createSelector(
    selectPaintingState,
    (state) => state.totalCount
);

export const selectCurrentPage = createSelector(
    selectPaintingState,
    (state) => state.currentPage
);

export const selectTotalPages = createSelector(
    selectPaintingState,
    (state) => state.totalPages
);

export const selectItemsPerPage = createSelector(
    selectPaintingState,
    (state) => state.itemsPerPage
);

export const selectPaginationInfo = createSelector(
    selectPaintingState,
    (state) => ({
        totalCount: state.totalCount,
        currentPage: state.currentPage,
        totalPages: state.totalPages,
        itemsPerPage: state.itemsPerPage
    })
);
