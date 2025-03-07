import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { authInterceptor, LogLevel, provideAuth, OpenIdConfiguration  } from 'angular-auth-oidc-client';
import { loggingInterceptor } from '../logging-interceptor';
import { customAuthInterceptor } from '../auth-interceptor';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { MY_DATE_FORMATS } from './test-angular/date-format';
import { MAT_DATE_FORMATS } from '@angular/material/core';


export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    // provideHttpClient(withInterceptors([loggingInterceptor, authInterceptor()])),
    provideHttpClient(withInterceptors([authInterceptor()])),
    provideAuth({
      config: {
        authority: 'http://pi5:8080/realms/master',
        authWellknownEndpointUrl: 'http://pi5:8080/realms/master/.well-known/openid-configuration',
        redirectUrl: 'https://localhost:4200/home',
        postLogoutRedirectUri: 'https://localhost:4200/logout',
        clientId: 'test-iodc',
        scope: 'openid',
        responseType: 'code',
        silentRenew: true,
        useRefreshToken: true,
        logLevel: LogLevel.Error,
        triggerAuthorizationResultEvent: true,
        postLoginRoute: 'https://localhost:4200/home',
        forbiddenRoute: 'https://localhost:4200/forbidden',
        unauthorizedRoute: 'https://localhost:4200/unauthorized',
        historyCleanupOff: true,
        secureRoutes: ['/']
      },
    }), provideAnimationsAsync(), provideAnimationsAsync(),
    { provide: MAT_DATE_FORMATS, useValue: MY_DATE_FORMATS },
  ] 
};
