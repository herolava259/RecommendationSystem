import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { SignupManagerService } from '../../../services/signup-manager.service';

@Component({
  selector: 'app-account-information-step',
  imports: [CommonModule,ReactiveFormsModule],
  templateUrl: './account-information-step.component.html',
  styleUrl: './account-information-step.component.scss'
})
export class AccountInformationStepComponent {

  /**
   *
   */
  // eslint-disable-next-line @angular-eslint/prefer-inject
  constructor(private signupManager: SignupManagerService) {

  }

  private fb = inject(FormBuilder);

  accountInformationForm = this.fb.group({
    email: ['', Validators.required, Validators.email],
    signInName: ['', Validators.required, Validators.minLength(4), Validators.maxLength(20)],
    passwodPlain: ['', Validators.required, Validators.minLength(8), Validators.maxLength(64)],
    confirmPassword: ['', Validators.required],
    phoneNumber: ['', Validators.required]

  });

  onSubmit() {
    return ;
  }

}
