import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Datapoint } from './datapoint.interface';
import { PdfViewerModule } from 'ng2-pdf-viewer';
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatDividerModule } from '@angular/material/divider';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-pdf-data-viewer',
  templateUrl: './pdf-data-viewer.component.html',
  styleUrls: ['./pdf-data-viewer.component.scss'],
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    PdfViewerModule,
    MatCardModule,
    MatInputModule,
    MatButtonModule,
    MatTooltipModule,
    MatDividerModule,
    MatListModule,
    MatIconModule,
    MatFormFieldModule
  ]
})
export class PdfDataViewerComponent {
  pdfSrc = '21583473018.pdf';
  dataPoints: Datapoint[] = [
    { key: 'Name', value: 'John Doe', initial_value: 'Jane Doe', page: 1 },
    { key: 'Address', value: '123 Main St', initial_value: '456 Elm St', page: 2 },
    { key: 'Phone', value: '555-1234', initial_value: '555-5678', page: 3 }
  ];

  validateValue(datapoint: Datapoint) {
    // TODO: Implement validation logic
  }

  deleteValue(datapoint: Datapoint) {
    // TODO: Implement delete logic
  }

  goToPage(page: number) {
    // TODO: Implement page navigation
  }

  validateInput(datapoint: Datapoint) {
    // TODO: Implement input validation
  }
}
