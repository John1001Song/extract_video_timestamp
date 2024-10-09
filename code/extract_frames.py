import cv2
import os
import glob

def extract_frames(video_path, output_folder, frame_interval=30):
    """
    Extract frames from a video file.

    Args:
    - video_path (str): Path to the input video file.
    - output_folder (str): Folder where the extracted frames will be saved.
    - frame_interval (int): Interval between frames to be saved. Default is 30.

    Returns:
    None
    """
    # Create output folder if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}.")
        return
    
    frame_count = 0
    extracted_count = 0
    video_basename = os.path.basename(video_path).split('.')[0]  # Get the base name without extension

    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # Save the frame if it is at the specified interval
        if frame_count % frame_interval == 0:
            frame_filename = os.path.join(output_folder, f"{video_basename}_frame_{extracted_count:04d}.jpg")
            cv2.imwrite(frame_filename, frame)
            print(f"Saved frame {extracted_count} to {frame_filename}")
            extracted_count += 1
        
        frame_count += 1
    
    cap.release()
    print(f"Finished extracting {extracted_count} frames from the video {video_path}.")

# Usage example
video_folder = '../data/video_for_calibration/'
output_folder = '../data/output/calibration_horizontal_frames/'
frame_interval = 10  # Extract one frame every 10 frames

# Find all MP4 files in the directory
video_files = glob.glob(os.path.join(video_folder, 'TimeVideo_20241008_132618.mp4'))

# Extract frames from each video file
for video_file in video_files:
    extract_frames(video_file, output_folder, frame_interval)