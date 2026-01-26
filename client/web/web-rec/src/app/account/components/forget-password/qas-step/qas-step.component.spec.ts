import { ComponentFixture, TestBed } from '@angular/core/testing';

import { QasStepComponent } from './qas-step.component';

describe('QasStepComponent', () => {
  let component: QasStepComponent;
  let fixture: ComponentFixture<QasStepComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [QasStepComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(QasStepComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
