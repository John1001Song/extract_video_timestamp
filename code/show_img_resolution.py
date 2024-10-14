import cv2
import os

def show_image_resolution(image_path):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Cannot open image file '{image_path}'")
        return

    # Get image dimensions
    height, width, channels = image.shape
    print(f"Image Resolution: {width}x{height} (Width x Height) - File: {os.path.basename(image_path)}")

# Example usage for showing image resolution for all images in a folder
# kitti_folder_path = '/home/js/Documents/GitHub/extract_video_timestamp/data/camera_to_kitti/test_imgs/'
kitti_folder_path = '/home/js/Documents/GitHub/extract_video_timestamp/data/kitti/image_2'


# Iterate over all images in the folder
for filename in os.listdir(kitti_folder_path):
    if filename.endswith('.png'):
        image_path = os.path.join(kitti_folder_path, filename)
        show_image_resolution(image_path)