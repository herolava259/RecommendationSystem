import { TestBed } from '@angular/core/testing';

import { AccountSsoService } from './account.sso.service';

describe('AccountSsoService', () => {
  let service: AccountSsoService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AccountSsoService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
