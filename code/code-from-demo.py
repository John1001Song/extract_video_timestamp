import cv2
import pytesseract
import re

cap = cv2.VideoCapture("../data/stamp_20240303_182801.mp4")
fps = round(cap.get(cv2.CAP_PROP_FPS))
print('fps:', fps)
frame_num = 0

NTH_SECONDS = 1

while cap.isOpened():
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
    print("Frame {} @ {}s".format(frame_num, secs))
    # hard code the area of timestamp
    # (0,0) is at top left corner,
    # x-direction: left to right
    # y-direction: top to bottom
    x, y, w, h = 30, 1150, 400, 50
    timestamp_crop = frame[y: y + h, x: x + w]
    cv2.imshow('timestamp', timestamp_crop)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
    #
    # timestamp_grey = cv2.cvtColor(timestamp_crop, cv2.COLOR_BGR2GRAY)
    # _, timestamp_thresh = cv2.threshold( \
    #   timestamp_grey, 127, 255, cv2.THRESH_BINARY)
    # cv2.imshow('thresholded timestamp', timestamp_thresh)
    #
    # candidate_str = pytesseract.image_to_string(timestamp_thresh,\
    #     config='--psm 7 outputbase digits')
    # regex_str = '[123]?\d{1}\.1?\d{1}\.19[89]\d{1}'
    #
    # if bool(re.match(regex_str, candidate_str)):
    #     print("** Timestamp @ {}s = {}".format(secs, candidate_str))
  else: # no frames left in video
    break

cap.release()
cv2.destroyAllWindows()