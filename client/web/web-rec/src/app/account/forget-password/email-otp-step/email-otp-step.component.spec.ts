import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EmailOtpStepComponent } from './email-otp-step.component';

describe('EmailOtpStepComponent', () => {
  let component: EmailOtpStepComponent;
  let fixture: ComponentFixture<EmailOtpStepComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EmailOtpStepComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EmailOtpStepComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
