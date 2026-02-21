import { Component, OnInit, OnDestroy, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { Subscription, firstValueFrom } from 'rxjs';
import { FavoritesService } from '../services/favorites.service';
import { PaintingsService, Painting } from '../services/paintings.service';
import { TranslationService } from '../services/translation.service';

@Component({
  selector: 'app-favorites',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './favorites.html',
  styleUrl: './favorites.css'
})
export class Favorites implements OnInit, OnDestroy {
  private readonly favoritesService = inject(FavoritesService);
  private readonly paintingsService = inject(PaintingsService);
  readonly translationService = inject(TranslationService);

  favoritePaintings: Painting[] = [];
  loading = false;
  mergeMessage: string | null = null;
  private subscription?: Subscription;

  get t() {
    return this.translationService.translations().favorites;
  }

  ngOnInit(): void {
    this.subscription = this.favoritesService.favorites$.subscribe(state => {
      this.mergeMessage = state.mergeMessage;
      this.loading = state.loading;
      
      if (state.ids.length > 0 && !state.loading) {
        this.loadFavoritePaintings(state.ids);
      } else if (state.ids.length === 0) {
        this.favoritePaintings = [];
      }
    });
  }

  ngOnDestroy(): void {
    this.subscription?.unsubscribe();
  }

  private async loadFavoritePaintings(ids: number[]): Promise<void> {
    this.loading = true;
    const paintings: Painting[] = [];

    for (const id of ids) {
      try {
        const painting = await firstValueFrom(this.paintingsService.getPaintingById(id));
        if (painting) {
          paintings.push(painting);
        }
      } catch (error) {
        console.error(`Failed to load painting ${id}:`, error);
      }
    }

    this.favoritePaintings = paintings;
    this.loading = false;
  }

  getImageUrl(imageId: string): string {
    return this.paintingsService.getImageUrl(imageId);
  }

  removeFavorite(paintingId: number): void {
    this.favoritesService.removeFavorite(paintingId);
  }

  dismissMergeMessage(): void {
    this.favoritesService.clearMergeMessage();
  }
}
