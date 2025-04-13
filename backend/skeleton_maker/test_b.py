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


def estimate_pose(name1, name2):
    # Initialize Pose Estimation
    mp_pose = mp.solutions.pose
    #pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    pose = mp_pose.Pose()

    # Open video file
    reader1 = cv2.VideoCapture(name1)
    reader2 = cv2.VideoCapture(name2)

    width = int(reader1.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(reader1.get(cv2.CAP_PROP_FRAME_HEIGHT))

    have_more_frame = True

    while have_more_frame:
        h1, frame1 = reader1.read()
        h2, frame2 = reader2.read()
        have_more_frame = h1 and h2

        frame1 = cv2.resize(frame1, (width//2, height//2))
        frame2 = cv2.resize(frame2, (width//2, height//2))
        img = np.hstack((frame1, frame2))

        
        results1 = pose.process(frame1)
        results2 = pose.process(frame2)
        
        if results1.pose_landmarks:
            mp_drawing = mp.solutions.drawing_utils
            mp_drawing.draw_landmarks(img[:,:width//2], results1.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        if results2.pose_landmarks:
            mp_drawing = mp.solutions.drawing_utils
            mp_drawing.draw_landmarks(img[:,width//2:], results2.pose_landmarks, mp_pose.POSE_CONNECTIONS)



        # Display the frame
        cv2.imshow('', img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    estimate_pose('good.mp4', 'bad.mp4')