import glob
import os


def rename_skeletons(source_all, pattern1, pattern2):
    # Define the source pattern
    source_pattern = source_all

    # Get all files matching the pattern
    files = glob.glob(source_pattern)

    for old_filename in files:
        try:
            # Construct the new filename
            new_filename = old_filename.replace(pattern1, pattern2)

            # Check if the new file already exists
            if os.path.exists(new_filename):
                print(f"File {new_filename} already exists. Skipping.")
                continue
            
            # Rename the file
            os.rename(old_filename, new_filename)
            print(f"Renamed {old_filename} to {new_filename}")
        except Exception as e:
            print(f"Error renaming {old_filename}: {e}")

if __name__ == '__main__':
    rename_skeletons("outputs_examples/skeleton_0_*.csv", "skeleton_0_", "skeleton2_0_")