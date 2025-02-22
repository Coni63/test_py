// test-data.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ApiResponse, TestData } from './test.interface';

@Injectable({
  providedIn: 'root'
})
export class TestDataService {
  private apiUrl = '/sample/test/'; // Update with your API URL

  constructor(private http: HttpClient) {}

  getTestData(
    pageIndex: number,
    pageSize: number,
    sortField: string,
    sortDirection: string,
    filters: any
  ): Observable<ApiResponse> {
    let params = new HttpParams()
      .set('page', (pageIndex + 1).toString())
      .set('page_size', pageSize.toString());

    if (sortField) {
      params = params.set('ordering', sortDirection === 'desc' ? `-${sortField}` : sortField);
    }

    // Add filters
    Object.keys(filters).forEach(key => {
      if (filters[key] !== null && filters[key] !== '') {
        params = params.set(key, filters[key]);
      }
    });

    return this.http.get<ApiResponse>(this.apiUrl, { params });
  }
}
