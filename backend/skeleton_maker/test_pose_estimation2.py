import cv2
import numpy as np
import time
import torch
import cv2
import matplotlib.pyplot as plt
from torchvision import transforms
import timm
import mediapipe as mp
import pickle
from math import sqrt
import pandas as pd


def estimate_pose2():
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

    PBOX_x1 = 325
    PBOX_y1 = 180
    PBOX_x2 = 490
    PBOX_y2 = 360


    #START_BOX_x1 = 350
    #START_BOX_y1 = 220
    #START_BOX_x2 = 400
    #START_BOX_y2 = 335

    START_BOX_x1 = 345
    START_BOX_y1 = 220
    START_BOX_x2 = 415
    START_BOX_y2 = 340

    start_threshold = 1.5


    i = 0

    counter = 0
    save_index = 0
    sequence_curr = []

    with open("starting_pos_ref2.pkl", "rb") as f:
        ref_pos = pickle.load(f)

    def distance_to_ref_pos(ref_pos, _pos):
        pos = [(x.x, x.y) for x in _pos]
        if len(pos) != len(ref_pos):
            return 10
        return sum([sqrt((x[0]-y[0])**2 + (x[1]-y[1])**2) for (x,y) in zip(ref_pos, pos)])

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        sub_rgb_frame = rgb_frame[PBOX_y1:PBOX_y2,PBOX_x1:PBOX_x2]
        init_pos_rgb_frame = rgb_frame[START_BOX_y1:START_BOX_y2,START_BOX_x1:START_BOX_x2]

        if not start_detected and i % 5 == 0:

            # Process the frame
            results = pose.process(init_pos_rgb_frame)
            
            # Extract landmarks
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
            else:
                landmarks = None
            
            
            if landmarks:
                mp_drawing = mp.solutions.drawing_utils
                #print(type(results.pose_landmarks))
                mp_drawing.draw_landmarks(frame[START_BOX_y1:START_BOX_y2,START_BOX_x1:START_BOX_x2], results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                dist = distance_to_ref_pos(ref_pos, results.pose_landmarks.landmark)
                print(dist)
                if dist < start_threshold:
                    start_detected = True
                    sequence_curr.append(results.pose_landmarks.landmark)
        
        elif start_detected:
            if counter == 0:
                print("START DETECTED!")
            if counter < 65:
                results = pose.process(sub_rgb_frame)
        
                if results.pose_landmarks:
                    mp_drawing = mp.solutions.drawing_utils
                    #print(type(results.pose_landmarks))
                    mp_drawing.draw_landmarks(frame[PBOX_y1:PBOX_y2,PBOX_x1:PBOX_x2], results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                    #print(distance_to_ref_pos(ref_pos, results.pose_landmarks.landmark))
                    sequence_curr.append(results.pose_landmarks.landmark)
            else:
                # save
                for i, skeleton in enumerate(sequence_curr):
                    file_name = f"skeletons_o2/skeleton_{save_index}_{i}.csv"
                    data = np.array([[x.x, x.y, x.z, x.visibility] for x in skeleton])
                    np.savetxt(file_name, data, delimiter=",")
                
                sequence_curr = []
                save_index += 1
                start_detected = False
            counter += 1
        
        else:
            start_detected = False
            counter = 0
            results = pose.process(init_pos_rgb_frame)

            if results.pose_landmarks:
                #mp_drawing = mp.solutions.drawing_utils
                #print(type(results.pose_landmarks))
                #mp_drawing.draw_landmarks(frame[START_BOX_y1:START_BOX_y2,START_BOX_x1:START_BOX_x2], results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                print(distance_to_ref_pos(ref_pos, results.pose_landmarks.landmark))
        
        # Display the frame
        cv2.rectangle(frame, (START_BOX_x1, START_BOX_y1), (START_BOX_x2, START_BOX_y2), (255, 0, 0), 1)
        cv2.imshow('Pose Estimation', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        i += 1

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    estimate_pose2()