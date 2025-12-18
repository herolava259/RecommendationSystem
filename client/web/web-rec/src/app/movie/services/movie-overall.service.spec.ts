import { TestBed } from '@angular/core/testing';

import { MovieOverallService } from './movie-overall.service';

describe('MovieOverallService', () => {
  let service: MovieOverallService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(MovieOverallService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
