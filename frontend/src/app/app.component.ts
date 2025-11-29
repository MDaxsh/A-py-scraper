import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'My Application';
  backendStatus = 'Loading...';

  constructor(private http: HttpClient) {
    this.checkBackendHealth();
  }

  checkBackendHealth() {
    this.http.get<any>('http://localhost:5000/api/health')
      .subscribe(
        (response) => {
          this.backendStatus = response.status;
        },
        (error) => {
          this.backendStatus = 'Connection error';
        }
      );
  }
}
