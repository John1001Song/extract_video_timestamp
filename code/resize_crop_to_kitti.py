import cv2
import os

def resize_and_crop(image, target_width, target_height):
    # Get original dimensions
    h, w = image.shape[:2]
    
    # Calculate the scaling factor
    scale = max(target_width / w, target_height / h)
    new_w, new_h = int(w * scale), int(h * scale)
    
    # Resize the image
    resized_image = cv2.resize(image, (new_w, new_h))
    
    # Calculate cropping coordinates
    start_x = (new_w - target_width) // 2
    # start_y = (new_h - target_height) // 2
    start_y = (new_h - target_height) if new_h > target_height else 0    
    
    # Crop the image to the target size
    cropped_image = resized_image[start_y:start_y + target_height, start_x:start_x + target_width]
    return cropped_image

def main():
    # Input and output paths
    image_folder = '/home/js/Documents/GitHub/extract_video_timestamp/data/camera_to_kitti/test_imgs/'  # Replace with the folder containing your images
    output_folder = '/home/js/Documents/GitHub/extract_video_timestamp/data/camera_to_kitti/resized/'  # Replace with the folder to save the resized images
    
    # Ensure output directory exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Target dimensions
    target_width, target_height = 1242, 375
    
    # Iterate through all images in the folder
    for filename in os.listdir(image_folder):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_path = os.path.join(image_folder, filename)
            image = cv2.imread(image_path)
            
            if image is None:
                print(f"Error: Cannot open image file '{image_path}'")
                continue
            
            # Resize and crop the image
            resized_image = resize_and_crop(image, target_width, target_height)
            
            # Save the resized image
            output_path = os.path.join(output_folder, f'resized_{filename}')
            cv2.imwrite(output_path, resized_image)
            print(f"Saved resized image: {output_path}")

if __name__ == "__main__":
    main()