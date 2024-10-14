import cv2
import pytesseract
import re
import os
from tqdm import tqdm
import datetime

# Paths for video and saving results
video_folder = '../data/video/'
output_folder = '../data/output/right_camera/'
frame_interval = 1  # Extract one frame every frame
save_frame_path = output_folder
save_timestamp_path = "../data/output/right_raw_timestamps/"

# Ensure save directories exist
os.makedirs(save_frame_path, exist_ok=True)
os.makedirs(save_timestamp_path, exist_ok=True)

# Video file and output file paths
video = os.path.join(video_folder, "right_camera.mp4")
timestamp_file_path = os.path.join(save_timestamp_path, "timestamps.txt")
utc_file_path = os.path.join(save_timestamp_path, "UTC.txt")

def extract_frames():
    # Open output files for appending data
    with open(timestamp_file_path, 'a+') as tp_file, open(utc_file_path, 'a+') as utc_file:
        # Open video capture
        cap = cv2.VideoCapture(video)
        if not cap.isOpened():
            print(f"Error: Cannot open video file '{video}'")
            exit(1)

        fps = round(cap.get(cv2.CAP_PROP_FPS))
        print('fps:', fps)

        frame_num = 0
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Progress bar for frame processing
        for _ in tqdm(range(frame_count), desc="Processing frames"):
            frame_exists, frame = cap.read()
            
            if not frame_exists:
                break

            # Hardcode the area of the timestamp (cropping coordinates)
            x, w, y, h = 0, 510, 1018, 100  # Crop area from the left bottom corner
            timestamp_crop = frame[y: y + h, x: x + w]

            # Show the cropped area
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
            
            # Extract timestamp from OCR output if available
            if len(candidate_str) >= 1:
                raw_timestamp = candidate_str[0]
                
                # Convert the raw timestamp to a UTC datetime object if possible
                try:
                    timestamp_dt = datetime.datetime.strptime(raw_timestamp, "%d/%m/%Y %H:%M:%S")
                    timestamp_utc = timestamp_dt.astimezone(datetime.timezone.utc)
                    utc_str = timestamp_utc.strftime("%Y-%m-%d %H:%M:%S %Z")
                except ValueError:
                    utc_str = "N/A"
            else:
                raw_timestamp, utc_str = "N/A", "N/A"

            # Save timestamp and UTC timestamp to files
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

# Call the function to extract frames and timestamps
extract_frames()