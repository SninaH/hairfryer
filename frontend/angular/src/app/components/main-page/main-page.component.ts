import { Component } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-main-page',
  templateUrl: './main-page.component.html',
  styleUrls: ['./main-page.component.css'],
  imports: [FormsModule, CommonModule]
})
export class MainPageComponent {
  videoLink: string = ''; // Property to hold the textarea content
  loading: boolean = false; // Property to track loading state

  constructor(
    private apiService: ApiService,
    private router: Router,
  ) {}

  onSubmit(): void {
    const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$/;
    if (!youtubeRegex.test(this.videoLink)) {
      alert("Please enter a valid YouTube link.");
      return;
    }

    this.loading = true; // Start loading
    this.apiService.sendVideoLink(this.videoLink).subscribe({
      next: (response) => {
        console.log("Response from backend:", response);
        this.loading = false; // Stop loading

        // Check if the response contains the expected data
        if (response && response.session_id && response.preview_image_url) {
          console.log("Video link sent successfully");
          this.apiService.setResponseData(response); // Save the response data for later use
          this.router.navigate(['/annotate']);
        } else {
          console.error("Unexpected response format:", response);
          alert("Unexpected response from the server. Please try again.");
        }
      },
      error: (error) => {
        console.error("Error occurred while sending video link:", error);
        this.loading = false; // Stop loading
        alert("An error occurred while sending the video link. Please check the console for details.");
      }
    });
  }
}