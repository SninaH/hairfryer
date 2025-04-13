import cv2
import numpy as np
import time
import torch
import cv2
import matplotlib.pyplot as plt
from torchvision import transforms
import timm
import mediapipe as mp


def estimate_pose1():
    # Initialize Pose Estimation
    mp_pose = mp.solutions.pose
    #pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    pose = mp_pose.Pose()

    # Open video file
    #cap = cv2.VideoCapture('movie.mp4')
    cap = cv2.VideoCapture('output.mp4')

    # Define key landmarks for stability detection
    key_landmarks = [mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.RIGHT_SHOULDER
                    #mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.RIGHT_HIP
    ]

    # Initialize previous landmarks
    prev_landmarks = None
    movement_threshold = 0.005  # Adjust as needed
    stationary_frames = 0
    start_detected = False

    # Predefined normal behavior
    normal_landmarks = {
        mp_pose.PoseLandmark.LEFT_SHOULDER: (0.2, 0.3),
        mp_pose.PoseLandmark.RIGHT_SHOULDER: (0.8, 0.3),
        # Define other key landmarks as needed
    }

    PBOX_x1 = 330
    PBOX_y1 = 180
    PBOX_x2 = 490
    PBOX_y2 = 355

    i = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        sub_rgb_frame = rgb_frame[PBOX_y1:PBOX_y2,PBOX_x1:PBOX_x2]


        if i % 5 == 0:
            # Process the frame
            results = pose.process(sub_rgb_frame)
            
            # Extract landmarks
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
            else:
                landmarks = None
            
            # Track movement for start phase
            if landmarks and prev_landmarks:
                total_movement = 0.0
                for lm in key_landmarks:
                    current = np.array([landmarks[lm.value].x, landmarks[lm.value].y])
                    previous = np.array([prev_landmarks[lm.value].x, prev_landmarks[lm.value].y])
                    movement = np.linalg.norm(current - previous)
                    total_movement += movement
                
                average_movement = total_movement / len(key_landmarks)
                #print(average_movement)
                if average_movement < movement_threshold:
                    stationary_frames += 1
                else:
                    print("HHHH")
                    stationary_frames = 0
                
                # Detect start phase
                if stationary_frames > 10:  # Adjust the number of frames as needed
                    start_detected = True
                    #print("Start phase detected!")
                    stationary_frames = 0  # Reset counter
            
            # Detect unconventional behavior if start phase is detected
            if landmarks and start_detected:
                deviation = 0.0
                for lm in key_landmarks:
                    current = np.array([landmarks[lm.value].x, landmarks[lm.value].y])
                    normal = np.array(normal_landmarks[lm])
                    diff = np.linalg.norm(current - normal)
                    deviation += diff
                
                average_deviation = deviation / len(key_landmarks)
                deviation_threshold = 0.1  # Adjust as needed
                
                #if average_deviation > deviation_threshold:
                #    print("Unconventional behavior detected!")
            
            # Update previous landmarks
            prev_landmarks = landmarks
            
            # Draw pose landmarks
            if results.pose_landmarks:
                mp_drawing = mp.solutions.drawing_utils
                #print(type(results.pose_landmarks))
                mp_drawing.draw_landmarks(frame[PBOX_y1:PBOX_y2,PBOX_x1:PBOX_x2], results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        else:
            if results.pose_landmarks:
                mp_drawing = mp.solutions.drawing_utils
                #print(type(results.pose_landmarks))
                #mp_drawing.draw_landmarks(frame[PBOX_y1:PBOX_y2,PBOX_x1:PBOX_x2], results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        # Display the frame
        #cv2.imshow('Pose Estimation', frame[PBOX_y1:PBOX_y2,PBOX_x1:PBOX_x2])
        cv2.imshow('Pose Estimation', frame[PBOX_y1:PBOX_y2,PBOX_x1:PBOX_x2])
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        i += 1

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    estimate_pose1()