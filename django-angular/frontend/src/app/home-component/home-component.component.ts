import { Component, OnInit, inject } from '@angular/core';
import { CommonModule  } from '@angular/common';
import { LoginResponse, OidcSecurityService } from 'angular-auth-oidc-client';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
    selector: 'app-home',
    imports: [CommonModule],
    templateUrl: './home-component.component.html',
    styleUrl: './home-component.component.scss'
})
export class HomeComponent implements OnInit {
  private readonly oidcSecurityService = inject(OidcSecurityService);
  private http = inject(HttpClient);

  configuration$ = this.oidcSecurityService.getConfiguration();

  userData$ = this.oidcSecurityService.userData$;
  isAuthenticated = false;

  ngOnInit(): void {
    // this.oidcSecurityService.isAuthenticated$.subscribe(
    //   ({ isAuthenticated }) => {
    //     this.isAuthenticated = isAuthenticated;

    //     console.warn('authenticated: ', isAuthenticated);
    //   }
    // );

    this.oidcSecurityService
      .checkAuth()
      .subscribe((loginResponse: LoginResponse) => {
        console.log(loginResponse);
        const { isAuthenticated, userData, accessToken, idToken, configId } =
          loginResponse;

        /*...*/
      });
  }

  login(): void {
    this.oidcSecurityService.authorize();
  }

  refreshSession(): void {
    this.oidcSecurityService
      .forceRefreshSession()
      .subscribe((result) => console.log(result));
  }

  logout(): void {
    this.oidcSecurityService
      .logoff()
      .subscribe((result) => console.log(result));
  }

  logoffAndRevokeTokens(): void {
    this.oidcSecurityService
      .logoffAndRevokeTokens()
      .subscribe((result) => console.log(result));
  }

  revokeRefreshToken(): void {
    this.oidcSecurityService
      .revokeRefreshToken()
      .subscribe((result) => console.log(result));
  }

  revokeAccessToken(): void {
    this.oidcSecurityService
      .revokeAccessToken()
      .subscribe((result) => console.log(result));
  }

  test_api(): void {
    // const headers = { 'Authorization': `Bearer abc` };
    this.http.get('/sample/my-api/').subscribe(
      (data: any) => console.log(data),
      (error: any) => console.error(error)
    );
  }

  // test_api(): void {
  //   this.oidcSecurityService.getAccessToken().subscribe((token) => {
  //     if (token) {
  //       const headers = { 'Authorization': `Bearer ${token}` };
  //       this.http.get('https://192.168.1.18:4200/sample/my-api/', { headers }).subscribe(
  //         (data: any) => console.log(data),
  //         (error: any) => console.error(error)
  //       );
  //     } else {
  //       console.error('No access token available');
  //     }
  //   });
  // }
}