import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StepperGroupComponent } from './stepper-group.component';

describe('StepperGroupComponent', () => {
  let component: StepperGroupComponent;
  let fixture: ComponentFixture<StepperGroupComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StepperGroupComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(StepperGroupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
