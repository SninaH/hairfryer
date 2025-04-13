import asyncio
import subprocess
import cv2
import os


async def save_youtube_video(url, output_path):
    with open(output_path + "downloaded_videos.txt", "r", encoding="utf-8") as file:
        downloaded_videos = file.read().splitlines()
        if url in downloaded_videos:
            print(f"Video {url} already downloaded.")
        else:
            print(f"Downloading video {url}...")
            subprocess.run(["yt-dlp", url, "-P", output_path, "-o", "%(id)s.mkv",
                            "-f bestvideo",
                            "--merge-output-format", "mkv", "--no-post-overwrites",
                            "--no-continue", "--no-check-certificate"])
            # Download the video using yt-dlp
            with open(output_path + "downloaded_videos.txt", "a", encoding="utf-8") as file:
                file.write(url + "\n")




async def video_to_images(video_name, video_format, input_path, output_path, every_n_seconds=5, for_frontend = False):
    vidcap = cv2.VideoCapture(f'{input_path}{video_name}.{video_format}')
    count = 0
    success = True
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))
    print('fps: ', fps, flush=True)
    while success:
        success, image = vidcap.read()
        if count % (every_n_seconds * fps) == 0:
            path = output_path + video_name + f'/frame{count:06d}.jpg'
            print(path)
            # check if the directory exists
            if not os.path.exists(output_path + video_name):
                os.makedirs(output_path + video_name)
                print(f"Directory {output_path + video_name} created")
            try:
                cv2.imwrite(path, image)
            except Exception as e:
                pass
            if for_frontend:
                break
            # print('successfully written 10th frame')
        count += 1

