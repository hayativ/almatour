import { Component, OnInit, OnDestroy, inject, ElementRef, ViewChild } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { Observable, Subscription, firstValueFrom } from 'rxjs';
import { take } from 'rxjs/operators';
import { AuthService } from '../services/auth.service';
import { ProfileService } from '../services/profile.service';
import { TranslationService } from '../services/translation.service';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule, RouterLink, DatePipe],
  templateUrl: './profile.html',
  styleUrl: './profile.css'
})
export class Profile implements OnInit, OnDestroy {
  private readonly authService = inject(AuthService);
  private readonly profileService = inject(ProfileService);
  private readonly router = inject(Router);
  readonly translationService = inject(TranslationService);

  @ViewChild('fileInput') fileInput!: ElementRef<HTMLInputElement>;

  user$: Observable<any>;
  uploading$ = this.profileService.uploading$;
  
  customPhotoURL: string | null = null;
  uploadError: string | null = null;
  uploadSuccess: string | null = null;
  
  private subscription?: Subscription;

  get t() {
    return this.translationService.translations().profile;
  }

  constructor() {
    this.user$ = this.authService.getCurrentUser();
  }

  ngOnInit(): void {
    this.subscription = this.user$.subscribe(async (user) => {
      if (user) {
        const profileData = await this.profileService.getProfileData(user.uid);
        if (profileData?.photoURL) {
          this.customPhotoURL = profileData.photoURL;
        }
      }
    });
  }

  ngOnDestroy(): void {
    this.subscription?.unsubscribe();
  }

  triggerFileInput(): void {
    this.fileInput.nativeElement.click();
  }

  async onFileSelected(event: Event): Promise<void> {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    
    if (!file) return;

    // Validate file type
    if (!file.type.startsWith('image/')) {
      this.uploadError = 'Please select an image file';
      return;
    }

    // Validate file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      this.uploadError = 'Image must be less than 5MB';
      return;
    }

    this.uploadError = null;
    this.uploadSuccess = null;

    try {
      const user = await firstValueFrom(this.authService.currentUser$.pipe(take(1)));
      if (!user) {
        this.uploadError = 'You must be logged in to upload a profile picture';
        return;
      }

      const downloadURL = await this.profileService.uploadProfilePicture(user.uid, file);
      this.customPhotoURL = downloadURL;
      this.uploadSuccess = 'Profile picture updated successfully!';
      
      // Clear file input
      input.value = '';

      // Clear success message after 3 seconds
      setTimeout(() => {
        this.uploadSuccess = null;
      }, 3000);
    } catch (error) {
      console.error('Upload error:', error);
      this.uploadError = 'Failed to upload image. Please try again.';
    }
  }

  getDisplayPhotoURL(user: any): string | null {
    return this.customPhotoURL || user?.photoURL || null;
  }

  logout(): void {
    this.authService.logout()
      .then(() => {
        this.router.navigate(['/login']);
      })
      .catch((error) => {
        console.error('Logout error:', error);
      });
  }
}