import { Component } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-main-page',
  templateUrl: './main-page.component.html',
  styleUrls: ['./main-page.component.css'],
  imports: [FormsModule]
})
export class MainPageComponent {
  videoLink: string = ''; // Property to hold the textarea content

  constructor(
    private apiService: ApiService,
    private router: Router,
  ) {}

  onSubmit(): void {
    // check first if the link is a valid youtube link
    const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$/;
    if (!youtubeRegex.test(this.videoLink)) {
      alert("Please enter a valid YouTube link.");
      return;
    }
    // send the link to the backend
    this.apiService.sendVideoLink(this.videoLink).subscribe({
      next: (response) => {
        console.log('Response from backend:', response);
        // response format: "success"
        if(response == "success") {
          console.log("Video link sent successfully");
          this.router.navigate(['/annotate']);
        } else {
          console.error("Error sending video link");
          alert("Error sending video link :(");
        }
        
      },
      error: (error) => {
        console.error('Error occurred:', error);
      }
    });
  }
}