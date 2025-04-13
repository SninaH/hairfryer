import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-coach',
  imports: [CommonModule],
  templateUrl: './coach.component.html',
  styleUrl: './coach.component.css'
})
export class CoachComponent {
  constructor(
    private router: Router,
    private apiService: ApiService
  ) {}

  videoUrl: string = '/images/output.mp4'; // URL of the video to be displayed

  ngOnInit(): void {
    // Fetch the video link when the component initializes
    this.apiService.getVideoLink().subscribe({
      next: (response) => {
        this.videoUrl = response.videoUrl;
        console.log('Video URL fetched:', this.videoUrl);
      },
      error: (error) => {
        console.error('Error fetching video URL:', error);
      },
    });
  }

  navigateToReport() {
    this.router.navigate(['/report']);
  }
}
