import numpy as np

def adjust_intrinsic_for_bottom_crop(camera_matrix, original_height, crop_height):
    """
    Adjust the camera intrinsic matrix when cropping the bottom part of the image.

    Parameters:
        camera_matrix (np.ndarray): Original 3x3 camera intrinsic matrix.
        original_height (int): Original height of the image.
        crop_height (int): New height after cropping from the bottom.

    Returns:
        np.ndarray: Updated camera intrinsic matrix.
    """
    # Copy the original camera matrix
    adjusted_camera_matrix = camera_matrix.copy()

    # Calculate the amount cropped from the bottom
    crop_amount = original_height - crop_height

    # Adjust the vertical principal point (c_y) by subtracting the crop amount
    adjusted_camera_matrix[1, 2] -= crop_amount

    return adjusted_camera_matrix

# Original camera intrinsic parameters (from 1600x1200)
camera_matrix = np.array([
    [1.46441343e+04, 0.00000000e+00, 8.28119820e+02],
    [0.00000000e+00, 2.54503534e+03, 5.92577085e+02],
    [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]
])
# 1600x1200 --> 1600x900
# Original and new heights
original_height = 1200
crop_height = 900

# Adjust the intrinsic matrix for bottom crop
adjusted_camera_matrix = adjust_intrinsic_for_bottom_crop(camera_matrix, original_height, crop_height)
print("Adjusted Camera Intrinsic Matrix:")
print(adjusted_camera_matrix)
