/* eslint-disable @angular-eslint/prefer-inject */
/* eslint-disable @typescript-eslint/no-explicit-any */
import { Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { catchError, map, concatMap } from 'rxjs/operators';
import { EMPTY, of } from 'rxjs';
import {AccountActions}  from './account.actions';


@Injectable()
export class AccountEffects {

  loadAccounts$ = createEffect(() => {
    return this.actions$.pipe(

      ofType(AccountActions.loadAccounts),
      concatMap(() =>
        /** An EMPTY observable only emits completion. Replace with your own observable API request */
        EMPTY.pipe(
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          map(data => (AccountActions as any).loadAccountsSuccess({ data })),
          catchError(error => of((AccountActions as any).loadAccountsFailure({ error }))))
      )
    );
  });


  constructor(private actions$: Actions) {}
}
