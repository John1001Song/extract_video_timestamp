import cv2
import numpy as np
import glob
import os

def calibrate_camera(chessboard_images, chessboard_size, square_size):
    """
    Calibrate a camera using chessboard images.

    Args:
    - chessboard_images (list of str): List of file paths to chessboard images.
    - chessboard_size (tuple): Number of inner corners per a chessboard row and column (width, height).
    - square_size (float): The size of a square on your chessboard in real-world units (e.g., meters or millimeters).

    Returns:
    - ret (bool): Whether calibration was successful.
    - mtx (ndarray): Camera matrix (internal parameters).
    - dist (ndarray): Distortion coefficients.
    - rvecs (list): Rotation vectors (external parameters for each image).
    - tvecs (list): Translation vectors (external parameters for each image).
    """
    # Termination criteria for corner subpixel refinement
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    
    # Prepare object points based on real-world coordinates
    objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)
    objp *= square_size
    
    # Arrays to store object points and image points from all images
    objpoints = []  # 3D points in real world space
    imgpoints = []  # 2D points in image plane

    # Create output folder for visualized corners if it does not exist
    output_folder = '../data/output/corners_in_frames/'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over each chessboard image
    for i, fname in enumerate(chessboard_images):
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

        if ret:
            objpoints.append(objp)
            # Refine corner locations to subpixel accuracy
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)
            
            # Visualize the corners
            cv2.drawChessboardCorners(img, chessboard_size, corners2, ret)
            cv2.imshow('Chessboard Corners', img)
            cv2.waitKey(100)

            # Save the visualized image to the output folder
            output_filename = os.path.join(output_folder, f"corners_{i:04d}.jpg")
            cv2.imwrite(output_filename, img)

    cv2.destroyAllWindows()

    # Perform camera calibration to find internal and external parameters
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    if ret:
        # Save calibration results
        np.save('../data/output/calibration/camera_matrix.npy', mtx)
        np.save('../data/output/calibration/dist_coeffs.npy', dist)
        np.save('../data/output/calibration/rotation_vectors.npy', rvecs)
        np.save('../data/output/calibration/translation_vectors.npy', tvecs)

    return ret, mtx, dist, rvecs, tvecs

# Usage example
chessboard_images = glob.glob('../data/output/calibration_frames/*.jpg')  # Update with your image path
chessboard_size = (9, 6)  # Update with the number of inner corners per chessboard row and column
square_size = 0.0255  # Update with the size of a square on your chessboard in meters

ret, mtx, dist, rvecs, tvecs = calibrate_camera(chessboard_images, chessboard_size, square_size)

if ret:
    print("Camera calibration was successful.")
    print("Camera matrix (intrinsic parameters):\n", mtx)
    print("Distortion coefficients:\n", dist)
    print("Rotation vectors (extrinsic parameters):\n", rvecs)
    print("Translation vectors (extrinsic parameters):\n", tvecs)
else:
    print("Camera calibration failed.")
