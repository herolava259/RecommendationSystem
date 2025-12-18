export interface EmailVerificationModel {
    id: string;
    accountId: string;
    activationKey: number;

    expireDate?: Date;

    is_verified: boolean;

}