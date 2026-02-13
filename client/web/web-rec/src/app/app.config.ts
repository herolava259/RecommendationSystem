import { ApplicationConfig, importProvidersFrom, provideZoneChangeDetection, isDevMode } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { provideClientHydration, withEventReplay } from '@angular/platform-browser';

import { globalHotToastConfig } from './configurations/hot-toast.config';
import {provideDialogConfig} from "@ngneat/dialog"
import { dialogConfig } from './configurations/dialog.config';
import { provideHotToastConfig} from '@ngxpert/hot-toast';

import { LucideAngularModule } from 'lucide-angular';
import { lucideIcons } from './configurations/lucide.config';
import { provideStore } from '@ngrx/store';
import { provideStoreDevtools } from '@ngrx/store-devtools';
import { provideEffects } from '@ngrx/effects';
import { provideRouterStore } from '@ngrx/router-store';
import { provideHttpClient } from '@angular/common/http';
import { API_BASE_URL, API_RESILIENCY_CONFIG } from './app.di.tokens';
import { environment } from '../environments/environment';

const diTokens = [
  {
    provide: API_BASE_URL,
    useValue: environment.api.base
  },
  {
    provide: API_RESILIENCY_CONFIG,
    useValue: environment.api.resilency
  }
];

export const appConfig: ApplicationConfig = {
  providers: [
    ...diTokens,
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    provideClientHydration(withEventReplay()),
    provideHttpClient(),
    provideDialogConfig(dialogConfig),
    provideHotToastConfig(globalHotToastConfig),
    importProvidersFrom(LucideAngularModule.pick(lucideIcons)),
    provideStore(),
    provideStoreDevtools({ maxAge: 25, logOnly: !isDevMode() }),
    provideEffects(),
    provideRouterStore()
  ]
};
