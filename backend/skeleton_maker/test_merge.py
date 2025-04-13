import cv2
import glob

def merge():
    # Read all PNG files for person1 and person2
    person1_frames = sorted(glob.glob('outputs_examples/person1_*.png'))
    person2_frames = sorted(glob.glob('outputs_examples/person2_*.png'))

    # Ensure both sequences have the same number of frames
    assert len(person1_frames) == len(person2_frames), "Frame counts must match"

    # Get the first frame to determine dimensions
    first_frame_p1 = cv2.imread(person1_frames[0])
    first_frame_p2 = cv2.imread(person2_frames[0])

    # Check if images are of the same height
    assert first_frame_p1.shape[0] == first_frame_p2.shape[0], "Images must have the same height"

    # Combine frames horizontally
    combined_frames = []
    for p1, p2 in zip(person1_frames, person2_frames):
        img1 = cv2.imread(p1)
        img2 = cv2.imread(p2)
        combined = cv2.hconcat([img1, img2])
        combined_frames.append(combined)

    # Create output video
    output_path = 'output.mp4'
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 30  # Adjust as needed
    height, width = combined_frames[0].shape[:2]
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for frame in combined_frames:
        out.write(frame)

    out.release()

if __name__ == '__main__':
    merge()