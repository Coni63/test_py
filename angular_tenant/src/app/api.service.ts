import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private apiUrl = '/api/people/';

  constructor(private http: HttpClient) {}

  getPeople(): Observable<any> {
    return this.http.get<any>(this.apiUrl);
  }
}
