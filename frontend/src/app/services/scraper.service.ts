import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ScraperParams {
  search_query?: string;
  location?: string;
  headless?: boolean;
}

export interface ScraperResponse {
  success: boolean;
  message: string;
  output?: string;
  error?: string;
}

export interface ScraperLogEntry {
  timestamp: string;
  step: string;
  message: string;
  emoji: string;
}

export interface ScraperStatus {
  status: string;
  current_step: string;
  total_steps: number;
  completed_steps: number;
  percent: number;
  started_at: string;
  updated_at: string;
  logs: ScraperLogEntry[];
  jobs_file_exists: boolean;
  total_jobs: number;
}

@Injectable({
  providedIn: 'root'
})
export class ScraperService {
  private apiUrl = 'http://localhost:5001/api/scraper';

  constructor(private http: HttpClient) {}

  runScraper(params: ScraperParams): Observable<ScraperResponse> {
    return this.http.post<ScraperResponse>(`${this.apiUrl}/run`, params);
  }

  runScraperAsync(params: ScraperParams): Observable<ScraperResponse> {
    return this.http.post<ScraperResponse>(`${this.apiUrl}/run-async`, params);
  }

  getStatus(): Observable<ScraperStatus> {
    return this.http.get<ScraperStatus>(`${this.apiUrl}/status`);
  }
}
