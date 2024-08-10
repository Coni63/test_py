import { Routes } from '@angular/router';
import { HomeComponent } from './home-component/home-component.component';
import { UnauthorizedComponent } from './unauthorized-component/unauthorized-component.component';
import { AuthorizedComponent } from './authorized-component/authorized-component.component';

export const routes: Routes = [
    { path: '', redirectTo: 'home', pathMatch: 'full' },
    { path: 'home', component: HomeComponent },
    { path: 'logout', component: HomeComponent },
    { path: 'unauthorized', component: UnauthorizedComponent },
    { path: 'forbidden', component: UnauthorizedComponent },
    { path: 'authorized', component: AuthorizedComponent },
];
