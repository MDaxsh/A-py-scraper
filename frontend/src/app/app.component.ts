import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'My Application';
  backendStatus = 'Loading...';

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.checkBackendHealth();
  }

  checkBackendHealth() {
    this.http.get<any>('http://localhost:5000/api/health')
      .subscribe({
        next: (response: any) => {
          this.backendStatus = response.status;
        },
        error: (error: any) => {
          this.backendStatus = 'Connection error';
        }
      });
  }
}
