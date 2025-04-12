import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment.development';

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
  private responseData: {session_id: string, preview_image_url: string} | null = null;

  constructor(private http: HttpClient) {}

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
}