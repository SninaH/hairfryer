import { Component, ViewChild } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AnnotatorComponent, Shape } from 'ngx-image-annotation';
import { Rectangle } from 'ngx-image-annotation';
import { Rectangles } from '../../classes/rectangles';

@Component({
  selector: 'app-annotate',
  templateUrl: './annotate.component.html',
  styleUrls: ['./annotate.component.css'],
  imports: [CommonModule, AnnotatorComponent]
})
export class AnnotateComponent {

  @ViewChild('annotator') annotator!: AnnotatorComponent;

  imageUrl: string = 'images/test_image.jpg'; // Replace with your image path
  objectsToAnnotate: string[] = ['throw order', 'pins fallen in throw', 'pins fallen on lane', 'pin 1', 'pin 2', 'pin 3', 'pin 4', 'pin 5', 'pin 6', 'pin 7', 'pin 8', 'pin 9']; // Predefined list of objects
  objectsToAnnotateLabels: string[] = ['Order', 'Throw', 'Lane', 'Pin 1', 'Pin 2', 'Pin 3', 'Pin 4', 'Pin 5', 'Pin 6', 'Pin 7', 'Pin 8', 'Pin 9']; // Labels for the objects
  currentObjectIndex: number = 0;
  loading: boolean = false; // Property to track loading state

  annotations = [
    {
      id: 1,
      points: [
        [729, 144], // Top-left corner
        [729, 167], // Bottom-left corner
        [756, 167], // Bottom-right corner
        [756, 144], // Top-right corner
      ],
      phi: 0,
      categories: ['Order'],
      type: 'rectangle',
      color: 'rgba(255, 0, 0, 0.2)',
    },
    {
      id: 2,
      points: [
        [805, 145],
        [805, 167],
        [824, 167],
        [824, 145],
      ],
      phi: 0,
      categories: ['Throw'],
      type: 'rectangle',
      color: 'rgba(0, 255, 0, 0.2)',
    },
    {
      id: 3,
      points: [
        [857, 145],
        [857, 167],
        [900, 167],
        [900, 145],
      ],
      phi: 0,
      categories: ['Lane'],
      type: 'rectangle',
      color: 'rgba(0, 0, 255, 0.2)',
    },
    {
      id: 4,
      points: [
        [812, 44],
        [812, 54],
        [822, 54],
        [822, 44],
      ],
      phi: 0,
      categories: ['Pin 1'],
      type: 'rectangle',
      color: 'rgba(255, 165, 0, 0.2)',
    },
    {
      id: 5,
      points: [
        [775, 63],
        [775, 73],
        [785, 73],
        [785, 63],
      ],
      phi: 0,
      categories: ['Pin 2'],
      type: 'rectangle',
      color: 'rgba(255, 165, 0, 0.2)',
    },
    {
      id: 6,
      points: [
        [848, 64],
        [848, 74],
        [858, 74],
        [858, 64],
      ],
      phi: 0,
      categories: ['Pin 3'],
      type: 'rectangle',
      color: 'rgba(255, 165, 0, 0.2)',
    },
    {
      id: 7,
      points: [
        [737, 81],
        [737, 91],
        [747, 91],
        [747, 81],
      ],
      phi: 0,
      categories: ['Pin 4'],
      type: 'rectangle',
      color: 'rgba(255, 165, 0, 0.2)',
    },
    {
      id: 8,
      points: [
        [812, 83],
        [812, 93],
        [822, 93],
        [822, 83],
      ],
      phi: 0,
      categories: ['Pin 5'],
      type: 'rectangle',
      color: 'rgba(255, 165, 0, 0.2)',
    },
    {
      id: 9,
      points: [
        [886, 83],
        [886, 93],
        [896, 93],
        [896, 83],
      ],
      phi: 0,
      categories: ['Pin 6'],
      type: 'rectangle',
      color: 'rgba(255, 165, 0, 0.2)',
    },
    {
      id: 10,
      points: [
        [774, 100],
        [774, 110],
        [784, 110],
        [784, 100],
      ],
      phi: 0,
      categories: ['Pin 7'],
      type: 'rectangle',
      color: 'rgba(255, 165, 0, 0.2)',
    },
    {
      id: 11,
      points: [
        [850, 103],
        [850, 113],
        [860, 113],
        [860, 103],
      ],
      phi: 0,
      categories: ['Pin 8'],
      type: 'rectangle',
      color: 'rgba(255, 165, 0, 0.2)',
    },
    {
      id: 12,
      points: [
        [811, 120],
        [811, 130],
        [821, 130],
        [821, 120],
      ],
      phi: 0,
      categories: ['Pin 9'],
      type: 'rectangle',
      color: 'rgba(255, 165, 0, 0.2)',
    },
  ];

