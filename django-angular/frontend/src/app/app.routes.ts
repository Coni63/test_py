import { Routes } from '@angular/router';
import { HomeComponent } from './home-component/home-component.component';
import { UnauthorizedComponent } from './unauthorized-component/unauthorized-component.component';
import { AuthorizedComponent } from './authorized-component/authorized-component.component';
import { LayoutComponent } from './layout/layout.component';
// import { TestTableComponent } from './test-table/test-table.component';
import { TestAngularComponent } from './test-angular/test-angular.component';
import { PdfDataViewerComponent } from './pdf-data-viewer/pdf-data-viewer.component';
import { DatapointComponent } from './datapoint/datapoint.component';

export const routes: Routes = [
    // { path: '', redirectTo: 'home', pathMatch: 'full' },
    // { path: 'home', component: HomeComponent },
    // { path: 'logout', component: HomeComponent },
    // { path: 'unauthorized', component: UnauthorizedComponent },
    // { path: 'forbidden', component: UnauthorizedComponent },
    // { path: 'authorized', component: AuthorizedComponent },
    // { path: 'test', component: LayoutComponent },
    // { path: 'table', component: TestTableComponent },
    { path: '', component: AuthorizedComponent },
    { path: 'pdf-viewer', component: PdfDataViewerComponent }
];
