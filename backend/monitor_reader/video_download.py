
    
# yt-dlp https://www.youtube.com/watch?v=i2scvOaaB-Q&t=1s&ab_channel=KKOgrajcaLjubljana

import subprocess

def download_video(url, output_path):
    with open(output_path + "downloaded_videos.txt", "r", encoding="utf-8") as file:
        downloaded_videos = file.read().splitlines()
        if url in downloaded_videos:
            print(f"Video {url} already downloaded.")
        else:
            print(f"Downloading video {url}...")
            subprocess.run(["yt-dlp", url, "-P", output_path, "-o","%(id)s",
                            "--merge-output-format", "mkv", "--no-post-overwrites",
                            "--no-continue", "--no-check-certificate"])
            # Download the video using yt-dlp
            with open(output_path + "downloaded_videos.txt", "a", encoding="utf-8") as file:
                file.write(url + "\n")
                
if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=i2scvOaaB-Q&t=1s&ab_channel=KKOgrajcaLjubljana"
    url = "https://www.youtube.com/watch?v=5d5lt6ek9YM&ab_channel=AronChupa%26LittleSisNora"
    url = "https://www.youtube.com/shorts/lrBFiM8n96E"
    url = "https://www.youtube.com/watch?v=E_ZRXdJrRG4&ab_channel=WiloPolis"
    download_video(url,"data/videos/")
    
