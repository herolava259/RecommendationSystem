import { TestBed } from '@angular/core/testing';

import { SignupManagerService } from './signup-manager.service';

describe('SignupManagerService', () => {
  let service: SignupManagerService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SignupManagerService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
