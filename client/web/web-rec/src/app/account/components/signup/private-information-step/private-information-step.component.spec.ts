import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PrivateInformationStepComponent } from './private-information-step.component';

describe('PrivateInformationStepComponent', () => {
  let component: PrivateInformationStepComponent;
  let fixture: ComponentFixture<PrivateInformationStepComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PrivateInformationStepComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PrivateInformationStepComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
