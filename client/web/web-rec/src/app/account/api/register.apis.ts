import { Injectable } from "@angular/core";
import { IApiEndpointGroup } from "../../shared/api/api.intefaces";


@Injectable()
export class RegisterApis implements IApiEndpointGroup {
  name: string;

  /**
   *
   */
  constructor() {

    this.name = "Register APIs";

  }

  static readonly RegisterPath = { method: 'POST', path: '/api/account/signup' };

  static readonly VerifyEmailPath = { method: 'POST', path: '/api/account/verify-email' };

  static readonly SubmitPrivateInformation = { method: 'POST', path: '/api/account/submit-private-information' };

}
