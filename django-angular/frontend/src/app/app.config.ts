import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { authInterceptor, LogLevel, provideAuth } from 'angular-auth-oidc-client';


export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),

    provideAuth({
      config: {
        authority: 'https://192.168.1.27:9090/realms/master/',
        authWellknownEndpointUrl: 'https://192.168.1.27:9090/realms/master/',
        redirectUrl: window.location.origin,
        postLogoutRedirectUri: window.location.origin,
        clientId: 'test_clientid',
        scope: 'openid profile email',
        responseType: 'code',
        silentRenew: true,
        useRefreshToken: true,
        logLevel: LogLevel.Debug,
        triggerAuthorizationResultEvent: true,
        postLoginRoute: '/home',
        forbiddenRoute: '/forbidden',
        unauthorizedRoute: '/unauthorized',
        historyCleanupOff: true,
      },
    }),
    provideHttpClient(withInterceptors([authInterceptor()])),
  ] 
};
