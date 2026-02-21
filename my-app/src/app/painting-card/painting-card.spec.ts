import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PaintingCard } from './painting-card';

describe('PaintingCard', () => {
  let component: PaintingCard;
  let fixture: ComponentFixture<PaintingCard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PaintingCard]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PaintingCard);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
