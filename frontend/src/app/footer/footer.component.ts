import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-footer',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.css']
})
export class FooterComponent implements OnInit {
  appInfo: { name?: string; version?: string; status?: string } = {};
  loading = true;
  error = '';

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    // Use host-mapped backend port. When developing locally the backend is on localhost:5001
    this.http.get<any>('http://localhost:5001/api/app-info')
      .subscribe({
        next: (data) => {
          this.appInfo = data || {};
          this.loading = false;
        },
        error: () => {
          this.error = 'Unable to load app info';
          this.loading = false;
        }
      });
  }
}
