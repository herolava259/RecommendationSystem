import { InjectionToken } from "@angular/core";


export const API_BASE_URL = new InjectionToken<string>("API_BASE_URL");

export const API_RESILIENCY_CONFIG = new InjectionToken<{ maxRetryAttempts: number, timeoutSeconds: number }>("API_RESILIENCY_CONFIG");
