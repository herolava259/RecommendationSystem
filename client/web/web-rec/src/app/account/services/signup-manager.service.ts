import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { CreateAccountFormContent, createAccountInformationRequestFromFormContent } from '../models/activities/register.data';
import { take } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SignupManagerService {

  private readonly httpClient = inject(HttpClient);

  // eslint-disable-next-line @typescript-eslint/no-empty-function, @typescript-eslint/no-unused-vars
  public submitAccountInformation(formContent: CreateAccountFormContent) {
    return this.httpClient.post('/api/account/create/accountinformation',
      createAccountInformationRequestFromFormContent(formContent))
      .pipe(take(1));
  }
}
