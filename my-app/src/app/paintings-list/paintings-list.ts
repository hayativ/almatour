import { Component, OnInit, OnDestroy, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { Subject, Subscription } from 'rxjs';
import { debounceTime, distinctUntilChanged, switchMap } from 'rxjs/operators';
import { Store } from '@ngrx/store';
import { PaintingsService, Painting } from '../services/paintings.service';
import { TranslationService } from '../services/translation.service';
import { PaintingCard } from '../painting-card/painting-card';
import * as PaintingActions from '../painting/state/painting.actions';
import * as PaintingSelectors from '../painting/state/painting.selectors';

@Component({
  selector: 'app-paintings-list',
  standalone: true,
  imports: [CommonModule, FormsModule, PaintingCard],
  templateUrl: './paintings-list.html',
  styleUrls: ['./paintings-list.css']
})
export class PaintingsList implements OnInit, OnDestroy {
  readonly translationService = inject(TranslationService);
  
  paintings: Painting[] = [];
  searchTerm: string = '';
  errorMessage: string | null = null;
  loading = false;

  // Pagination properties
  currentPage = 1;
  totalPages = 1;
  totalCount = 0;
  itemsPerPage = 9;
  pageSizeOptions = [6, 9, 21];

  get t() {
    return this.translationService.translations().paintings;
  }

  private readonly searchSubject = new Subject<string>();
  private searchSubscription?: Subscription;
  private routeSubscription?: Subscription;
  private storeSubscription?: Subscription;
  // eslint-disable-next-line @typescript-eslint/prefer-readonly
  private paginationSubscription?: Subscription;

  constructor(
    private readonly paintingsService: PaintingsService,
    private readonly route: ActivatedRoute,
    private readonly router: Router,
    private readonly store: Store
  ) { }

  ngOnInit() {
    // Subscribe to paintings list state
    this.storeSubscription = this.store.select(PaintingSelectors.selectPaintingState).subscribe(state => {
      this.paintings = state.paintings;
      this.loading = state.loadingList;
      this.errorMessage = state.errorList;
      this.totalCount = state.totalCount;
      this.currentPage = state.currentPage;
      this.totalPages = state.totalPages;
    });

    // Search with debounce, distinctUntilChanged, and switchMap pattern
    this.searchSubscription = this.searchSubject.pipe(
      debounceTime(400),
      distinctUntilChanged(),
      switchMap((term) => {
        // Update URL and dispatch action
        this.updateQueryParams(term, 1, this.itemsPerPage);
        return []; // We dispatch action via URL change, so return empty
      })
    ).subscribe();

    // React to URL query param changes
    this.routeSubscription = this.route.queryParams.subscribe({
      next: (params) => {
        const query = params['q'] || '';
        const page = Number.parseInt(params['page'], 10) || 1;
        const limit = Number.parseInt(params['limit'], 10) || 9;
        
        this.searchTerm = query;
        this.currentPage = page;
        this.itemsPerPage = limit;
        
        this.store.dispatch(PaintingActions.loadPaintings({ 
          query: query || undefined, 
          page, 
          limit 
        }));
      }
    });
  }

  ngOnDestroy() {
    if (this.searchSubscription) {
      this.searchSubscription.unsubscribe();
    }
    if (this.routeSubscription) {
      this.routeSubscription.unsubscribe();
    }
    if (this.storeSubscription) {
      this.storeSubscription.unsubscribe();
    }
    if (this.paginationSubscription) {
      this.paginationSubscription.unsubscribe();
    }
  }

  onSearchChange(event: Event) {
    const value = (event.target as HTMLInputElement).value;
    this.searchSubject.next(value);
  }

  updateQueryParams(query: string, page: number, limit: number) {
    this.router.navigate([], {
      relativeTo: this.route,
      queryParams: { 
        q: query || null, 
        page: page > 1 ? page : null,
        limit: limit === 9 ? null : limit
      },
      queryParamsHandling: 'merge'
    });
  }

  // Pagination methods
  goToPage(page: number) {
    if (page >= 1 && page <= this.totalPages && page !== this.currentPage) {
      this.updateQueryParams(this.searchTerm, page, this.itemsPerPage);
    }
  }

  previousPage() {
    if (this.currentPage > 1) {
      this.goToPage(this.currentPage - 1);
    }
  }

  nextPage() {
    if (this.currentPage < this.totalPages) {
      this.goToPage(this.currentPage + 1);
    }
  }

  onPageSizeChange(event: Event) {
    const newSize = Number.parseInt((event.target as HTMLSelectElement).value, 10);
    this.itemsPerPage = newSize;
    // Reset to page 1 when changing page size
    this.updateQueryParams(this.searchTerm, 1, newSize);
  }

  loadPaintings() {
    this.searchTerm = '';
    this.updateQueryParams('', 1, this.itemsPerPage);
  }

  getImageUrl(imageId: string): string {
    return this.paintingsService.getImageUrl(imageId);
  }

  // Helper to generate page numbers for pagination UI
  getPageNumbers(): number[] {
    const pages: number[] = [];
    const maxVisiblePages = 5;
    
    let startPage = Math.max(1, this.currentPage - Math.floor(maxVisiblePages / 2));
    let endPage = Math.min(this.totalPages, startPage + maxVisiblePages - 1);
    
    // Adjust start if we're near the end
    if (endPage - startPage < maxVisiblePages - 1) {
      startPage = Math.max(1, endPage - maxVisiblePages + 1);
    }
    
    for (let i = startPage; i <= endPage; i++) {
      pages.push(i);
    }
    
    return pages;
  }
}
