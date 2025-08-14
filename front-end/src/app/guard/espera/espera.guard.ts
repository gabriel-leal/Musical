// espera.guard.ts
import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { EsperaAccessService } from '../../services/espera/espera.service';

@Injectable({ providedIn: 'root' })
export class EsperaGuard implements CanActivate {
  constructor(private esperaAccess: EsperaAccessService, private router: Router) {}

  canActivate(): boolean {
    if (this.esperaAccess.canAccess()) {
      return true;
    }
    this.router.navigate(['/']);  // redireciona para home se não permitido
    return false;
  }
}
