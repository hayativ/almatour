import { Component, Input, inject, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { Subscription } from 'rxjs';
import { Painting } from '../services/paintings.service';
import { FavoritesService } from '../services/favorites.service';

@Component({
  selector: 'app-painting-card',
  imports: [CommonModule, RouterLink],
  templateUrl: './painting-card.html',
  styleUrl: './painting-card.css',
})
export class PaintingCard implements OnInit, OnDestroy {
  @Input() painting!: Painting;
  @Input() getImageUrl!: (imageId: string) => string;

  private readonly favoritesService = inject(FavoritesService);
  isFavorite = false;
  private subscription?: Subscription;

  ngOnInit(): void {
    this.subscription = this.favoritesService.isFavorite$(this.painting.id).subscribe(
      isFav => this.isFavorite = isFav
    );
  }

  ngOnDestroy(): void {
    this.subscription?.unsubscribe();
  }

  async toggleFavorite(event: Event): Promise<void> {
    event.preventDefault();
    event.stopPropagation();
    try {
      await this.favoritesService.toggleFavorite(this.painting.id);
    } catch (error) {
      console.error('Error toggling favorite:', error);
    }
  }
}
