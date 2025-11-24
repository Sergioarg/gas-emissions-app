import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Emission } from '../core/models/emissions';
import { environment } from '../../environments/environment';
import { ROUTES } from '../core/constants/routes';

@Injectable({
  providedIn: 'root',
})
export class EmissionApi {
  private readonly apiUrl = `${environment.apiUrl}`;

  constructor(private http: HttpClient) {}

  getEmissions(filters?: {
    country?: string;
    activity?: string;
    emission_type?: string;
  }): Observable<Emission[]> {
    let url = this.apiUrl + `${ROUTES.emissions}`;
    const params: string[] = [];

    if (filters) {
      if (filters.country) {
        params.push(`country=${encodeURIComponent(filters.country)}`);
      }
      if (filters.activity) {
        params.push(`activity=${encodeURIComponent(filters.activity)}`);
      }
      if (filters.emission_type) {
        params.push(`emission_type=${encodeURIComponent(filters.emission_type)}`);
      }
    }

    if (params.length > 0) {
      url += '?' + params.join('&');
    }

    return this.http.get<Emission[]>(url);
  }
}