  constructor(
    private apiService: ApiService,
    private router: Router,
  ) {
    this.imageUrl = this.apiService.getResponseData()?.preview_image_url || 'images/test_image.jpg';
    console.log('Image URL:', this.imageUrl);
    // Log the dimensions of the image
    const img = new Image();
    img.src = this.imageUrl;
    img.onload = () => {
      console.log(`Image Dimensions: ${img.width}px x ${img.height}px`);
    };
  }

  goBack(): void {
    this.router.navigate(['/']);
  }

  // Called when a new annotation is added
  onAnnotationAdded(shape: Shape): void {
    if (this.currentObjectIndex < this.objectsToAnnotate.length) {
      const objectName = this.objectsToAnnotateLabels[this.currentObjectIndex];
      this.annotations.push({
        id: shape.id,
        points: (shape as Rectangle).points,
        phi: shape.phi,
        categories: [objectName],
        type: 'rectangle',
        color: 'rgba(0, 0, 0, 0.2)', // Default color
      });
      this.annotator.updateCategories(shape.id, [objectName]);
      this.currentObjectIndex++;
    } else {
      alert('All objects have been annotated!');
    }
  }

  // Called when an annotation is right-clicked
  editAnnotation(shape: Shape): void {
    const objectName = prompt('Update the object name for this annotation:', shape.categories[0] || '');
    if (objectName) {
      const annotation = this.annotations.find((a) => a.id === shape.id);
      if (annotation) {
        annotation.categories = [objectName];
        this.annotator.updateCategories(shape.id, [objectName]);
      }
    }
  }

  onAnnotationEdited(shape: Shape): void {
    // Find the annotation that matches the edited shape
    const annotation = this.annotations.find((a) => a.id === shape.id);

    if (annotation) {
      // Update the shape of the annotation with the new edited shape
      annotation.points = (shape as Rectangle).points;
      annotation.phi = shape.phi;

      // Log the updated annotation for debugging
      console.log(`Annotation with ID ${shape.id} has been updated:`, annotation);
    } else {
      console.warn(`No annotation found with ID ${shape.id}`);
    }
  }

  sendAnnotations(): void {
    console.log('Final Annotations:', this.annotations);
    var rectangles = new Rectangles();

    // Populate the rectangles object with the annotations
    for (let annotation of this.annotations) {
      const topLeft = annotation.points[0];
      const bottomRight = annotation.points[2];
      const x = topLeft[0]; // Access the x-coordinate of the first point
      const y = topLeft[1]; // Access the y-coordinate of the first point
      const width = bottomRight[0] - x; // Calculate width
      const height = bottomRight[1] - y; // Calculate height

      if (annotation.categories[0] === 'Order') {
        rectangles.throw_order = [x, y, width, height];
      } else if (annotation.categories[0] === 'Throw') {
        rectangles.pins_fallen_in_throw = [x, y, width, height];
      } else if (annotation.categories[0] === 'Lane') {
        rectangles.pins_fallen_on_lane = [x, y, width, height];
      } else {
        const pinIndex = parseInt(annotation.categories[0].split(' ')[1]) - 1; // Assuming pin names are like "Pin 1", "Pin 2", etc.
        const pinKey = `pin_${pinIndex + 1}` as keyof typeof rectangles.pins; // Explicitly assert the key type
        rectangles.pins[pinKey] = [x, y, width, height];
      }
    }

    this.loading = true; // Start loading
    this.apiService.submitCoordinates(rectangles).subscribe({
      next: (response) => {
        console.log('Response from backend:', response);
        console.log("Annotations sent successfully!");
        this.loading = false; // Stop loading
        // go to reports component
        this.router.navigate(['/report']);
      },
      error: (error) => {
        console.error('Error occurred:', error);
        this.loading = false; // Stop loading
        alert("Error sending annotations :(");
      }
    });
  }
}