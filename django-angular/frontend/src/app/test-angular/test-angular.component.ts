import { Component } from '@angular/core';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import {MatIconModule} from '@angular/material/icon';
import {MatDividerModule} from '@angular/material/divider';
import {MatButtonModule} from '@angular/material/button';


@Component({
    selector: 'app-test-angular',
    imports: [
        MatSlideToggleModule,
        MatButtonModule, MatIconModule, MatDividerModule

    ],
    templateUrl: './test-angular.component.html',
    styleUrl: './test-angular.component.scss',
    standalone: true,
})
export class TestAngularComponent {

}
