import { TestBed } from '@angular/core/testing';
import { CanActivateFn } from '@angular/router';

import { dependenteGuard } from './dependente.guard';

describe('dependenteGuard', () => {
  const executeGuard: CanActivateFn = (...guardParameters) => 
      TestBed.runInInjectionContext(() => dependenteGuard(...guardParameters));

  beforeEach(() => {
    TestBed.configureTestingModule({});
  });

  it('should be created', () => {
    expect(executeGuard).toBeTruthy();
  });
});
