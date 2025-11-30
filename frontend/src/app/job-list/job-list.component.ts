import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { JobsService } from '../services/jobs.service';
import { Job } from '../models/job.model';

@Component({
  selector: 'app-job-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './job-list.component.html',
  styleUrls: ['./job-list.component.scss']
})
export class JobListComponent implements OnInit {
  jobs: Job[] = [];
  totalJobs = 0;
  isLoading = false;
  error: string | null = null;

  // Search and filter state
  searchQuery = '';
  c2cFilter: boolean | null = null;
  hasEmailFilter: boolean | null = null;

  constructor(private jobsService: JobsService) {}

  ngOnInit(): void {
    this.loadJobs();
  }

  loadJobs(): void {
    this.isLoading = true;
    this.error = null;

    this.jobsService.searchJobs(this.searchQuery, this.c2cFilter, this.hasEmailFilter)
      .subscribe({
        next: (response) => {
          this.jobs = response.jobs;
          this.totalJobs = response.total;
          this.isLoading = false;
        },
        error: (err) => {
          this.error = 'Failed to load jobs. Please try again.';
          this.isLoading = false;
          console.error('Error loading jobs:', err);
        }
      });
  }

  onSearch(): void {
    this.loadJobs();
  }

  onC2CFilterChange(value: string): void {
    if (value === '') {
      this.c2cFilter = null;
    } else {
      this.c2cFilter = value === 'true';
    }
    this.loadJobs();
  }

  onEmailFilterChange(value: string): void {
    if (value === '') {
      this.hasEmailFilter = null;
    } else {
      this.hasEmailFilter = value === 'true';
    }
    this.loadJobs();
  }

  clearFilters(): void {
    this.searchQuery = '';
    this.c2cFilter = null;
    this.hasEmailFilter = null;
    this.loadJobs();
  }

  openJobLink(url: string): void {
    window.open(url, '_blank');
  }
}
