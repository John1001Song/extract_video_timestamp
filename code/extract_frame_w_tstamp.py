import cv2
import pytesseract
import re
import os
from tqdm import tqdm
import datetime
import argparse

def main():
    # Define the argument parser to get command-line arguments
    parser = argparse.ArgumentParser(description="Extract frames and timestamps from video.")
    parser.add_argument('--video_folder', type=str, required=True, help='Path to the folder containing video files.')
    parser.add_argument('--output_folder', type=str, required=True, help='Path to the folder to save output frames and timestamps.')
    parser.add_argument('--frame_interval', type=int, default=5, help='Interval of frames to process (default is 5).')
    args = parser.parse_args()

    # Paths for video and saving results
    video_folder = args.video_folder
    output_folder = args.output_folder
    frame_interval = args.frame_interval

    # Iterate over all video files in the video folder
    for video_file in os.listdir(video_folder):
        if video_file.endswith(('.mp4', '.avi', '.mov')):
            video_path = os.path.join(video_folder, video_file)
            video_output_folder = os.path.join(output_folder, os.path.splitext(video_file)[0])
            save_frame_path = os.path.join(video_output_folder, 'frames')
            save_timestamp_path = os.path.join(video_output_folder, 'timestamps')

            # Ensure save directories exist
            os.makedirs(save_frame_path, exist_ok=True)
            os.makedirs(save_timestamp_path, exist_ok=True)

            # Output file paths
            timestamp_file_path = os.path.join(save_timestamp_path, "timestamps.txt")
            utc_file_path = os.path.join(save_timestamp_path, "UTC.txt")

            extract_frames(video_path, save_frame_path, timestamp_file_path, utc_file_path, frame_interval)

def extract_frames(video, save_frame_path, timestamp_file_path, utc_file_path, frame_interval):
    # Open output files for appending data
    with open(timestamp_file_path, 'a+') as tp_file, open(utc_file_path, 'a+') as utc_file:
        # Open video capture
        cap = cv2.VideoCapture(video)
        if not cap.isOpened():
            print(f"Error: Cannot open video file '{video}'")
            return

        fps = round(cap.get(cv2.CAP_PROP_FPS))
        print(f'Processing video: {video}, fps: {fps}')

        frame_num = 0
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Progress bar for frame processing
        for _ in tqdm(range(frame_count), desc="Processing frames"):
            frame_exists, frame = cap.read()

            if not frame_exists:
                break

            if frame_num % frame_interval == 0:
                # Hardcode the area of the timestamp (cropping coordinates)
                # Adjust cropping area based on frame resolution
                if frame.shape[1] == 1920 and frame.shape[0] == 1080:
                    x, w, y, h = 0, 565, 1018, 100  # Crop area for 1920x1080 10/26/2024 16:18:42.482
                    # x, w, y, h = 0, 510, 1018, 100 # Crop area for 1920x1080 10/26/24 16:18:42.482
                elif frame.shape[1] == 1600 and frame.shape[0] == 1200:
                    x, w, y, h = 0, 425, 1132, 111  # Crop area for 1600x1200
                else:
                    # Default cropping area for unexpected resolutions
                    x, w, y, h = 0, frame.shape[1] // 4, frame.shape[0] - 100, 100

                timestamp_crop = frame[y: y + h, x: x + w]

                # # Show the cropped area
                # cv2.imshow('Cropped Timestamp Area', timestamp_crop)
                # if cv2.waitKey(1) & 0xFF == ord('q'):
                #     break

                # Preprocess the cropped area to improve OCR accuracy
                timestamp_grey = cv2.cvtColor(timestamp_crop, cv2.COLOR_BGR2GRAY)
                _, timestamp_thresh = cv2.threshold(timestamp_grey, 127, 255, cv2.THRESH_BINARY)

                # OCR using pytesseract
                candidate_str = pytesseract.image_to_string(timestamp_thresh,
                                                            config='--psm 6 -c tessedit_char_whitelist="NW0123456789/.: "')
                candidate_str = candidate_str.strip().split("\n")
                # Print out the timestamp string
                # print(f'OCR Candidate String: {candidate_str}')

                # Extract timestamp from OCR output if available
                if len(candidate_str) >= 1:
                    raw_timestamp = candidate_str[0]
                    # print(f"raw_timestamp: {raw_timestamp}")
                    # Convert the raw timestamp to a UTC datetime object if possible
                    try:
                        timestamp_dt = datetime.datetime.strptime(raw_timestamp, "%m/%d/%Y %H:%M:%S.%f") # for 10/26/2024 16:18:38.127
                        # timestamp_dt = datetime.datetime.strptime(raw_timestamp, "%m/%d/%y %H:%M:%S.%f") # for 10/26/24 16:18:38.127
                        # print(f"timestamp_dt: {timestamp_dt}")
                        timestamp_utc = timestamp_dt.astimezone(datetime.timezone.utc)
                        utc_str = timestamp_utc.strftime("%Y-%m-%dT%H:%M:%S.%fZ") # Format to ISO 8601 with 3 digits for milliseconds
                        # print(utc_str)
                    except ValueError:
                        raw_timestamp, utc_str = "N/A", "N/A"
                else:
                    raw_timestamp, utc_str = "N/A", "N/A"

                # Save timestamp and UTC timestamp to files if the timestamp is valid
                if raw_timestamp != "N/A":
                    tp_file.write(raw_timestamp + "\n")
                    utc_file.write(utc_str + "\n")

                    # Save the frame using the timestamp as the filename (replace invalid characters if necessary)
                    frame_filename = os.path.join(save_frame_path, f'{raw_timestamp.replace("/", "-").replace(":", "-")}.png')
                    cv2.imwrite(frame_filename, frame)

            frame_num += 1

        # Release the video capture object
        cap.release()

    # Destroy all OpenCV windows (if any were used)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
