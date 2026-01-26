import { createActionGroup, emptyProps, props } from '@ngrx/store';
import { Update } from '@ngrx/entity';

import { Account } from './account.model';

export const AccountActions = createActionGroup({
  source: 'Account/API',
  events: {
    loadAccounts: props<{ accounts: Account[] }>(),
    addAccount: props<{ account: Account }>(),
    upsertAccount: props<{ account: Account }>(),
    addAccounts: props<{ accounts: Account[] }>(),
    upsertAccounts: props<{ accounts: Account[] }>(),
    updateAccount: props<{ account: Update<Account> }>(),
    updateAccounts: props<{ accounts: Update<Account>[] }>(),
    deleteAccount: props<{ id: string }>(),
    deleteAccounts: props<{ ids: string[] }>(),
    clearAccounts: emptyProps(),
  }
});

