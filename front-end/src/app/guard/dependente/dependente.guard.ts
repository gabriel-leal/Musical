import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { LOCAL_STORAGE_KEYS } from '../../app.config';

export const dependenteGuard: CanActivateFn = (route, state) => {
    const router = inject(Router);
    const nome = localStorage.getItem(LOCAL_STORAGE_KEYS.NOME)
    if (nome === null) {
      router.navigate(['/inscrito']);
      return false;
    } else {
      return true;
    }
};
