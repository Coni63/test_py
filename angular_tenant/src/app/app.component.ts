import { Component, inject, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ApiService } from './api.service';
import { Observable, of } from 'rxjs';
import { CommonModule } from '@angular/common';
import { LoginResponse, OidcSecurityService } from 'angular-auth-oidc-client';

@Component({
  selector: 'app-root',
  imports: [CommonModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
  standalone: true,
})
export class AppComponent implements OnInit {
  private readonly apiService = inject(ApiService);
  private readonly oidcSecurityService = inject(OidcSecurityService);

  title = 'angular_tenant';
  
  people$: Observable<any>;
  auth$: Observable<LoginResponse | null>;

  constructor() {
    this.people$ = of({});
    this.auth$ = of(null);
  }

  ngOnInit() {
    this.auth$ = this.oidcSecurityService.checkAuth();
  }

  login() {
    this.oidcSecurityService.authorize();
  }

  logout() {
    this.oidcSecurityService
      .logoff()
      .subscribe((result) => console.log(result));
  }

  call_api() {
    this.people$ = this.apiService.getPeople();
  }
}
