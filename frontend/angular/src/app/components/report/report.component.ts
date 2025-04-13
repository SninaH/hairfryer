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
  loading: boolean = true; // Property to track loading state

  // call apiService to get report every 2 seconds until status is done
  // Call the API to get the report
  getReport() {
    this.apiService.getReport().subscribe({
      next: (response) => {
        console.log("Response from backend:", response);

        // Check if the response contains the fields indicating the report is done
        if ('total_throws' in response && 'total_pins_fallen' in response) {
          console.log("Report is complete. Saving results.");
          this.gottenReport = response; // Save the report data
          this.loading = false; // Stop loading
        } else {
          console.log("Report is still processing.");
        }
      },
      error: (error) => {
        console.error("Error occurred while fetching report:", error);
        this.loading = false; // Stop loading in case of error
        alert("Failed to fetch the report. Please try again later.");
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
