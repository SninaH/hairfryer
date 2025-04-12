import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-annotate',
  imports: [],
  templateUrl: './annotate.component.html',
  styleUrl: './annotate.component.css'
})

export class AnnotateComponent implements OnInit {
  private sessionId!: string;
  private imageUrl!: string;

  private canvas!: HTMLCanvasElement;
  private ctx!: CanvasRenderingContext2D;
  private isDrawing = false;
  private startX = 0;
  private startY = 0;
  private rectWidth = 0;
  private rectHeight = 0;
  private imageWidth = 0;
  private imageHeight = 0;
  private scaleFactor = 1; // Scale factor for image-to-canvas mapping

  constructor(
    private apiService: ApiService,
  ) { }

  ngOnInit(): void {
    const response = this.apiService.getResponseData();
    if (response) {
      if (response.session_id && response.preview_image_url) {
        this.sessionId = response.session_id;
        this.imageUrl = response.preview_image_url;
        console.log('Session ID:', this.sessionId);
        console.log('Preview Image URL:', this.imageUrl);
      } else {
        console.error('Invalid response data:', response);
        return;
        // TODO: decide what to display if the response is invalid
      }

      this.initializeCanvas();
    } else {
      console.error('No response data found!');
      // TODO: decide what to display if the response is invalid
      return;
    }
  }

  initializeCanvas(): void {
    this.canvas = document.getElementById('imageCanvas') as HTMLCanvasElement;
    this.ctx = this.canvas.getContext('2d')!;

    const image = new Image();
    image.src = this.imageUrl;
    image.onload = () => {
      // Calculate scale factor to fit the image within the canvas
      this.imageWidth = image.width;
      this.imageHeight = image.height;

      const canvasWidth = 800; // Set your desired canvas width
      const canvasHeight = 600; // Set your desired canvas height
      const widthRatio = canvasWidth / this.imageWidth;
      const heightRatio = canvasHeight / this.imageHeight;
      this.scaleFactor = Math.min(widthRatio, heightRatio);

      // Set canvas size to match the scaled image
      this.canvas.width = this.imageWidth * this.scaleFactor;
      this.canvas.height = this.imageHeight * this.scaleFactor;

      // Draw the scaled image on the canvas
      this.ctx.drawImage(
        image,
        0,
        0,
        this.imageWidth * this.scaleFactor,
        this.imageHeight * this.scaleFactor
      );
    };

    // Add mouse event listeners
    this.canvas.addEventListener('mousedown', this.startDrawing.bind(this));
    this.canvas.addEventListener('mousemove', this.drawRectangle.bind(this));
    this.canvas.addEventListener('mouseup', this.stopDrawing.bind(this));
  }

  startDrawing(event: MouseEvent): void {
    this.isDrawing = true;
    const rect = this.canvas.getBoundingClientRect();
    this.startX = (event.clientX - rect.left) / this.scaleFactor;
    this.startY = (event.clientY - rect.top) / this.scaleFactor;
  }

  drawRectangle(event: MouseEvent): void {
    if (!this.isDrawing) return;

    const rect = this.canvas.getBoundingClientRect();
    const currentX = (event.clientX - rect.left) / this.scaleFactor;
    const currentY = (event.clientY - rect.top) / this.scaleFactor;

    this.rectWidth = currentX - this.startX;
    this.rectHeight = currentY - this.startY;

    // Clear the canvas and redraw the image and rectangle
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    const image = new Image();
    image.src = this.imageUrl;
    image.onload = () => {
      this.ctx.drawImage(
        image,
        0,
        0,
        this.imageWidth * this.scaleFactor,
        this.imageHeight * this.scaleFactor
      );
      this.ctx.strokeStyle = 'red';
      this.ctx.lineWidth = 2;
      this.ctx.strokeRect(
        this.startX * this.scaleFactor,
        this.startY * this.scaleFactor,
        this.rectWidth * this.scaleFactor,
        this.rectHeight * this.scaleFactor
      );
    };
  }

  stopDrawing(): void {
    this.isDrawing = false;
  }

  saveRectangle(): void {
    // Scale rectangle coordinates back to the original image dimensions
    const originalStartX = this.startX;
    const originalStartY = this.startY;
    const originalWidth = this.rectWidth;
    const originalHeight = this.rectHeight;

    console.log('Top-left corner:', originalStartX, originalStartY);
    console.log('Width:', originalWidth);
    console.log('Height:', originalHeight);
    alert(`Rectangle saved! Coordinates: (${originalStartX}, ${originalStartY}), Width: ${originalWidth}, Height: ${originalHeight}`);
  }

}

