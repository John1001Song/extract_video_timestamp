import cv2
import pytesseract
import re
import os
from tqdm import tqdm


path = "/Users/js/Documents/GitHub/extract_video_timestamp/data/video/"
save_frame_path = "../results/raw_frames/"
save_timestamp_path = "../results/raw_timestamps/"
save_GPS_path = "../results/raw_gps/"



os.chdir(path)

tp_file = open(save_timestamp_path+"timestamps.txt", 'a+')
gps_file = open(save_GPS_path+"gps.txt", 'a+')

# video = "TimeVideo_20240307_113053.mp4"
video = "TimeVideo_20240314_123607.mp4"
# video = "TimeVideo_20240314_123607_10sec.mp4"
cap = cv2.VideoCapture(video)
fps = round(cap.get(cv2.CAP_PROP_FPS))
print('fps:', fps)
frame_num = 0

progress_bar = iter(tqdm(range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))))

NTH_SECONDS = 1
idx = 0
while cap.isOpened():
  next(progress_bar)
  frame_exists, frame = cap.read()
  frame_num += 1

  # test code check if the video is complete
  # print('frame_exists:', frame_exists)
  # print('frame:', frame)
  # if frame_exists:
  #   cv2.imshow('frame:', frame)
  #   cv2.waitKey(1)
  # else:
  #   break

  # if frame_exists and frame_num % (fps * NTH_SECONDS) == 0:
  if frame_exists:
    # secs = round(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)
    secs = (cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)
    # print("Frame {} @ {}s".format(frame_num, secs))
    # hard code the area of timestamp
    # (0,0) is at top left corner,
    # x-direction: left to right
    # y-direction: top to bottom
    # x, w, y, h = 0, 725, 1130, 100
    x, w, y, h = 0, 725, 975, 1000
    timestamp_crop = frame[y: y + h, x: x + w]
    # cv2.imshow('timestamp', timestamp_crop)
    # cv2.imshow('original', frame)
    cv2.imwrite(save_frame_path+'raw'+str(idx)+'.png', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
    #
    # timestamp_grey = cv2.cvtColor(timestamp_crop, cv2.COLOR_BGR2GRAY)
    # _, timestamp_thresh = cv2.threshold( \
    #   timestamp_grey, 127, 255, cv2.THRESH_BINARY)
    # cv2.imshow('thresholded timestamp', timestamp_thresh)
    #
    candidate_str = pytesseract.image_to_string(timestamp_crop,
                                                config='--psm 6 -c tessedit_char_whitelist="NW0123456789/.: "')
        # config='--psm 7 outputbase digits')
    # print('raw candidate_str:', candidate_str)
    raw_timestamp = candidate_str.split("\n")[0]
    raw_location = candidate_str.split("\n")[1]
    # print('raw_timestamp:', raw_timestamp)
    # print('raw_location:', raw_location)
    tp_file.write(raw_timestamp+"\n")
    gps_file.write(raw_location+"\n")
    # no frames left in video
  else:
    break
  idx+=1


cap.release()
cv2.destroyAllWindows()
tp_file.close()
gps_file.close()