// espera-access.service.ts
import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class EsperaAccessService {
  private allowAccess = false;

  permitAccess() {
    this.allowAccess = true;
  }

  canAccess(): boolean {
    if (this.allowAccess) {
      this.allowAccess = false; 
      return true;
    }
    return false;
  }
}
