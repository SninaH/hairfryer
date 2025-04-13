# hairfryer
Dragonhack 2025 team Hairfryer's solution

We developed a solution for video data extraction in sport, namely bowling. We extract data about hit pins from monitor generating a report. This mode is useful both for the referee, that has to keep track of the match score, as well as for the players and coaches that want to have detailed statistics about performance across multiple matches.

On the other hand pose estimator (skeleton model) is applied to enable comparison between individual throws and among different players. This mode serves as a smart tool to help coach track their player's behavior change throughout the season, as per example are speed and hand posture.

Streaming of the nine-pin bowling matches across Youtube is mandatory in Slovenia for two years now. Such extraction is platform ignorant, and therefore suitable to use on any bowling ally.

Our web app consist of fast API backend, where OCR and skeleton creation via mediapipe libray are performed, and of intuitive angular frontend that enables a quick adoption of the tool to anyone. All you need is to provide the app with the url of the match Youtube video and confirm the field locations. For the posture comparison the data is automatically split for you into individual throws, and difference through time is neatly plotted as a time-difference graph.

On the first page the user enters the link to the youtube video of the match.
![Screenshot from 2025-04-13 11-52-24](https://github.com/user-attachments/assets/b2363903-f6db-466f-9ec0-14923219de56)

Then the user checks that the annotation of the areas with pin information is correct. When pressing done, the server processes the video.

![Screenshot from 2025-04-13 11-50-41](https://github.com/user-attachments/assets/d490a3f4-6bc8-40e9-80a6-61ee96e8d758)
![Screenshot from 2025-04-13 11-49-59](https://github.com/user-attachments/assets/de6f4edd-83e3-48dd-ad8a-a8e535afeee3)

![Screenshot from 2025-04-13 11-49-31](https://github.com/user-attachments/assets/1182b668-7903-48c1-b19c-674db3377016)

![Screenshot from 2025-04-13 11-51-15](https://github.com/user-attachments/assets/345f59c1-7990-487b-a7c0-061f24a98e58)

The user is first redirected to the page with the report of the scores of the chosen player.

![Screenshot from 2025-04-13 11-50-58](https://github.com/user-attachments/assets/78f603e1-547f-4b4f-84ef-739bd92382ce)

When the user presses "Switch to Coach" the video with skeleton of players comparison is displayed.





