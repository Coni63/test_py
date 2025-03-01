import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatDividerModule } from '@angular/material/divider';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatListModule } from '@angular/material/list';
import { MatTooltipModule } from '@angular/material/tooltip';
import { Datapoint } from '../datapoint';


@Component({
  selector: 'app-datapoint',
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    MatInputModule,
    MatButtonModule,
    MatTooltipModule,
    MatDividerModule,
    MatListModule,
    MatIconModule,
    MatFormFieldModule
  ],
  templateUrl: './datapoint.component.html',
  styleUrl: './datapoint.component.scss'
})
export class DatapointComponent implements OnInit {
  @Input() datapoint!: Datapoint;
  @Output() onSearch = new EventEmitter<Datapoint>();
  @Output() onDelete = new EventEmitter<Datapoint>();
  @Output() onValidate = new EventEmitter<Datapoint>();
  @Output() onRevert = new EventEmitter<Datapoint>();

  currentValue: string | null = null;

  ngOnInit() {
    this.currentValue = this.datapoint.validatedValue ? this.datapoint.validatedValue : this.datapoint.initialValue;
  }

  validateValue() {
    if (!this.datapoint.isValidated) {
      this.datapoint.validatedValue = this.currentValue;
      this.onValidate.emit(this.datapoint);
    }
  }

  revertValue() {
    if (this.datapoint.isValidated) {
      this.currentValue = this.datapoint.validatedValue;
      this.onRevert.emit(this.datapoint);
    }
  }

  resetValue() {
    this.currentValue = this.datapoint.validatedValue ? this.datapoint.validatedValue : this.datapoint.initialValue;
  }

  deleteValue() {
    this.onDelete.emit(this.datapoint);
  }

  searchValue() {
    this.onSearch.emit(this.datapoint);
  }
}
