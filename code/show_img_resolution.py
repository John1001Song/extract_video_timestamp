import cv2
import os
import argparse

def show_image_resolution(image_path):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Cannot open image file '{image_path}'")
        return

    # Get image dimensions
    height, width, channels = image.shape
    print(f"Image Resolution: {width}x{height} (Width x Height) - File: {os.path.basename(image_path)}")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Show image resolutions in a folder.')
    parser.add_argument('--folder_path', type=str, required=True, help='Path to the folder containing images')
    args = parser.parse_args()

    folder_path = args.folder_path

    # Check if the provided path exists and is a directory
    if not os.path.isdir(folder_path):
        print(f"Error: The provided folder path '{folder_path}' does not exist or is not a directory.")
        return

    # Iterate over all images in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
            image_path = os.path.join(folder_path, filename)
            show_image_resolution(image_path)

if __name__ == "__main__":
    main()
