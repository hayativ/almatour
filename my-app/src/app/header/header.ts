import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-header',
  imports: [CommonModule, FormsModule],
  templateUrl: './header.html',
  styleUrl: './header.css'
})
export class Header {
  title = 'Art Institue of Chicago';
  schedule = 'Daily 10-8';
  message = '';
  exhibitionButton = 'Become a member';
  photoUrl = "https://artic-web.imgix.net/905abd91-5c0d-451b-9319-f7cd1505bc33/IM026911_002-web.jpg?w=1200&h=800&fit=crop";
  
  showSubscribe = false;
  email = '';
  subscribeMessage = '';
  subscribeButton = 'Subscribe';

  toggleMessage() {
    if (this.message) {
      this.showSubscribe = false;
    } else {
      this.showSubscribe = true;
    }
  }

  subscribe() {
    if (this.email.trim()) {
      this.subscribeMessage = `Thank you, ${this.email}!`;
      this.email = '';
    } else {
      this.subscribeMessage = 'Please enter an email';
    }
  }
}
