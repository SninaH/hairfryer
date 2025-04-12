import cv2
import numpy as np
import matplotlib.pyplot as plt
# import pandas as pd
from get_subimage import get_subimage 
from image_to_number import get_number, light_type



# df = pd.DataFrame(columns=['frame', 'zaporedni met', 'steza', 'podrti v metu', 'podrti na stezi'])
# for frame in ["images/tiny/frame0.jpg", "images/tiny/frame300.jpg",
#               "images/medium/frame25200.jpg"]:
# get list of files in directory
import os
from os import listdir
from os.path import isfile, join

def get_raw_data_from_frame(frame_path):
    
    size = 8
            
    fileds = [  (729, 144, 27, 23, "int"),# zaporedni met 3. steza
                (805, 145, 19, 22, "int"),# podrti v metu
                (857, 145, 43, 22, "int"), # podrti skupaj
                
                (812, 44, size, size, "bool"), #1
                (775,63, size, size, "bool"), #2
                (848,64, size, size, "bool"), #3
                (737, 81, size, size, "bool"), #4
                (812,83, size, size, "bool"), #5
                (886,83, size, size, "bool"), #6
                (774,100, size, size, "bool"), #7
                (850, 103, size, size,"bool"), #8
                (811,120, size, size,"bool") #9
    ]
                

    frame_values = []
    for field in fileds:
        x,y,w,h,type =field
        subimg = get_subimage(frame_path, x,y,w,h)
        if type == "bool":
            number = light_type(subimg)
        elif type == "int":
            number = get_number(subimg)
        frame_values.append( number )
    
    # print(frame_values[3])
    # print(frame_values[4], frame_values[5])
    # print(frame_values[6], frame_values[7], frame_values[8])
    # print(frame_values[9], frame_values[10])
    # print(frame_values[11])
    
    # img = cv2.imread(frame_path)
    # plt.imshow(img)
    # plt.show()
    return frame_values

def merge_data_from_frames(values):
    
    cleaned_values = dict()
    cleaned_values[0]  = [0, 0, 0,  0,0,0,0,0,0,0,0,0]
    cumulative_sum = 0
    ciscenje_stojijo = None
    prev_met = -1
    for i in range(1,len(values)):
        # met, _, _ = values[i]  
        met = values[i][0]
        
        if met == 16:
            ciscenje_stojijo = 9
        
        if met > 0:
            if prev_met != met:
                print("NOV MET")
                prev_podrti = cleaned_values[prev_met][1]
                cumulative_sum += prev_podrti
                if ciscenje_stojijo:
                    ciscenje_stojijo -= prev_podrti
                    if ciscenje_stojijo == 0:
                        ciscenje_stojijo = 9
            
            # met, podrti, skupaj = values[i]
            met = values[i][0]
            podrti = values[i][1]
            skupaj = values[i][2]
            lucke = values[i][3:]
            stojece_lucke = 9 - sum(lucke)
            if ciscenje_stojijo is not None:
                podrti_lucke = ciscenje_stojijo - stojece_lucke
            else:
                podrti_lucke = 9 - stojece_lucke
            print(f"met: {met}, podrti: {podrti}, skupaj: {skupaj}")
            diff = skupaj - cumulative_sum
            
            # if cumulative_sum + podrti == skupaj:
            if diff == podrti_lucke or podrti == podrti_lucke:
                cleaned_values[met] = [met, podrti_lucke, skupaj, *lucke]
                print("OK")
            elif diff == podrti and (met not in cleaned_values):
                cleaned_values[met] = [met, podrti, skupaj, None]
                print(lucke)
                print("OK None")
                
            else:
                print("!=")
                print("diff: ", diff)
                print("podrti: ", podrti)
                print("podrti_lucke:", podrti_lucke)
            
            
        prev_met = met
    return cleaned_values

            
        
    

def get_data_from_frames(path):
    # values = dict()
    values = []
    frames = [f for f in listdir(path) if isfile(join(path, f))]
    frames.sort()
    print(frames)
    for frame in frames:
    
        frame_path = path + frame
        print("Frame: ", frame, frame_path)
       
        value = get_raw_data_from_frame(frame_path)
        values.append(value)
        
    # filetered_values = dict()
    # for frame, frame_values in values.items():
    #     filtered_values[frame] = []
        
    for frame, frame_values in zip(frames, values):
        print(f"Frame: {frame}")
        for number in frame_values:
            print(f"{number} ", end=" ")
        print()
    
    return values
    
        
if __name__ == "__main__":
    video_name = "E_ZRXdJrRG4"
    input_path = "data/images/"
    values = get_data_from_frames(input_path + video_name + "/")
    cleaned_data =  merge_data_from_frames(values)
    print("Cleaned data:")
    for met, values in cleaned_data.items():
        print(f"{met}: {values}")
    # get_raw_data("images/tiny/")
    # get_raw_data("images/large/")
    # get_raw_data("images/large2/")