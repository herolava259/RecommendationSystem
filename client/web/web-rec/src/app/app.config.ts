import { ApplicationConfig, importProvidersFrom, provideZoneChangeDetection, isDevMode } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { provideClientHydration, withEventReplay } from '@angular/platform-browser';

import { globalHotToastConfig } from './configs/hot-toast.config';
import {provideDialogConfig, DialogConfig} from "@ngneat/dialog"
import { dialogConfig } from './configs/dialog.config';
import { provideHotToastConfig} from '@ngxpert/hot-toast';

import { LucideAngularModule } from 'lucide-angular';
import { lucideIcons } from './configs/lucide.config';
import { provideStore } from '@ngrx/store';
import { provideStoreDevtools } from '@ngrx/store-devtools';
import { provideEffects } from '@ngrx/effects';
import { provideRouterStore } from '@ngrx/router-store';
import { provideHttpClient } from '@angular/common/http';

export const appConfig: ApplicationConfig = {
  providers: [
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
    provideRouterStore()]
};
