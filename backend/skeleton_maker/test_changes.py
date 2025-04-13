import cv2
import numpy as np
import time
import torch
import cv2
import matplotlib.pyplot as plt
from torchvision import transforms
import timm
import mediapipe as mp


def test_changes():
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    # Read the video
    cap = cv2.VideoCapture('movie.mp4')

    preprocess = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    def get_keypoints(heatmaps, threshold=0.2):
        keypoint_coords = []
        for heatmap in heatmaps:
            heatmap = heatmap.cpu().numpy()
            heatmap = np.squeeze(heatmap)
            
            max_val = heatmap.max()
            if max_val > threshold:
                y, x = np.unravel_index(np.argmax(heatmap), heatmap.shape)
                keypoint_coords.append((x, y))
            else:
                keypoint_coords.append((0, 0))  # No detection
        return keypoint_coords

    # Define the ROI (e.g., center of the video)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    '''ROI_x1 = 370#width // 2 - 100
    ROI_y1 = 22#height // 2 - 100
    ROI_x2 = 455#width // 2 + 100
    ROI_y2 = 65#height // 2 + 100'''

    # one light (speciifc)
    ROI_x1 = 405
    ROI_y1 = 21
    ROI_x2 = 412
    ROI_y2 = 29

    # number (1st)
    #ROI_x1 = 370
    #ROI_y1 = 75
    #ROI_x2 = 377
    #ROI_y2 = 85

    PBOX_x1 = 330
    PBOX_y1 = 180
    PBOX_x2 = 490
    PBOX_y2 = 355


    last_pose_landmarks = None

    def light_type(subimage, brightness_threshold=0.66):
        """
            subimage: cv2
            return: 1 if light is bright and 0 else
        """
        gray = cv2.cvtColor(subimage, cv2.COLOR_BGR2GRAY)

        mean_brightness = cv2.mean(gray)[0]
        normalized_brightness = mean_brightness / 255.0

        return int(normalized_brightness >= brightness_threshold)#, normalized_brightness



    def estimate_brightness(image):
        # Calculate the average pixel value
        mean_brightness = cv2.mean(image)[0]

        # Normalize the brightness measure (optional)
        normalized_brightness = mean_brightness / 255.0
        
        return normalized_brightness

    #ROI2_

    # Initialize variables
    ret, prev_frame = cap.read()
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    prev_roi = prev_gray[ROI_y1:ROI_y2, ROI_x1:ROI_x2]

    threshold = 5


    # initial brightness
    brightness = None
    brightness_threshold = 0.6

    i = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        l_type = light_type(frame[ROI_y1:ROI_y2, ROI_x1:ROI_x2])
        #print(l_type)


        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        sub_frame_rgb = frame_rgb[PBOX_y1:PBOX_y2,PBOX_x1:PBOX_x2]

        if i % 10 == 0:
            results = pose.process(sub_frame_rgb)

            #def transform_coordinates(pose_landmarks):


            # Draw pose landmarks
            if results.pose_landmarks:
                mp_drawing = mp.solutions.drawing_utils
                #mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                mp_drawing.draw_landmarks(frame[PBOX_y1:PBOX_y2,PBOX_x1:PBOX_x2], results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                #mp_drawing.draw_landmarks(sub_frame_rgb, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                last_pose_landmarks = results.pose_landmarks

                #cv2.rectangle(frame, (PBOX_x1, PBOX_y1), (PBOX_x2, PBOX_y2), (255, 0, 0), 5)
        else:
            if last_pose_landmarks:
                mp_drawing = mp.solutions.drawing_utils
                mp_drawing.draw_landmarks(frame[PBOX_y1:PBOX_y2,PBOX_x1:PBOX_x2], results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                

        
        '''
        input_tensor = preprocess(frame_rgb).unsqueeze(0)
        # Perform pose estimation
        #with torch.no_grad():
        #    outputs = model(input_tensor)
        
        # Get key points
        #keypoint_coords = get_keypoints(outputs)
        
        # Visualize the pose on the original frame
        #for coord in keypoint_coords:
        #    x, y = coord
        #    if x != 0 and y != 0:  # Only draw if detected
        #        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
        
        # Display the frame
        #cv2.imshow('Pose Estimation', frame)'''
        
        
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Extract ROI
        current_roi = gray[ROI_y1:ROI_y2, ROI_x1:ROI_x2]
        #print(f"brightness: {brightness}")
        #print(estimate_brightness(current_roi))
        
        if brightness is None:
            brightness = (estimate_brightness(current_roi) > brightness_threshold)
        if brightness and estimate_brightness(current_roi) < brightness_threshold:
            print("DOWN")
            brightness = not brightness
        if not brightness and estimate_brightness(current_roi) > brightness_threshold:
            print("UP")
            brightness = not brightness
        #print(estimate_brightness(current_roi))
        
        # Compute absolute difference
        diff = cv2.absdiff(current_roi, prev_roi)
        
        # Calculate the mean of the difference
        mean_diff = np.mean(diff)
        #print(mean_diff)
        time.sleep(0.02)
        
        # If mean_diff exceeds threshold, mark as change
        if mean_diff > threshold:
            #print("Change detected!")
            # Draw a red bounding box around the ROI
            cv2.rectangle(frame, (ROI_x1, ROI_y1), (ROI_x2, ROI_y2), (0, 255, 0), 1)
        else:
            cv2.rectangle(frame, (ROI_x1, ROI_y1), (ROI_x2, ROI_y2), (0, 0, 255), 1)    
        # Display the frame
        cv2.imshow('Video', frame)
        
        # Update previous ROI
        prev_roi = current_roi.copy()
        
        # Break if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        i += 1

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    test_changes()