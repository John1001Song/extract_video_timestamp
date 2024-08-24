import numpy as np
import cv2

# Load the calibration results
camera_matrix = np.load('../data/output/calibration/camera_matrix.npy')
dist_coeffs = np.load('../data/output/calibration/dist_coeffs.npy')
rotation_vectors = np.load('../data/output/calibration/rotation_vectors.npy', allow_pickle=True)
translation_vectors = np.load('../data/output/calibration/translation_vectors.npy', allow_pickle=True)

# Example of using loaded camera matrix and distortion coefficients
print("Loaded Camera Matrix:\n", camera_matrix)
print("Loaded Distortion Coefficients:\n", dist_coeffs)

# If you need to use rotation vectors and translation vectors
for i, (rvec, tvec) in enumerate(zip(rotation_vectors, translation_vectors)):
    R = cv2.Rodrigues(rvec)[0]
    print(f"Rotation matrix for image {i}:\n", R)
    print(f"Translation vector for image {i}:\n", tvec)
