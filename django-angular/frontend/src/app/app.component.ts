import { Component, inject, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { OidcSecurityService } from 'angular-auth-oidc-client';


@Component({
    selector: 'app-root',
    imports: [
        RouterOutlet,
    ],
    templateUrl: './app.component.html',
    styleUrl: './app.component.scss',
    standalone: true,
})
export class AppComponent implements OnInit {
  private readonly oidcSecurityService = inject(OidcSecurityService);

  ngOnInit(): void {
    // this.oidcSecurityService
    //   .checkAuth()
    //   .subscribe(({ isAuthenticated, accessToken }) => {
        // console.log('app authenticated', isAuthenticated);
        // console.log(`Current access token is '${accessToken}'`);
      // });
  }
}