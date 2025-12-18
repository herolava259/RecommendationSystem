import {FormControl, FormRecord} from '@angular/forms';

export type CreateAccountFormContent = {
    email: FormControl<string>;
    phone: FormControl<string>;
    password: FormControl<string>;
    confirmPassword: FormControl<string>;
};


export interface CreateAccountRequest {
    email: string;
    phone: string;
    signinName: string;
    password: string;
}

export interface CreateAccountResponse  {
    succeed: boolean;
    responseMessage: string;
    navigationHome: boolean;
    needVerifyEmail: boolean;
    additionalInfo?: string;
}

export interface LoginRequest {
    email: string | null;
    signinName: string | null;
    password: string | null;
    checkSum: string | null;  
}


