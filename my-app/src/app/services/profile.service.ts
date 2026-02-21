import { Injectable, inject } from '@angular/core';
import { Database, ref, set, get, child } from '@angular/fire/database';
import { BehaviorSubject } from 'rxjs';

export interface ProfileData {
  photoURL: string | null;
  displayName?: string;
}

@Injectable({
  providedIn: 'root'
})
export class ProfileService {
  private readonly database = inject(Database);

  private readonly uploadingSubject = new BehaviorSubject<boolean>(false);
  public readonly uploading$ = this.uploadingSubject.asObservable();

  // Compress image using canvas and return as base64 data URL
  async compressImage(file: File, maxWidth = 400, maxHeight = 400, quality = 0.8): Promise<string> {
    const imageDataUrl = await this.readFileAsDataUrl(file);
    const img = await this.loadImage(imageDataUrl);
    return this.resizeAndCompressToBase64(img, maxWidth, maxHeight, quality);
  }

  private readFileAsDataUrl(file: File): Promise<string> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (event) => resolve(event.target?.result as string);
      reader.onerror = () => reject(new Error('Failed to read file'));
      reader.readAsDataURL(file);
    });
  }

  private loadImage(src: string): Promise<HTMLImageElement> {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => resolve(img);
      img.onerror = () => reject(new Error('Failed to load image'));
      img.src = src;
    });
  }

  private resizeAndCompressToBase64(img: HTMLImageElement, maxWidth: number, maxHeight: number, quality: number): Promise<string> {
    return new Promise((resolve, reject) => {
      const canvas = document.createElement('canvas');
      let { width, height } = img;

      // Calculate new dimensions while maintaining aspect ratio
      if (width > height && width > maxWidth) {
        height = Math.round((height * maxWidth) / width);
        width = maxWidth;
      } else if (height > maxHeight) {
        width = Math.round((width * maxHeight) / height);
        height = maxHeight;
      }

      canvas.width = width;
      canvas.height = height;

      const ctx = canvas.getContext('2d');
      if (!ctx) {
        reject(new Error('Failed to get canvas context'));
        return;
      }

      ctx.drawImage(img, 0, 0, width, height);
      
      // Return as base64 data URL
      const dataUrl = canvas.toDataURL('image/jpeg', quality);
      resolve(dataUrl);
    });
  }

  async uploadProfilePicture(userId: string, file: File): Promise<string> {
    this.uploadingSubject.next(true);

    try {
      // Compress the image and get base64 data URL
      const base64DataUrl = await this.compressImage(file);
      
      // Save base64 image directly to Realtime Database
      await this.saveProfileData(userId, { photoURL: base64DataUrl });

      return base64DataUrl;
    } finally {
      this.uploadingSubject.next(false);
    }
  }

  async saveProfileData(userId: string, data: Partial<ProfileData>): Promise<void> {
    const dbRef = ref(this.database, `users/${userId}`);
    
    // Get existing data and merge
    const existingData = await this.getProfileData(userId);
    const mergedData = { ...existingData, ...data };
    
    await set(dbRef, mergedData);
  }

  async getProfileData(userId: string): Promise<ProfileData | null> {
    try {
      const dbRef = ref(this.database);
      const snapshot = await get(child(dbRef, `users/${userId}`));
      
      if (snapshot.exists()) {
        return snapshot.val() as ProfileData;
      }
      return null;
    } catch (error: unknown) {
      console.error('Error getting profile data:', error);
      return null;
    }
  }
}
