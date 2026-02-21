import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { TranslationService } from '../services/translation.service';

@Component({
  selector: 'app-footer',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './footer.html',
  styleUrls: ['./footer.css']
})
export class Footer {
  readonly translationService = inject(TranslationService);
  
  ticketCnt = 0;
  email = '';
  showPaymentMessage = false;

  get t() {
    return this.translationService.translations().footer;
  }

  ticket() {
    this.ticketCnt++;
  }

  buy() {
    this.showPaymentMessage = true;
  }
}
