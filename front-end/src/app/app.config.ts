import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { provideClientHydration } from '@angular/platform-browser';
import { provideEnvironmentNgxMask } from 'ngx-mask';
import { provideHttpClient, withFetch } from '@angular/common/http';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';

export const appConfig: ApplicationConfig = {
  providers: [provideZoneChangeDetection({ eventCoalescing: true }), provideRouter(routes), provideEnvironmentNgxMask(), provideHttpClient(withFetch()), provideAnimationsAsync()]
};

export const LOCAL_STORAGE_KEYS = {
  ADM: 's6S4hQ47WF',
  // ROLES: '3ENnp9bVsb',
  // NAME: 'FbhpLb7HZJ',
  // EMAIL: 'FbdpLb9xZJ',
  ID: '0vK22KkTqI',
  NOME: 'g8T7jR29XG'
};
