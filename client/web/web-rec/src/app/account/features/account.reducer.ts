import { createFeature, createReducer, on } from '@ngrx/store';
import { AccountActions }  from './account.actions';
import { accountAdapter, initialAccountState } from './account.entity';

export const accountsFeatureKey = 'accounts';

export const reducer = createReducer(
  initialAccountState,
  on(AccountActions.addAccount,
    (state, action) => accountAdapter.addOne(action.account, state)
  ),
  on(AccountActions.upsertAccount,
    (state, action) => accountAdapter.upsertOne(action.account, state)
  ),
  on(AccountActions.addAccounts,
    (state, action) => accountAdapter.addMany(action.accounts, state)
  ),
  on(AccountActions.upsertAccounts,
    (state, action) => accountAdapter.upsertMany(action.accounts, state)
  ),
  on(AccountActions.updateAccount,
    (state, action) => accountAdapter.updateOne(action.account, state)
  ),
  on(AccountActions.updateAccounts,
    (state, action) => accountAdapter.updateMany(action.accounts, state)
  ),
  on(AccountActions.deleteAccount,
    (state, action) => accountAdapter.removeOne(action.id, state)
  ),
  on(AccountActions.deleteAccounts,
    (state, action) => accountAdapter.removeMany(action.ids, state)
  ),
  on(AccountActions.loadAccounts,
    (state, action) => accountAdapter.setAll(action.accounts, state)
  ),
  on(AccountActions.clearAccounts,
    state => accountAdapter.removeAll(state)
  ),
);

export const accountsFeature = createFeature({
  name: accountsFeatureKey,
  reducer,
  extraSelectors: ({ selectAccountsState }) => ({
    ...accountAdapter.getSelectors(selectAccountsState)
  }),
});

export const {
  selectIds,
  selectEntities,
  selectAll,
  selectTotal,
} = accountsFeature;
