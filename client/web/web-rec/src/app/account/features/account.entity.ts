import { createEntityAdapter, EntityAdapter, EntityState } from "@ngrx/entity";
import { Account } from "./account.model";


export interface AccountState extends EntityState<Account> {
  selectedAccountId: string | null;
}


export const accountAdapter: EntityAdapter<Account> = createEntityAdapter<Account>();

export const initialAccountState: AccountState = accountAdapter.getInitialState({
  selectedAccountId: null,
});
