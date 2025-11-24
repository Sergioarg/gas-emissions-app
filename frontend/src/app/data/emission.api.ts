import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Emission } from '../core/models/emissions';
import { environment } from '../../environments/environment';
import { ROUTES } from '../core/constants/routes';

@Injectable({
  providedIn: 'root',
})
export class EmissionApi {
  private readonly apiUrl = `${environment.apiUrl}`;

  constructor(private http: HttpClient) { }

  getEmissions(filters?: {
    country?: string;
    activity?: string;
    emission_type?: string;
  }): Observable<Emission[]> {
    let httpParams = new HttpParams();

    if (filters) {
      if (filters.country) {
        httpParams = httpParams.set('country', filters.country);
      }
      if (filters.activity) {
        httpParams = httpParams.set('activity', filters.activity);
      }
      if (filters.emission_type) {
        httpParams = httpParams.set('emission_type', filters.emission_type);
      }
    }

    return this.http.get<Emission[]>(this.apiUrl + ROUTES.emissions, { params: httpParams });
  }
}
