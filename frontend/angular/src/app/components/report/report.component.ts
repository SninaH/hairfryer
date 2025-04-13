import { Component } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

interface Report {
  total_throws: number;
  total_pins_fallen: number;
  throws: Array<{
    pins_fallen: number;
    pins_hit: [number, number, number, number, number, number, number, number, number]; // Tuple with exactly 9 numbers
  }>;
}

@Component({
  selector: 'app-report',
  imports: [CommonModule],
  templateUrl: './report.component.html',
  styleUrl: './report.component.css'
})


export class ReportComponent {
  // const testResponse = {
  //   status: "done",
  //   results: {
  //     total_throws: 10,
  //     total_pins_fallen: 85,
  //     throws: [
  //       { pins_fallen: 5, pins_hit: [1, 2, 3, 4, 5] },
  //       { pins_fallen: 3, pins_hit: [1, 2, 3] },
  //       { pins_fallen: 4, pins_hit: [1, 2, 3, 4] },
  //     ]
  //   }
  // };


  constructor(
    private apiService: ApiService,
    private router: Router,
  ) { }


  gottenReport: any = null; // Property to hold the report data

  // call apiService to get report every 2 seconds until status is done
  getReport() {
    const sessionId = this.apiService.getSessionId();
    if (!sessionId) {
      console.error('Session ID is not set. Please send the video link first.');
      return;
    }
    console.log("Fetching report for session ID:", sessionId);

    this.apiService.getReport().subscribe({
      next: (response) => {
        console.log("Response from backend:", response);
        // Check if the response indicates processing or done
        if (response.status === "processing") {
          console.log("Report is still processing.");
        } else if (response.status === "done") {
          console.log("Report is complete. Saving results.");
          // Save the report to this.gottenReport
          this.gottenReport = response.results;
        } else {
          console.warn("Unexpected status received:", response.status);
        }
      },
      error: (error) => {
        console.error("Error occurred while fetching report:", error);
      }
    });
  }

  // Call getReport every 2 seconds until we have gottenReport
  ngOnInit() {
    const interval = setInterval(() => {
      this.getReport();
      if (this.gottenReport) {
        clearInterval(interval);
      }
    }, 2000);
  }

  navigateToCoach() {
    this.router.navigate(['/coach']);
  }

}
