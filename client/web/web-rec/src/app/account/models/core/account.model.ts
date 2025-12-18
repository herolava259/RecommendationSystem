

export interface AccountModel {
    id: string;
    email: string;
    phone: string;
    signinName: string;
    imageUrl?: string;

    active: boolean;

    personalIdentifier?: string;
    createdAt: Date;
    updatedAt: Date;

    emailVerified: boolean;
}


