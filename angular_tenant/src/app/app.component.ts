import { Component, inject, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ApiService } from './api.service';
import { Observable, of } from 'rxjs';
import { CommonModule } from '@angular/common';


@Component({
  selector: 'app-root',
  imports: [CommonModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
  standalone: true,
})
export class AppComponent implements OnInit {
  private readonly apiService = inject(ApiService);
  title = 'angular_tenant';
  
  people$: Observable<any>;

  constructor() {
    this.people$ = of({});
  }

  ngOnInit() {
    this.people$ = this.apiService.getPeople();
  }
}
