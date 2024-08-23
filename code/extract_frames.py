import cv2
import os

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
        print("Error: Could not open video.")
        return
    
    frame_count = 0
    extracted_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # Save the frame if it is at the specified interval
        if frame_count % frame_interval == 0:
            frame_filename = os.path.join(output_folder, f"frame_{extracted_count:04d}.jpg")
            cv2.imwrite(frame_filename, frame)
            print(f"Saved frame {extracted_count} to {frame_filename}")
            extracted_count += 1
        
        frame_count += 1
    
    cap.release()
    print(f"Finished extracting {extracted_count} frames from the video.")

# Usage example
video_path = '../data/video_for_frames_only/TimeVideo_20240822_114913.mp4'
output_folder = '../data/output/frames_only/'
frame_interval = 30  # Extract one frame every 30 frames
extract_frames(video_path, output_folder, frame_interval)
