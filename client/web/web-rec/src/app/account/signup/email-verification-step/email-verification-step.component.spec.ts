import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EmailVerificationStepComponent } from './email-verification-step.component';

describe('EmailVerificationStepComponent', () => {
  let component: EmailVerificationStepComponent;
  let fixture: ComponentFixture<EmailVerificationStepComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EmailVerificationStepComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EmailVerificationStepComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
