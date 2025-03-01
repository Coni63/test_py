import { Component, inject, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { OidcSecurityService } from 'angular-auth-oidc-client';
import { Datapoint } from './datapoint';
import { DatapointComponent } from "./datapoint/datapoint.component";
import { CommonModule } from '@angular/common';


@Component({
    selector: 'app-root',
    imports: [
    RouterOutlet,
    DatapointComponent,
    CommonModule,
],
    templateUrl: './app.component.html',
    styleUrl: './app.component.scss',
    standalone: true,
})
export class AppComponent implements OnInit {
  // private readonly oidcSecurityService = inject(OidcSecurityService);

  datapoints: Datapoint[] = [
    {
      id: '296fa464-9dea-482a-80f0-af7533649940',
      initialValue: '42',
      validatedValue: null,
      key: 'test key',
      isValidated: false,
      page: 4
    },
    {
      id: '296fa464-9dea-482a-80f0-af7533649941',
      initialValue: 'asdfadsfasdfasdfasdf',
      validatedValue: null,
      key: 'test key 2',
      isValidated: false,
      page: 4
    }
  ];

  ngOnInit(): void {
    console.log('Datapoints:', this.datapoints);
    // this.oidcSecurityService
    //   .checkAuth()
    //   .subscribe(({ isAuthenticated, accessToken }) => {
        // console.log('app authenticated', isAuthenticated);
        // console.log(`Current access token is '${accessToken}'`);
      // });
  }

  validateDatapoint(datapoint: Datapoint) {
    let item = this.datapoints.find(x => x.id == datapoint.id);
    if (item && !item.isValidated ) {
      item.isValidated = true;
    }
    console.log("validateDatapoint ", datapoint);
  }

  revertDatapoint(datapoint: Datapoint) {
    let item = this.datapoints.find(x => x.id == datapoint.id);
    if (item && item.isValidated ) {
      item.isValidated = false;
    }
    console.log("revertDatapoint ", datapoint);
  }

  deleteDatapoint(datapoint: Datapoint) {
    this.datapoints = this.datapoints.filter(x => x.id != datapoint.id);
  }

  searchDatapoint(datapoint: Datapoint) {
    console.log("search ", datapoint);
  }

}