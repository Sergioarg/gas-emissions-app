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

  getEmissions(): Observable<Emission[]> {
    return this.http.get<Emission[]>(this.apiUrl + `${ROUTES.emissions}`);
  }
}
