import { TestBed } from '@angular/core/testing';

import { EmissionApi } from './emission.api';

describe('EmissionApi', () => {
  let service: EmissionApi;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(EmissionApi);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
