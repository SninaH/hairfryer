import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { tap, catchError } from 'rxjs/operators';
import { environment } from '../../environments/environment.development';
import { Rectangles } from '../classes/rectangles';

// response when sending video link format
interface ResponseData {
  session_id: string;
  preview_image_url: string; // URL of the image the user will annotate (location where the score is displayed)
}

interface ReportResponse {
  status: string;
  results: any; // Replace `any` with a more specific type if you know the structure of `results`
}


@Injectable({
  providedIn: 'root', // Makes the service available application-wide
})
export class ApiService {
  private apiUrl = environment.apiUrl;
  private responseData: { session_id: string, preview_image_url: string } | null = null;
  private report: { status: string, results: any } | null = null;

  constructor(private http: HttpClient) { }

  sendVideoLink(videoLink: string): Observable<any> {
    const payload = { "youtube_url": videoLink };
    console.log("Payload sent to backend:", payload);

    return this.http.post(this.apiUrl + "/upload-youtube", payload).pipe(
      tap((response) => {
        console.log("Response received from backend:", response);
      }),
      catchError((error) => {
        console.error("Error occurred while sending video link:", error);
        return throwError(() => new Error("Failed to send video link. Please check the backend."));
      })
    );
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
    // return test data just to check if the function is called properly
    return new Observable((observer) => {
      console.log("Payload sent to backend:", payload);
      observer.next({
        "status": "coordinates_received",
        "message": "Coordinates successfully received, processing will continue."
      });
      observer.complete();
    });
  }

  /*
  GET /api/v1/status/{session_id}
response ČE ŠE NI:
{
  "status": "processing"
}
response ČE ŽE JE:
{
  "status": "done",
  "results": {
    "total_throws": 10,
    "total_pins_fallen": 85,
    "throws":[
        {
          pins_fallen: 5,               # št podrtih kegljev
          pins_hit: [1, 2, 3, 4, 5],        # številjke kegljev ki so bili podrti
        },
        {
          pins_fallen: 3,
          pins_hit: [1, 2, 3],
        },
        {
          pins_fallen: 4,
          pins_hit: [1, 2, 3, 4],
        },
    ]
  }
}
  */
  getReport(): Observable<ReportResponse> {
    const sessionId = this.responseData?.session_id;
    if (!sessionId) {
      throw new Error('Session ID is not set. Please send the video link first.');
    }
    console.log("Fetching report for session ID:", sessionId);

    // return this.http.get<ReportResponse>(`${this.apiUrl}/status/${sessionId}`).pipe(
    //   tap((response: ReportResponse) => {
    //     console.log("Response received from backend:", response);

    //     // Check if the response indicates processing or done
    //     if (response.status === "processing") {
    //       console.log("Report is still processing.");
    //     } else if (response.status === "done") {
    //       console.log("Report is complete. Saving results.");
    //       // Save the report to this.report
    //       this.report = response;
    //     } else {
    //       console.warn("Unexpected status received:", response.status);
    //     }
    //   }),
    //   catchError((error) => {
    //     console.error("Error occurred while fetching report:", error);
    //     return throwError(() => new Error("Failed to fetch report. Please check the backend."));
    //   })
    // );
    // return test data just to check if the function is called properly
    return new Observable((observer) => {
      console.log("Fetching report for session ID:", sessionId);
      const testResponse = {
        status: "done",
        results: {
          total_throws: 10,
          total_pins_fallen: 85,
          throws: [
            { pins_fallen: 5, pins_hit: [0, 1, 0, 0, 1, 0, 0, 0, 1] },
            { pins_fallen: 3, pins_hit: [0, 1, 0, 0, 1, 0, 0, 0, 1] },
            { pins_fallen: 4, pins_hit: [0, 1, 0, 0, 1, 0, 0, 0, 1] },
          ]
        }
      };
      observer.next(testResponse);
      observer.complete();
    });
  }

  getReportData(): { status: string, results: any } | null {
    return this.report;
  }

  getSessionId(): string | null {
    return this.responseData?.session_id || null;
  }

  // Fetch the video link from the backend
  getVideoLink(): Observable<{ videoUrl: string }> {
    // return this.http.get<{ videoUrl: string }>(`${this.apiUrl}/video-link`);
    // return test data just to check if the function is called properly
    return new Observable((observer) => {
      const testResponse = {
        videoUrl: "/images/output_h264.mp4" // URL of the video to be displayed
      };
      observer.next(testResponse);
      observer.complete();
    }
    );
  }

}