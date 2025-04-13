import cv2


def combine_comparison(filename1, filename2):
    # Create VideoCapture objects
    cap1 = cv2.VideoCapture(filename1)
    cap2 = cv2.VideoCapture(filename2)

    # Get video properties for video1
    width1 = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
    height1 = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps1 = cap1.get(cv2.CAP_PROP_FPS)
    frames1 = int(cap1.get(cv2.CAP_PROP_FRAME_COUNT))

    # Get video properties for video2
    width2 = int(cap2.get(cv2.CAP_PROP_FRAME_WIDTH))
    height2 = int(cap2.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps2 = cap2.get(cv2.CAP_PROP_FPS)
    frames2 = int(cap2.get(cv2.CAP_PROP_FRAME_COUNT))

    # Determine target width
    target_width = min(width1, width2)

    # Calculate new height for video2 if resizing is needed
    if width2 != target_width:
        new_height2 = int(height2 * (target_width / width2))
    else:
        new_height2 = height2

    new_height2 = int(new_height2/2)

    fps = 15

    # Initialize VideoWriter with the combined height
    total_height = height1 + new_height2
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('outputs_examples/output_all.mp4', fourcc, fps, (target_width, total_height))

    # Read frames and process them
    while True:
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        if not ret1 or not ret2:
            break
        
        # Resize frame2 to target_width
        if width2 != target_width:
            frame2 = cv2.resize(frame2, (target_width, new_height2))

        # Stack the frames vertically
        combined_frame = cv2.vconcat([frame1, frame2])

        # Write the combined frame to the output video
        out.write(combined_frame)

    # Release the VideoCapture and VideoWriter objects
    cap1.release()
    cap2.release()
    out.release()

    # Close all windows
    cv2.destroyAllWindows()

if __name__ == '__main__':
    combine_comparison('outputs_examples/output_comparison.mp4', 'outputs_examples/output_distances.mp4')