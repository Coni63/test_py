import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient, withInterceptors } from '@angular/common/http'
import { provideAuth, LogLevel, authInterceptor } from 'angular-auth-oidc-client';

import { routes } from './app.routes';

// https://nice-hill-002425310.azurestaticapps.net/docs/samples/
// https://github.com/damienbod/angular-auth-oidc-client/blob/main/projects/sample-code-flow-auth0/src/app/auth-config.module.ts
export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }), 
    provideRouter(routes), 
    provideHttpClient(withInterceptors([authInterceptor()])),
    provideAuth({
      config: {
        authority: 'https://pi5.local/keycloak/realms/master',
        redirectUrl: window.location.origin,
        postLogoutRedirectUri: window.location.origin,
        clientId: 'test-iodc',
        scope: 'openid profile email offline_access',
        responseType: 'code',
        silentRenew: true,
        useRefreshToken: true,
        logLevel: LogLevel.Debug,
        customParamsAuthRequest: {
          audience: 'https://auth0-api-spa',
        },
        customParamsRefreshTokenRequest: {
          scope: 'openid profile offline_access auth0-user-api-spa',
        },
      },
    })
  ]
};
