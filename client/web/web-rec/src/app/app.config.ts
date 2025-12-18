import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { provideClientHydration, withEventReplay } from '@angular/platform-browser';

import {provideHotToastConfig} from '@ngneat/hot-toast';
import { hotToastConfig } from './configs/hot-toast.config';
import {provideDialogConfig, DialogConfig} from "@ngneat/dialog"
import { dialogConfig } from './configs/dialog.config';


export const appConfig: ApplicationConfig = {
  providers: [provideZoneChangeDetection({ eventCoalescing: true }), 
              provideRouter(routes), provideClientHydration(withEventReplay()),
              provideHotToastConfig(hotToastConfig),
              provideDialogConfig(dialogConfig)]
};
