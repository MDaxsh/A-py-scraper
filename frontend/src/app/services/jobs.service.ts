import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { JobsResponse } from '../models/job.model';

@Injectable({
  providedIn: 'root'
})
export class JobsService {
  private apiUrl = 'http://localhost:5001/api/jobs';

  constructor(private http: HttpClient) {}

  searchJobs(query?: string, c2c?: boolean | null, hasEmail?: boolean | null): Observable<JobsResponse> {
    let params = new HttpParams();

    if (query && query.trim()) {
      params = params.set('q', query.trim());
    }

    if (c2c !== null && c2c !== undefined) {
      params = params.set('c2c', c2c.toString());
    }

    if (hasEmail !== null && hasEmail !== undefined) {
      params = params.set('has_email', hasEmail.toString());
    }

    return this.http.get<JobsResponse>(`${this.apiUrl}/search`, { params });
  }
}
