import { createReducer, on } from '@ngrx/store';
import { Painting } from '../../services/paintings.service';
import * as PaintingActions from './painting.actions';

export interface PaintingState {
    paintings: Painting[];
    selectedPainting: Painting | null;
    loadingList: boolean;
    loadingDetails: boolean;
    errorList: string | null;
    errorDetails: string | null;
    // Pagination state
    totalCount: number;
    currentPage: number;
    totalPages: number;
    itemsPerPage: number;
}

export const initialState: PaintingState = {
    paintings: [],
    selectedPainting: null,
    loadingList: false,
    loadingDetails: false,
    errorList: null,
    errorDetails: null,
    // Pagination initial state
    totalCount: 0,
    currentPage: 1,
    totalPages: 1,
    itemsPerPage: 9,
};

export const paintingReducer = createReducer(
    initialState,
    on(PaintingActions.loadPaintings, (state) => ({
        ...state,
        loadingList: true,
        errorList: null,
    })),
    on(PaintingActions.loadPaintingsSuccess, (state, { paintings, totalCount, currentPage, totalPages }) => ({
        ...state,
        paintings,
        totalCount,
        currentPage,
        totalPages,
        loadingList: false,
    })),
    on(PaintingActions.loadPaintingsFailure, (state, { error }) => ({
        ...state,
        loadingList: false,
        errorList: error,
    })),
    on(PaintingActions.loadPainting, (state) => ({
        ...state,
        loadingDetails: true,
        errorDetails: null,
        selectedPainting: null,
    })),
    on(PaintingActions.loadPaintingSuccess, (state, { painting }) => ({
        ...state,
        selectedPainting: painting,
        loadingDetails: false,
    })),
    on(PaintingActions.loadPaintingFailure, (state, { error }) => ({
        ...state,
        loadingDetails: false,
        errorDetails: error,
    }))
);
