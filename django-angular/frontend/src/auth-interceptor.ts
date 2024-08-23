import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { OidcSecurityService } from 'angular-auth-oidc-client';
import { switchMap } from 'rxjs/operators';

const SECURE_ROUTES = ['/sample/']; // Add your secure routes here

function isSecureRoute(url: string): boolean {
  return SECURE_ROUTES.some(route => url.startsWith(route));
}

export const customAuthInterceptor: HttpInterceptorFn = (req, next) => {
  const oidcSecurityService = inject(OidcSecurityService);

  console.log('CustomAuthInterceptor: Intercepting request to', req.url);

  if (!isSecureRoute(req.url)) {
    console.log('CustomAuthInterceptor: Not a secure route, proceeding without authentication');
    return next(req);
  }

  return oidcSecurityService.getAccessToken().pipe(
    switchMap(token => {
      if (token) {
        console.log('CustomAuthInterceptor: Token available, adding to headers');
        const authReq = req.clone({
          headers: req.headers.set('Authorization', `Bearer ${token}`)
        });
        return next(authReq);
      } else {
        console.log('CustomAuthInterceptor: No token available, proceeding without authentication');
        return next(req);
      }
    })
  );
};