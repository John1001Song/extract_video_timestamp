import numpy as np
import os

# Load camera parameters from npy files
npy_folder = "/home/js/Documents/GitHub/extract_video_timestamp/data/camera_to_kitti/calibration_horizontal_npy"
K_original = np.load(os.path.join(npy_folder, "camera_matrix.npy"))
dist = np.load(os.path.join(npy_folder, "dist_coeffs.npy"))

# Original and target image sizes
original_width, original_height = 1920, 1080
target_width, target_height = 1242, 375

# Calculate scale factors
scale_x = target_width / original_width
scale_y = target_height / original_height

# Adjust the intrinsic matrix
K_resized = K_original.copy()
K_resized[0, 0] *= scale_x  # Adjust f_x
K_resized[1, 1] *= scale_y  # Adjust f_y
K_resized[0, 2] *= scale_x  # Adjust c_x
K_resized[1, 2] *= scale_y  # Adjust c_y

print("Adjusted Intrinsic Matrix:\n", K_resized)