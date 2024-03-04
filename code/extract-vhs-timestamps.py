import pytesseract
import cv2
import sys
import re
import datetime

####
# To run, pipe output to a csv:
#
#   $ python3 extract-timestamps.py file1.mov file2.mov > timestamps.csv
#
# Output will be:
#
#  file,timestamp,hhmmss,sec
#  file1.mov,15.10.1993,0:02:25,145
#  file1.mov,15.10.1993,0:02:30,150
#  file1.mov,15.10.1993,0:02:55,175
#  file1.mov,15.10.1993,0:03:00,180
#
# hhmmss indicates the timestamp within the file (i.e., hhmmss) where the VHS
# timestamp was found
####

# Adjust this to capture timestamps fewer seconds
CAPTURE_AT_N_SECONDS = 5

# Adjust this to modify where the timestamp is located in the frame
TIMESTAMP_XY = (80, 460)
TIMESTAMP_SZ = (250, 50)

def extract_timestamp(frame):
    img_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, img_thresh = cv2.threshold(img_grey, 127, 255, cv2.THRESH_BINARY)
    x, y = TIMESTAMP_XY
    w, h = TIMESTAMP_SZ
    img_crop = img_thresh[y:y + h, x:x + w]

    # Uncomment to show cropped timestamp
    # cv2.imshow('crop', img_crop)

    # Uncomment to show full frame
    # cv2.imshow('full', frame)

    timestamp = pytesseract.image_to_string(img_crop, \
        config='--psm 7 outputbase digits')

    # Movies are usually in 198x--200x
    if bool(re.match('[123]?\d{1}\.1?\d{1}\.[12][90][890]\d{1}', timestamp)):
        # Parse as a proper datetime
        try:
            return datetime.datetime.strptime(timestamp, "%d.%m.%Y")
        except ValueError:
            return None
    return None

if __name__ == "__main__":
    files = sys.argv[1:]
    while len(files) > 0:
        infile = files.pop(-1)
        cap = cv2.VideoCapture(infile)
        fps = round(cap.get(cv2.CAP_PROP_FPS))
        frame_num = 0
        print('file,timestamp,hhmmss,sec')
        while (cap.isOpened()):
            frame_exists, frame = cap.read()
            if frame_exists and (frame_num % (fps * CAPTURE_AT_N_SECONDS) == 0):
                timestamp = extract_timestamp(frame)
                if timestamp is not None:
                    cap_millisecs = round(cap.get(cv2.CAP_PROP_POS_MSEC))
                    hhmmss = str(datetime.timedelta( \
                        milliseconds=cap_millisecs)).split(".")[0]
                    print("{},{},{},{}".format(\
                        infile.split('/')[-1],\
                        timestamp.strftime("%d.%m.%Y"),\
                        hhmmss,\
                        round(cap_millisecs / 1000))\
                    )
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            frame_num += 1

        cap.release()
        cv2.destroyAllWindows()