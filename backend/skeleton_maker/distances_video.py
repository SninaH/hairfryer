import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2


def create_distances_video(filename1, filename2):
    skeleton0_files = sorted(glob.glob(filename1))
    skeleton1_files = sorted(glob.glob(filename2))


    # Ensure the number of files matches
    print(len(skeleton0_files))
    print(len(skeleton1_files))
    assert len(skeleton0_files) == len(skeleton1_files), "Number of CSV files for skeleton_0 and skeleton_1 must match"

    # Initialize a list to store all distances
    all_distances = []

    # Process each pair of CSV files
    for i, (skel0_file, skel1_file) in enumerate(zip(skeleton0_files, skeleton1_files)):
        print(i)

        # Read the CSV files
        skel0_data = pd.read_csv(skel0_file, header=None)
        skel1_data = pd.read_csv(skel1_file, header=None)

        # Extract the first three columns
        skel0_coords = skel0_data.iloc[:, :3].values
        skel1_coords = skel1_data.iloc[:, :3].values

        # Calculate L2 distances between corresponding rows
        distances = np.linalg.norm(skel0_coords - skel1_coords, axis=1)
        distance = np.average(distances)

        # Append distances to the list
        all_distances.append(distance)


    # Create a directory for the output images
    output_dir = 'graph_frames'
    os.makedirs(output_dir, exist_ok=True)

    # Initialize a list to store frame filenames
    frame_files = []

    # Plot each frame's distance and cumulative data
    for i, distance in enumerate(all_distances):
        print(i)
        plt.figure(figsize=(10, 6))

        # Plot current distance
        #plt.plot(i, distance, 'ro', markersize=10)

        # Plot cumulative average
        #cumulative_avg = np.mean(all_distances[:i+1])
        #val = all_distances[i]
        plt.plot([j for j in range(i)], all_distances[:i], '-o', markersize=10)
        plt.xlim([-2,64])
        plt.ylim([-0.1, 0.7])

        # Set labels and title
        plt.xlabel('Frame Number')
        plt.ylabel('L2 Distance')
        plt.title(f'L2 Distance and Cumulative Average at Frame {i+1}')
        plt.legend()

        # Save the plot as a PNG file
        frame_filename = os.path.join(output_dir, f'frame_{i:04d}.png')
        plt.savefig(frame_filename)
        frame_files.append(frame_filename)

        # Close the plot to free memory
        #plt.close()


    # Set video parameters
    output_video = 'distance_graphs3.mp4'
    fps = 15  # Frames per second
    frame_size = (640, 480)  # Adjust based on your images

    # Create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video, fourcc, fps, frame_size)

    # Read each frame image and write to video
    for i,frame_file in enumerate(frame_files):
        print(i)
        img = cv2.imread(frame_file)
        # Resize if necessary
        img = cv2.resize(img, frame_size)
        out.write(img)

    # Release the VideoWriter
    out.release()

if __name__ == '__main__':
    create_distances_video('outputs_examples/skeleton1_0_*.csv', 'outputs_examples/skeleton2_0_*.csv')