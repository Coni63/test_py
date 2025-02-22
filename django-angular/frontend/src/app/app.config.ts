import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { authInterceptor, LogLevel, provideAuth } from 'angular-auth-oidc-client';
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
        authority: 'https://192.168.1.27:9090/realms/master',
        authWellknownEndpointUrl: 'https://192.168.1.27:9090/realms/master/.well-known/openid-configuration',
        redirectUrl: 'https://192.168.1.18:4200/home',
        postLogoutRedirectUri: 'https://192.168.1.18:4200/logout',
        clientId: 'test_clientid',
        scope: 'openid profile email',
        responseType: 'code',
        silentRenew: true,
        useRefreshToken: true,
        logLevel: LogLevel.Error,
        triggerAuthorizationResultEvent: true,
        postLoginRoute: 'https://192.168.1.18:4200/home',
        forbiddenRoute: 'https://192.168.1.18:4200/forbidden',
        unauthorizedRoute: 'https://192.168.1.18:4200/unauthorized',
        historyCleanupOff: true,
        secureRoutes: ['/'],
      },
    }), provideAnimationsAsync(), provideAnimationsAsync(),
    { provide: MAT_DATE_FORMATS, useValue: MY_DATE_FORMATS },
  ] 
};
