import { Component, inject, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { OidcSecurityService } from 'angular-auth-oidc-client';
import { Datapoint } from './datapoint';
import { DatapointComponent } from "./datapoint/datapoint.component";
import { CommonModule } from '@angular/common';
import { ResizeDirective } from './resize.directive';
import {CdkTree, CdkTreeModule} from '@angular/cdk/tree';
import {MatTreeModule} from '@angular/material/tree';
import { MatIcon, MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatTableDataSource } from '@angular/material/table';
import {MatTableModule} from '@angular/material/table';
import {MatDividerModule} from '@angular/material/divider';
import { UserAvatarComponent } from './user-avatar/user-avatar.component';
interface INode {
  name: string;
  expanded: boolean;
  objects?: Datapoint[];
}

@Component({
    selector: 'app-root',
    imports: [
    RouterOutlet,
    DatapointComponent,
    CommonModule,
    ResizeDirective,
    CdkTreeModule,
    MatTreeModule,
    MatIconModule,
    MatButtonModule,
    MatTableModule,
    MatDividerModule,
    UserAvatarComponent
],
    templateUrl: './app.component.html',
    styleUrl: './app.component.scss',
    standalone: true,
})
export class AppComponent implements OnInit {
  // private readonly oidcSecurityService = inject(OidcSecurityService);

  // datapoints: Datapoint[] = [
  //   {
  //     id: '',
  //     name: 'Fruit',
  //     initialValue: '',
  //     validatedValue: null,
  //     key: 'test key',
  //     isValidated: false,
  //     page: 4,
  //     children: [
        // {
        //   id: '296fa464-9dea-482a-80f0-af7533649940',
        //   initialValue: '42',
        //   validatedValue: null,
        //   key: 'test key',
        //   isValidated: false,
        //   page: 4,
        //   name: null,
        //   children: []
        // },
        // {
        //   id: '296fa464-9dea-482a-80f0-af7533649941',
        //   initialValue: 'asdfadsfasdfasdfasdf',
        //   validatedValue: null,
        //   key: 'test key 2',
        //   isValidated: true,
        //   page: 4,
        //   name: null,
        //   children: []
        // },
        // {
        //   id: '296fa464-9dea-482a-80f0-af7533649941',
        //   initialValue: 'asdfadsfasdfasdfasdf',
        //   validatedValue: null,
        //   key: 'test key 2',
        //   isValidated: true,
        //   page: 4,
        //   name: null,
        //   children: []
        // },
        // {
        //   id: '296fa464-9dea-482a-80f0-af7533649941',
        //   initialValue: 'asdfadsfasdfasdfasdf',
        //   validatedValue: null,
        //   key: 'test key 2',
        //   isValidated: false,
        //   page: 4,
        //   name: null,
        //   children: []
        // },
        // {
        //   id: '296fa464-9dea-482a-80f0-af7533649941',
        //   initialValue: 'asdfadsfasdfasdfasdf',
        //   validatedValue: null,
        //   key: 'test key 2',
        //   isValidated: true,
        //   page: 4,
        //   name: null,
        //   children: []
        // },
        // {
        //   id: '296fa464-9dea-482a-80f0-af7533649941',
        //   initialValue: 'asdfadsfasdfasdfasdf',
        //   validatedValue: null,
        //   key: 'test key 2',
        //   isValidated: false,
        //   page: 4,
        //   name: null,
        //   children: []
        // }
  //     ],
  //   },
  //   {
  //     id: '',
  //     name: 'Vegetables',
  //     initialValue: '',
  //     validatedValue: null,
  //     key: 'test key',
  //     isValidated: false,
  //     page: 4,
  //     children: [
  //       {
  //         id: '296fa464-9dea-482a-80f0-af7533649940',
  //         initialValue: '42',
  //         validatedValue: null,
  //         key: 'test key',
  //         isValidated: false,
  //         page: 4,
  //         name: null,
  //         children: []
  //       },
  //       {
  //         id: '296fa464-9dea-482a-80f0-af7533649941',
  //         initialValue: 'asdfadsfasdfasdfasdf',
  //         validatedValue: null,
  //         key: 'test key 2',
  //         isValidated: true,
  //         page: 4,
  //         name: null,
  //         children: []
  //       },
  //       {
  //         id: '296fa464-9dea-482a-80f0-af7533649941',
  //         initialValue: 'asdfadsfasdfasdfasdf',
  //         validatedValue: null,
  //         key: 'test key 2',
  //         isValidated: true,
  //         page: 4,
  //         name: null,
  //         children: []
  //       },
  //       {
  //         id: '296fa464-9dea-482a-80f0-af7533649941',
  //         initialValue: 'asdfadsfasdfasdfasdf',
  //         validatedValue: null,
  //         key: 'test key 2',
  //         isValidated: false,
  //         page: 4,
  //         name: null,
  //         children: []
  //       },
  //       {
  //         id: '296fa464-9dea-482a-80f0-af7533649941',
  //         initialValue: 'asdfadsfasdfasdfasdf',
  //         validatedValue: null,
  //         key: 'test key 2',
  //         isValidated: true,
  //         page: 4,
  //         name: null,
  //         children: []
  //       },
  //       {
  //         id: '296fa464-9dea-482a-80f0-af7533649941',
  //         initialValue: 'asdfadsfasdfasdfasdf',
  //         validatedValue: null,
  //         key: 'test key 2',
  //         isValidated: false,
  //         page: 4,
  //         name: null,
  //         children: []
  //       }
  //     ],
  //   },
  // ];
  // displayedColumns: string[] = ['group'];
  groups2: INode[] = [];
  groups: INode[] = [
    { name: 'Group A', expanded: true, objects: [      {
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
      isValidated: true,
      page: 4
    },
    {
      id: '296fa464-9dea-482a-80f0-af7533649941',
      initialValue: 'asdfadsfasdfasdfasdf',
      validatedValue: null,
      key: 'test key 2',
      isValidated: true,
      page: 4
    },
    {
      id: '296fa464-9dea-482a-80f0-af7533649941',
      initialValue: 'asdfadsfasdfasdfasdf',
      validatedValue: null,
      key: 'test key 2',
      isValidated: false,
      page: 4
    },
    {
      id: '296fa464-9dea-482a-80f0-af7533649941',
      initialValue: 'asdfadsfasdfasdfasdf',
      validatedValue: null,
      key: 'test key 2',
      isValidated: true,
      page: 4
    },
    {
      id: '296fa464-9dea-482a-80f0-af7533649941',
      initialValue: 'asdfadsfasdfasdfasdf',
      validatedValue: null,
      key: 'test key 2',
      isValidated: false,
      page: 4
    }] },
    { name: 'Group B', expanded: false, objects: [      {
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
      isValidated: true,
      page: 4
    },
    {
      id: '296fa464-9dea-482a-80f0-af7533649941',
      initialValue: 'asdfadsfasdfasdfasdf',
      validatedValue: null,
      key: 'test key 2',
      isValidated: true,
      page: 4
    },
    {
      id: '296fa464-9dea-482a-80f0-af7533649941',
      initialValue: 'asdfadsfasdfasdfasdf',
      validatedValue: null,
      key: 'test key 2',
      isValidated: false,
      page: 4
    },
    {
      id: '296fa464-9dea-482a-80f0-af7533649941',
      initialValue: 'asdfadsfasdfasdfasdf',
      validatedValue: null,
      key: 'test key 2',
      isValidated: true,
      page: 4
    },
    {
      id: '296fa464-9dea-482a-80f0-af7533649941',
      initialValue: 'asdfadsfasdfasdfasdf',
      validatedValue: null,
      key: 'test key 2',
      isValidated: false,
      page: 4
    }] },
  ];

  dataSource = new MatTableDataSource(this.groups);
  expandedGroup: INode | null = null;

  // toggleGroup(group: INode) {
  //   this.expandedGroup = this.expandedGroup === group ? null : group;
  //   console.log(this.expandedGroup);
  // }

  isExpanded = (index: number, row: INode) => {
    console.log(index, row.name, this.expandedGroup?.name);
    return row === this.expandedGroup;
  }

  ngOnInit(): void {
    // this.oidcSecurityService
    //   .checkAuth()
    //   .subscribe(({ isAuthenticated, accessToken }) => {
    //     console.log('app authenticated', isAuthenticated);
    //     console.log(`Current access token is '${accessToken}'`);
    //   });
  }

  validateDatapoint(datapoint: Datapoint) {
    // let item = this.datapoints.find(x => x.id == datapoint.id);
    // if (item && !item.isValidated ) {
    //   item.isValidated = true;
    // }
    // console.log("validateDatapoint ", datapoint);
  }

  revertDatapoint(datapoint: Datapoint) {
    // let item = this.datapoints.find(x => x.id == datapoint.id);
    // if (item && item.isValidated ) {
    //   item.isValidated = false;
    // }
    // console.log("revertDatapoint ", datapoint);
  }

  deleteDatapoint(datapoint: Datapoint) {
    // this.datapoints = this.datapoints.filter(x => x.id != datapoint.id);
  }

  searchDatapoint(datapoint: Datapoint) {
    console.log("search ", datapoint);
  }


  toggleGroup(group: INode) {
    group.expanded = !group.expanded;
  }
}