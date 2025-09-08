import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Emotion } from './emotion';

describe('Emotion', () => {
  let component: Emotion;
  let fixture: ComponentFixture<Emotion>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Emotion]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Emotion);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
