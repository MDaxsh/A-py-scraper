import { Component, OnInit, OnDestroy, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ScraperService, ScraperParams, ScraperStatus, ScraperLogEntry } from '../services/scraper.service';
import { interval, Subscription } from 'rxjs';

@Component({
  selector: 'app-scraper-control',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './scraper-control.component.html',
  styleUrls: ['./scraper-control.component.scss']
})
export class ScraperControlComponent implements OnInit, OnDestroy {
  @Output() scraperCompleted = new EventEmitter<void>();

  // Form inputs
  searchQuery: string = 'python developer';
  location: string = 'Remote';
  headless: boolean = true;

  // State
  isRunning: boolean = false;
  status: ScraperStatus | null = null;
  errorMessage: string = '';
  successMessage: string = '';

  // Polling
  private statusSubscription: Subscription | null = null;
  private pollingSubscription: Subscription | null = null;

  constructor(private scraperService: ScraperService) {}

  ngOnInit(): void {
    this.fetchStatus();
  }

  ngOnDestroy(): void {
    this.stopPolling();
  }

  fetchStatus(): void {
    this.scraperService.getStatus().subscribe({
      next: (status) => {
        this.status = status;
        this.isRunning = status.status === 'running' || status.status === 'in_progress';
        
        if (this.isRunning && !this.pollingSubscription) {
          this.startPolling();
        }
      },
      error: (err) => {
        console.error('Failed to fetch status', err);
      }
    });
  }

  startScraper(): void {
    this.errorMessage = '';
    this.successMessage = '';
    this.isRunning = true;

    const params: ScraperParams = {
      search_query: this.searchQuery,
      location: this.location,
      headless: this.headless
    };

    this.scraperService.runScraperAsync(params).subscribe({
      next: (response) => {
        if (response.success) {
          this.successMessage = response.message;
          this.startPolling();
        } else {
          this.errorMessage = response.error || 'Failed to start scraper';
          this.isRunning = false;
        }
      },
      error: (err) => {
        this.errorMessage = err.error?.error || 'Failed to start scraper';
        this.isRunning = false;
      }
    });
  }

  private startPolling(): void {
    this.stopPolling();
    this.pollingSubscription = interval(2000).subscribe(() => {
      this.scraperService.getStatus().subscribe({
        next: (status) => {
          const wasRunning = this.isRunning;
          this.status = status;
          this.isRunning = status.status === 'running' || status.status === 'in_progress';

          if (wasRunning && !this.isRunning) {
            this.stopPolling();
            if (status.status === 'completed') {
              this.successMessage = 'Scraper completed successfully!';
              this.scraperCompleted.emit();
            } else if (status.status === 'error') {
              this.errorMessage = status.current_step || 'Scraper encountered an error';
            }
          }
        },
        error: (err) => {
          console.error('Polling error', err);
        }
      });
    });
  }

  private stopPolling(): void {
    if (this.pollingSubscription) {
      this.pollingSubscription.unsubscribe();
      this.pollingSubscription = null;
    }
  }

  getStatusBadgeClass(): string {
    if (!this.status) return 'bg-secondary';
    
    switch (this.status.status) {
      case 'running':
      case 'in_progress':
        return 'bg-primary';
      case 'completed':
        return 'bg-success';
      case 'error':
        return 'bg-danger';
      default:
        return 'bg-secondary';
    }
  }

  getLogIcon(log: ScraperLogEntry): string {
    return log.emoji || '📝';
  }
}
