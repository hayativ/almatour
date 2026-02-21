import { Component, inject, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TranslationService } from '../services/translation.service';

@Component({
    selector: 'app-about',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './about.html',
    styleUrl: './about.css'
})
export class About {
    readonly translationService = inject(TranslationService);
    
    foundedYear = '1879';
    collectionSize = '300,000+';

    schedule = {
        weekdays: 'Monday - Friday: 10:00 AM - 8:00 PM',
        weekends: 'Saturday - Sunday: 10:00 AM - 5:00 PM'
    };

    get t() {
        return this.translationService.translations().about;
    }

    facts = computed(() => {
        const factT = this.t.facts;
        return [
            { title: factT.worldClass.title, description: factT.worldClass.description },
            { title: factT.historic.title, description: factT.historic.description },
            { title: factT.diverse.title, description: factT.diverse.description },
            { title: factT.educational.title, description: factT.educational.description }
        ];
    });
}
