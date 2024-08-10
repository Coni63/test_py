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
        authority: 'https://192.168.1.27:9090/realms/master',
        authWellknownEndpointUrl: 'https://192.168.1.27:9090/realms/master/.well-known/openid-configuration',
        redirectUrl: 'https://192.168.1.18:4200/home',
        postLogoutRedirectUri: 'https://192.168.1.18:4200/logout',
        clientId: 'test_clientid',
        scope: 'openid profile email',
        responseType: 'code',
        silentRenew: true,
        useRefreshToken: true,
        logLevel: LogLevel.Debug,
        triggerAuthorizationResultEvent: true,
        postLoginRoute: 'https://192.168.1.18:4200/home',
        forbiddenRoute: 'https://192.168.1.18:4200/forbidden',
        unauthorizedRoute: 'https://192.168.1.18:4200/unauthorized',
        historyCleanupOff: true,
      },
    }),
    provideHttpClient(withInterceptors([authInterceptor()])),
  ] 
};
