import { Injectable } from '@angular/core';
import { HttpInterceptorFn, HttpHandlerFn, HttpRequest, HttpEvent } from '@angular/common/http';
import { Observable, tap } from 'rxjs';

export const loggingInterceptor: HttpInterceptorFn = (
  req: HttpRequest<unknown>,
  next: HttpHandlerFn
): Observable<HttpEvent<unknown>> => {
  console.log('Request URL:', req.url);
  console.log('Request method:', req.method);
  console.log('Request headers before authInterceptor:', req.headers.keys());

  return next(req).pipe(
    tap({
      next: (event) => {
        if (event.type === 0) {
          console.log('Request headers after authInterceptor:', req.headers.keys());
        }
      }
    })
  );
};