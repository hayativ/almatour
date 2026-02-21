import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PaintingsList } from './paintings-list';

describe('PainitingsList', () => {
  let component: PaintingsList;
  let fixture: ComponentFixture<PaintingsList>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PaintingsList]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PaintingsList);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
