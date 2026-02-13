
export interface Account {
  id: string;
  email?: string | null;
  loginName: string;
  imageUrl?: string | null;
  active: boolean;
  passwordPlain: string;
  createdAt: Date;
  updatedAt: Date;
}
