import numpy as np
import os

def load_and_print_npy_files(folder_path, print_intrinsic=True, print_extrinsic=True):
    # Define the file names
    camera_matrix_file = os.path.join(folder_path, 'camera_matrix.npy')
    dist_coeffs_file = os.path.join(folder_path, 'dist_coeffs.npy')
    rotation_vectors_file = os.path.join(folder_path, 'rotation_vectors.npy')
    translation_vectors_file = os.path.join(folder_path, 'translation_vectors.npy')

    # Load the .npy files
    camera_matrix = np.load(camera_matrix_file)
    dist_coeffs = np.load(dist_coeffs_file)
    rotation_vectors = np.load(rotation_vectors_file, allow_pickle=True)
    translation_vectors = np.load(translation_vectors_file, allow_pickle=True)

    # Print out the loaded parameters based on the arguments
    if print_intrinsic:
        print("Camera Matrix (Intrinsic Parameters):")
        print(camera_matrix)
        print("\nDistortion Coefficients:")
        print(dist_coeffs)

    if print_extrinsic:
        print("\nRotation Vectors (Extrinsic Parameters for each image):")
        for idx, rvec in enumerate(rotation_vectors):
            print(f"Image {idx + 1}:")
            print(rvec)
        print("\nTranslation Vectors (Extrinsic Parameters for each image):")
        for idx, tvec in enumerate(translation_vectors):
            print(f"Image {idx + 1}:")
            print(tvec)

# Example usage
if __name__ == "__main__":
    folder_path = '/home/js/Documents/GitHub/extract_video_timestamp/data/camera_to_kitti/calibration_horizontal_npy'  # Update with the correct path
    load_and_print_npy_files(folder_path, print_intrinsic=True, print_extrinsic=False)