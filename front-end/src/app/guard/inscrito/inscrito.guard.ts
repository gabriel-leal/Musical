import { CanActivateFn, Router } from '@angular/router';
import { inject } from '@angular/core';
import { LOCAL_STORAGE_KEYS } from '../../app.config';

export const inscritoGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);
  const id = localStorage.getItem(LOCAL_STORAGE_KEYS.ID)
  if (id === null) {
    router.navigate(['/']);
    return false;
  } else {
    return true;
  }
};
