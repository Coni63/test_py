import { Component, inject,  OnInit, ViewChild } from '@angular/core';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import {MatIconModule} from '@angular/material/icon';
import {MatDividerModule} from '@angular/material/divider';
import {MatButtonModule} from '@angular/material/button';
import { TestDataService } from './test-api.service';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { FormGroup, FormBuilder } from '@angular/forms';
import { debounceTime, distinctUntilChanged } from 'rxjs/operators';
import { MatFormField, MatLabel } from '@angular/material/form-field';
import { DatePipe, DecimalPipe } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { MatTableModule } from '@angular/material/table';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatSortModule } from '@angular/material/sort';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';


@Component({
    selector: 'app-test-angular',
    imports: [
        MatSlideToggleModule,
        MatButtonModule, 
        MatIconModule, 
        MatDividerModule,
        MatLabel,
        MatFormField,
        MatDatepickerModule,
        MatSelectModule,
        DatePipe,
        ReactiveFormsModule,
        MatTableModule,
        MatPaginatorModule,
        MatSortModule,
        MatFormFieldModule,
        MatInputModule,
        MatSelectModule,
        MatDatepickerModule,
        MatNativeDateModule,
        MatIconModule,
        ReactiveFormsModule,
        DecimalPipe
    ],
    templateUrl: './test-angular.component.html',
    styleUrl: './test-angular.component.scss',
    standalone: true,
})
export class TestAngularComponent {
    private readonly apiService = inject(TestDataService);

    displayedColumns: string[] = ['text', 'date', 'bool', 'number', 'float'];
    dataSource: MatTableDataSource<any> = new MatTableDataSource();
    totalRecords = 0;
    matchingRecords = 0;
    filterForm: FormGroup;
  
    @ViewChild(MatPaginator) paginator!: MatPaginator;
    @ViewChild(MatSort) sort!: MatSort;
  
    constructor(
      private testDataService: TestDataService,
      private fb: FormBuilder
    ) {
      this.filterForm = this.fb.group({
        text: [''],
        date_after: [''],
        date_before: [''],
        bool: [''],
        number_min: [''],
        number_max: [''],
        float_min: [''],
        float_max: ['']
      });
    }
  
    ngOnInit() {
      this.loadData();
      
      // Subscribe to filter changes
      this.filterForm.valueChanges
        .pipe(
          debounceTime(500),
          distinctUntilChanged()
        )
        .subscribe(() => {
          this.paginator.pageIndex = 0;
          this.loadData();
        });
    }
  
    loadData() {
      this.testDataService
        .getTestData(
          this.paginator?.pageIndex || 0,
          this.paginator?.pageSize || 20,
          this.sort?.active || 'date',
          this.sort?.direction || 'desc',
          this.filterForm.value
        )
        .subscribe((response) => {
          this.dataSource.data = response.results;
          this.totalRecords = response.total_records;
          this.matchingRecords = response.matching_records;
        });
    }
  
    onSortChange() {
      this.loadData();
    }
  
    onPageChange() {
      this.loadData();
    }
}
