import cv2
import os



def video_to_images(video_name, video_format, input_path, output_path, every_n_seconds =10):
    vidcap = cv2.VideoCapture(f'{input_path}{video_name}.{video_format}')
    count = 0
    success = True
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))
    print(fps)
    while success:
        success,image = vidcap.read()
        if count%(every_n_seconds*fps) == 0 :
            path = output_path+video_name+'/frame%d.jpg'%count
            print(path)
            # check if the directory exists
            if not os.path.exists(output_path+video_name):
                os.makedirs(output_path+video_name)
                print(f"Directory {output_path+video_name} created")
            cv2.imwrite(path,image)
            # print('successfully written 10th frame')
        count+=1
        
        
if __name__ == "__main__":
    # name = "tiny"
    # video_format = "mp4"

    # name = "short"
    # video_format = "mkv"

    # name = "medium"
    # format = "mkv"
    
    name = "E_ZRXdJrRG4"
    format = "mkv"
    
    video_to_images(name, format, 
                    input_path = "data/videos/",
                    output_path="data/images/")
