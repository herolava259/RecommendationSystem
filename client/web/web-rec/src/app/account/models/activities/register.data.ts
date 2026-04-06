import {FormControl} from '@angular/forms';

export interface CreateAccountFormContent {
    email: FormControl<string>;
    phone: FormControl<string>;
    password: FormControl<string>;
    confirmPassword: FormControl<string>;
};

// Step 1: Create Account Request and Response
export interface CreateAccountInformationRequest {
    email: string;
    phone: string;
    signinName: string;
    password: string;
}

export function createAccountInformationRequestFromFormContent(formContent: CreateAccountFormContent): CreateAccountInformationRequest
{
  return {
    email: formContent.email.value,
    phone: formContent.phone.value,
    signinName: formContent.email.value, // Assuming signinName is the same as email
    password: formContent.password.value
  }
}

export interface CreateAccountResponse  {
    succeed: boolean;
    responseMessage: string;
    navigationHome: boolean;
    needVerifyEmail: boolean;
    additionalInfo?: string;
}

// Step 2: Verify Email Request and Response
export interface VerifyEmailRequest {
  activationKey: string;
  email: string;
  signin_name: string;
  personal_key: string;
}

export interface EmailVerificationResponse {
  succeed: boolean;
  responseMessage: string;
  navigationHome: boolean;
}


// Step 3: Submit Private Information Request and Response
export interface SubmitPrivateInformationRequest {
  accountId: string;
  phone: string;
  special_name: string;
  address: string;
  postCode: string;
  userName: string;
  preference: string;
  secretQas: Record<string, string>;
}

export interface SubmitPrivateInformationResponse {
  succeed: boolean;
  responseMessage: string;
}


export interface LoginRequest {
    email: string | null;
    signinName: string | null;
    password: string | null;
    checkSum: string | null;
}


export interface AccessTokenResponse{
    accessToken: string;
    refreshToken: string;
    userData: Record<string, string>;
    tokenType: string;
    algType: string;
    claim: Record<string, string>;
    signature: string;
}

export interface LoginResponse {
    succeed: boolean;
    responseMessage: string;
    accessTokenResponse?: AccessTokenResponse;
}

