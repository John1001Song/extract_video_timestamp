import cv2
import os
import argparse

def resize_images_in_folder(source_folder_path, target_folder_path, target_width, target_height):
    # Ensure target folder exists
    os.makedirs(target_folder_path, exist_ok=True)
    
    # Iterate over all files in the folder
    for filename in os.listdir(source_folder_path):
        if filename.endswith(('.jpg', '.jpeg', '.png')):  # Adjust file extensions as needed
            image_path = os.path.join(source_folder_path, filename)
            # Load the original image
            image = cv2.imread(image_path)
            if image is None:
                print(f"Error: Cannot read image file '{image_path}'")
                continue

            # Resize the image
            resized_image = cv2.resize(image, (target_width, target_height), interpolation=cv2.INTER_AREA)

            # Save the resized image to the target folder
            resized_image_path = os.path.join(target_folder_path, filename)
            cv2.imwrite(resized_image_path, resized_image)

            print(f"Resized and saved image: {resized_image_path}")

def main():
    parser = argparse.ArgumentParser(description='Resize images in a folder from 1920x1080 to 1600x900.')
    parser.add_argument('--source_folder_path', type=str, required=True, help='Path to the folder containing images to resize')
    parser.add_argument('--target_folder_path', type=str, required=True, help='Path to the folder to save resized images')
    args = parser.parse_args()

    # Target resolution (1600x900)
    target_width = 1600
    target_height = 900

    # Resize images in the provided folder
    resize_images_in_folder(args.source_folder_path, args.target_folder_path, target_width, target_height)

if __name__ == "__main__":
    main()
