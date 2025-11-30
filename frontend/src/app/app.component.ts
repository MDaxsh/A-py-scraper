import { Component, OnInit, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { FooterComponent } from './footer/footer.component';
import { JobListComponent } from './job-list/job-list.component';
import { ScraperControlComponent } from './scraper-control/scraper-control.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FooterComponent, JobListComponent, ScraperControlComponent],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  @ViewChild(JobListComponent) jobList!: JobListComponent;

  title = 'Py scraper';
  backendStatus = 'Loading...';

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.checkBackendHealth();
  }

  checkBackendHealth() {
    this.http.get<any>('http://localhost:5001/api/health')
      .subscribe({
        next: (response: any) => {
          this.backendStatus = response.status;
        },
        error: (error: any) => {
          this.backendStatus = 'Connection error';
        }
      });
  }

  onScraperCompleted(): void {
    // Refresh the job list when scraper completes
    if (this.jobList) {
      this.jobList.loadJobs();
    }
  }
}
