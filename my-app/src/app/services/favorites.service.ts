import { Injectable, inject } from '@angular/core';
import { Database, ref, set, get, child } from '@angular/fire/database';
import { BehaviorSubject, Observable, firstValueFrom } from 'rxjs';
import { AuthService } from './auth.service';
import { map, take } from 'rxjs/operators';

const LOCAL_STORAGE_KEY = 'guest_favorites';

export interface FavoritesState {
  ids: number[];
  loading: boolean;
  mergeMessage: string | null;
}

@Injectable({
  providedIn: 'root'
})
export class FavoritesService {
  private readonly database = inject(Database);
  private readonly authService = inject(AuthService);

  private readonly favoritesSubject = new BehaviorSubject<FavoritesState>({
    ids: [],
    loading: false,
    mergeMessage: null
  });

  public readonly favorites$ = this.favoritesSubject.asObservable();
  public readonly favoriteIds$ = this.favorites$.pipe(map(state => state.ids));

  constructor() {
    // Listen to auth state changes to load/merge favorites
    this.authService.currentUser$.subscribe(user => {
      if (user) {
        this.handleUserLogin(user.uid);
      } else {
        this.loadGuestFavorites();
      }
    });
  }

  private async handleUserLogin(userId: string): Promise<void> {
    this.setLoading(true);
    
    const localFavorites = this.getLocalFavorites();
    const serverFavorites = await this.getServerFavorites(userId);

    if (localFavorites.length > 0 && serverFavorites.length === 0) {
      // First login - migrate local favorites to server
      await this.saveServerFavorites(userId, localFavorites);
      this.clearLocalFavorites();
      this.updateFavorites(localFavorites, 'Your favorites have been saved to your account!');
    } else if (localFavorites.length > 0 && serverFavorites.length > 0) {
      // Merge local and server favorites
      const mergedFavorites = [...new Set([...serverFavorites, ...localFavorites])];
      const newItems = mergedFavorites.length - serverFavorites.length;
      await this.saveServerFavorites(userId, mergedFavorites);
      this.clearLocalFavorites();
      this.updateFavorites(mergedFavorites, `Merged ${newItems} new item(s) with your account favorites!`);
    } else {
      // Just load server favorites
      this.updateFavorites(serverFavorites, null);
    }

    this.setLoading(false);
  }

  private loadGuestFavorites(): void {
    const favorites = this.getLocalFavorites();
    this.updateFavorites(favorites, null);
  }

  // Local storage methods for guests
  private getLocalFavorites(): number[] {
    try {
      const stored = localStorage.getItem(LOCAL_STORAGE_KEY);
      return stored ? JSON.parse(stored) : [];
    } catch {
      return [];
    }
  }

  private saveLocalFavorites(ids: number[]): void {
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(ids));
  }

  private clearLocalFavorites(): void {
    localStorage.removeItem(LOCAL_STORAGE_KEY);
  }

  // Realtime Database methods for authenticated users
  private async getServerFavorites(userId: string): Promise<number[]> {
    try {
      const dbRef = ref(this.database);
      const snapshot = await get(child(dbRef, `users/${userId}/favorites`));
      
      if (snapshot.exists()) {
        return snapshot.val() || [];
      }
      return [];
    } catch (error: unknown) {
      console.error('Error getting server favorites:', error);
      return this.getLocalFavorites(); // Fallback to local on any error
    }
  }

  private async saveServerFavorites(userId: string, ids: number[]): Promise<void> {
    try {
      const dbRef = ref(this.database, `users/${userId}/favorites`);
      await set(dbRef, ids);
    } catch (error) {
      console.error('Error saving server favorites:', error);
    }
  }

  // Public methods
  async addFavorite(paintingId: number): Promise<void> {
    const currentState = this.favoritesSubject.value;
    if (currentState.ids.includes(paintingId)) return;

    const newIds = [...currentState.ids, paintingId];
    
    const user = await firstValueFrom(this.authService.currentUser$.pipe(take(1)));
    
    if (user) {
      await this.saveServerFavorites(user.uid, newIds);
    } else {
      this.saveLocalFavorites(newIds);
    }

    this.updateFavorites(newIds, null);
  }

  async removeFavorite(paintingId: number): Promise<void> {
    const currentState = this.favoritesSubject.value;
    const newIds = currentState.ids.filter(id => id !== paintingId);
    
    const user = await firstValueFrom(this.authService.currentUser$.pipe(take(1)));
    
    if (user) {
      await this.saveServerFavorites(user.uid, newIds);
    } else {
      this.saveLocalFavorites(newIds);
    }

    this.updateFavorites(newIds, null);
  }

  async toggleFavorite(paintingId: number): Promise<void> {
    console.log('toggleFavorite called with:', paintingId);
    console.log('Current favorites:', this.favoritesSubject.value.ids);
    console.log('Is favorite?', this.isFavorite(paintingId));
    
    if (this.isFavorite(paintingId)) {
      await this.removeFavorite(paintingId);
    } else {
      await this.addFavorite(paintingId);
    }
    
    console.log('Updated favorites:', this.favoritesSubject.value.ids);
  }

  isFavorite(paintingId: number): boolean {
    return this.favoritesSubject.value.ids.includes(paintingId);
  }

  isFavorite$(paintingId: number): Observable<boolean> {
    return this.favoriteIds$.pipe(
      map(ids => ids.includes(paintingId))
    );
  }

  clearMergeMessage(): void {
    const current = this.favoritesSubject.value;
    this.favoritesSubject.next({ ...current, mergeMessage: null });
  }

  private updateFavorites(ids: number[], message: string | null): void {
    this.favoritesSubject.next({
      ...this.favoritesSubject.value,
      ids,
      mergeMessage: message
    });
  }

  private setLoading(loading: boolean): void {
    this.favoritesSubject.next({
      ...this.favoritesSubject.value,
      loading
    });
  }
}
