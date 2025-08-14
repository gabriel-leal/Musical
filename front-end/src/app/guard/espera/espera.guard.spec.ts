import { TestBed } from '@angular/core/testing';
import { CanActivateFn } from '@angular/router';

import { esperaGuard } from './espera.guard';

describe('esperaGuard', () => {
  const executeGuard: CanActivateFn = (...guardParameters) => 
      TestBed.runInInjectionContext(() => esperaGuard(...guardParameters));

  beforeEach(() => {
    TestBed.configureTestingModule({});
  });

  it('should be created', () => {
    expect(executeGuard).toBeTruthy();
  });
});
