import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AccountInformationStepComponent } from './account-information-step.component';

describe('AccountInformationStepComponent', () => {
  let component: AccountInformationStepComponent;
  let fixture: ComponentFixture<AccountInformationStepComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AccountInformationStepComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AccountInformationStepComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
