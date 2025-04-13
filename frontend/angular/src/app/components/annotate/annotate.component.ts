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

  annotations = [
    {
      id: 1,
      points: [
        [70, 144], // Top-left corner
        [70, 164], // Bottom-left corner
        [93, 164], // Bottom-right corner
        [93, 144], // Top-right corner
      ],
      phi: 0, // Rotation angle
      categories: ['Order'], // Category for the annotation
      type: 'rectangle', // Shape type
      color: 'rgba(255, 0, 0, 0.2)', // Annotation color with transparency
    },
    {
      id: 2,
      points: [
        [144, 144],
        [144, 164],
        [157, 164],
        [157, 144],
      ],
      phi: 0,
      categories: ['Throw'],
      type: 'rectangle',
      color: 'rgba(0, 255, 0, 0.2)',
    },
    {
      id: 3,
      points: [
        [221, 144],
        [221, 164],
        [234, 164],
        [234, 144],
      ],
      phi: 0,
      categories: ['Lane'],
      type: 'rectangle',
      color: 'rgba(0, 0, 255, 0.2)',
    },
    {
      id: 4,
      points: [
        [144, 43],
        [144, 53],
        [155, 53],
        [155, 43],
      ],
      phi: 0,
      categories: ['Pin 1'],
      type: 'rectangle',
      color: 'rgba(255, 165, 0, 0.2)',
    },
    {
      id: 5,
      points: [
        [108, 62],
        [108, 71],
        [119, 71],
        [119, 62],
      ],
      phi: 0,
      categories: ['Pin 2'],
      type: 'rectangle',
      color: 'rgba(255, 165, 0, 0.2)',
    },
    {
      id: 6,
      points: [
        [181, 60],
        [181, 72],
        [192, 72],
        [192, 60],
      ],
      phi: 0,
      categories: ['Pin 3'],
      type: 'rectangle',
      color: 'rgba(255, 165, 0, 0.2)',
    },
    {
      id: 7,
      points: [
        [73, 80],
        [73, 90],
        [84, 90],
        [84, 80],
      ],
      phi: 0,
      categories: ['Pin 4'],
      type: 'rectangle',
      color: 'rgba(255, 165, 0, 0.2)',
    },
    {
      id: 8,
      points: [
        [145, 80],
        [145, 90],
        [155, 90],
        [155, 80],
      ],
      phi: 0,
      categories: ['Pin 5'],
      type: 'rectangle',
      color: 'rgba(255, 165, 0, 0.2)',
    },
    {
      id: 9,
      points: [
        [217, 79],
        [217, 90],
        [229, 90],
        [229, 79],
      ],
      phi: 0,
      categories: ['Pin 6'],
      type: 'rectangle',
      color: 'rgba(255, 165, 0, 0.2)',
    },
    {
      id: 10,
      points: [
        [108, 98],
        [108, 108],
        [119, 108],
        [119, 98],
      ],
      phi: 0,
      categories: ['Pin 7'],
      type: 'rectangle',
      color: 'rgba(255, 165, 0, 0.2)',
    },
    {
      id: 11,
      points: [
        [181, 98],
        [181, 108],
        [192, 108],
        [192, 98],
      ],
      phi: 0,
      categories: ['Pin 8'],
      type: 'rectangle',
      color: 'rgba(255, 165, 0, 0.2)',
    },
    {
      id: 12,
      points: [
        [145, 117],
        [145, 127],
        [156, 127],
        [156, 117],
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
  ) { }

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

    this.apiService.submitCoordinates(rectangles).subscribe({
      next: (response) => {
        console.log('Response from backend:', response);
        alert("Annotations sent successfully!");
      },
      error: (error) => {
        console.error('Error occurred:', error);
        alert("Error sending annotations :(");
      }
    });
  }
}