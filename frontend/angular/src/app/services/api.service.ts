import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment.development';
import { Rectangles } from '../classes/rectangles';

// response when sending video link format
interface ResponseData {
  session_id: string;
  preview_image_url: string; // URL of the image the user will annotate (location where the score is displayed)
}



@Injectable({
  providedIn: 'root', // Makes the service available application-wide
})
export class ApiService {
  private apiUrl = environment.apiUrl;
  private responseData: { session_id: string, preview_image_url: string } | null = null;

  constructor(private http: HttpClient) { }

  sendVideoLink(videoLink: string): Observable<any> {
    const payload = { videoLink };
    // return this.http.post(this.apiUrl + "upload-youtube", payload);

    //return test data just to check if the function is called properly
    return new Observable((observer) => {
      this.responseData = {
        session_id: "xyz789",
        preview_image_url: "images/test_image.jpg"
      };
      observer.next("success");
      observer.complete();
    });
  }

  setResponseData(data: ResponseData): void {
    this.responseData = data;
  }

  getResponseData(): ResponseData | null {
    return this.responseData;
  }

  /*
  POST /api/v1/submit-coordinates
request:
{
  "session_id": "xyz789",
  "coordinates": {
    "throw_order": [120, 200, 453, 544],      #zaporedni met
    "pins_fallen_in_throw": [120, 200, 453, 544],      # podrti keglji v metu
    "pins_fallen_on_lane": [120, 200, 453, 544],        # podrti keglji na stezi
    "pins": {
        "pin_1": [120, 200, 453, 544],
        "pin_2": [120, 200, 453, 544],
        "pin_3": [120, 200, 453, 544],
        "pin_4": [120, 200, 453, 544],
        "pin_5": [120, 200, 453, 544],
        "pin_6": [120, 200, 453, 544],
        "pin_7": [120, 200, 453, 544],
        "pin_8": [120, 200, 453, 544],
        "pin_9": [120, 200, 453, 544],
    }
  }
}
  */
  submitCoordinates(rectangles: Rectangles): Observable<any> {
    if (!this.responseData) {
      throw new Error('Session ID is not set. Please send the video link first.');
    }
    const payload = {
      session_id: this.responseData?.session_id,
      coordinates: rectangles
    };
    // return this.http.post(`${this.apiUrl}/submit-coordinates`, payload);
    //return test data just to check if the function is called properly
    return new Observable((observer) => {
      console.log("Payload sent to backend:", payload);
      observer.next("success");
      observer.complete();
    });
  }
}