import { TestBed } from '@angular/core/testing';

import { InscritoService } from './inscrito.service';

describe('InscritoService', () => {
  let service: InscritoService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(InscritoService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
