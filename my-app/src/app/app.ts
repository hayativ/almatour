import { Component, signal, OnInit, OnDestroy, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterOutlet, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs/operators';
import { Navbar } from './navbar/navbar';
import { Footer } from './footer/footer';

@Component({
  selector: 'app-root',
  imports: [CommonModule, RouterOutlet, Navbar, Footer],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit, OnDestroy {
  protected readonly title = signal('my-app');
  isOffline = signal(false);
  showOfflinePage = signal(false);

  private readonly router = inject(Router);
  private currentUrl = '/';

  private readonly onlineHandler = () => {
    this.isOffline.set(false);
    this.showOfflinePage.set(false);
  };

  private readonly offlineHandler = () => {
    this.isOffline.set(true);
    // Only show offline page if not already on offline or favorites page
    if (!this.currentUrl.includes('/offline') && !this.currentUrl.includes('/favorites')) {
      this.showOfflinePage.set(true);
    }
  };

  ngOnInit(): void {
    // Track current URL
    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd)
    ).subscribe((event: NavigationEnd) => {
      this.currentUrl = event.urlAfterRedirects;
    });

    // Check initial state
    this.isOffline.set(!navigator.onLine);

    // Listen for connectivity changes
    globalThis.addEventListener('online', this.onlineHandler);
    globalThis.addEventListener('offline', this.offlineHandler);
  }

  ngOnDestroy(): void {
    globalThis.removeEventListener('online', this.onlineHandler);
    globalThis.removeEventListener('offline', this.offlineHandler);
  }

  goToOfflinePage(): void {
    this.showOfflinePage.set(false);
    this.router.navigate(['/offline']);
  }

  dismissOfflinePrompt(): void {
    this.showOfflinePage.set(false);
  }
}
