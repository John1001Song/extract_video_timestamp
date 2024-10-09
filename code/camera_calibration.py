import cv2
import numpy as np
import glob
import os

def calibrate_camera(chessboard_images, chessboard_size, square_size, corner_img_output, npy_output):
    """
    Calibrate a camera using chessboard images and save the calibration results.

    Args:
    - chessboard_images (list of str): List of file paths to chessboard images.
    - chessboard_size (tuple): Number of inner corners per a chessboard row and column (width, height).
    - square_size (float): The size of a square on your chessboard in real-world units (e.g., meters or millimeters).
    - output_folder (str): Directory to save calibration visualizations and results.

    Returns:
    - ret (bool): Whether calibration was successful.
    - mtx (ndarray): Camera matrix (intrinsic parameters).
    - dist (ndarray): Distortion coefficients.
    - rvecs (list): Rotation vectors (extrinsic parameters for each image).
    - tvecs (list): Translation vectors (extrinsic parameters for each image).
    - objpoints (list): 3D points in real world space.
    - imgpoints (list): 2D points in image plane.
    """
    # Termination criteria for corner subpixel refinement
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)
    objp *= square_size

    objpoints = []  # 3D points in real world space
    imgpoints = []  # 2D points in image plane

    if not os.path.exists(corner_img_output):
        os.makedirs(corner_img_output)
    if not os.path.exists(npy_output):
        os.makedirs(npy_output)

    for i, fname in enumerate(chessboard_images):
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

        if ret:
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)
            cv2.drawChessboardCorners(img, chessboard_size, corners2, ret)

            # Show the image with the chessboard corners
            cv2.imshow('Chessboard Corners', img)
            cv2.waitKey(100)

            # Save the visualized image to the output folder
            output_filename = os.path.join(corner_img_output, f"corners_{i:04d}.jpg")
            cv2.imwrite(output_filename, img)

    # Destroy all windows after processing all images
    cv2.destroyAllWindows()

    if len(objpoints) == 0:
        print("No valid chessboard images were found.")
        return False, None, None, None, None, None, None

    # Perform camera calibration to find internal and external parameters
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    if ret:
        np.save(os.path.join(npy_output, 'camera_matrix.npy'), mtx)
        np.save(os.path.join(npy_output, 'dist_coeffs.npy'), dist)
        np.save(os.path.join(npy_output, 'rotation_vectors.npy'), rvecs)
        np.save(os.path.join(npy_output, 'translation_vectors.npy'), tvecs)

    return ret, mtx, dist, rvecs, tvecs, objpoints, imgpoints


def undistort_image(image_path, mtx, dist):
    """
    Undistort an image using the provided camera matrix and distortion coefficients.

    Args:
    - image_path (str): Path to the image to undistort.
    - mtx (ndarray): Camera matrix.
    - dist (ndarray): Distortion coefficients.
    """
    img = cv2.imread(image_path)
    h, w = img.shape[:2]
    new_camera_mtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    undistorted_img = cv2.undistort(img, mtx, dist, None, new_camera_mtx)

    # Crop the image (optional) based on the region of interest
    x, y, w, h = roi
    undistorted_img = undistorted_img[y:y+h, x:x+w]

    cv2.imshow("Undistorted Image", undistorted_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def compute_reprojection_error(objpoints, imgpoints, rvecs, tvecs, mtx, dist):
    """
    Compute the re-projection error for the camera calibration.

    Args:
    - objpoints (list): 3D points in real world space.
    - imgpoints (list): 2D points in image plane.
    - rvecs (list): Rotation vectors from the calibration.
    - tvecs (list): Translation vectors from the calibration.
    - mtx (ndarray): Camera matrix (intrinsic parameters).
    - dist (ndarray): Distortion coefficients.

    Returns:
    - error (float): Re-projection error.
    """
    total_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
        total_error += error
    return total_error / len(objpoints)


# Main Usage Example
if __name__ == "__main__":
    chessboard_images = glob.glob('../data/output/calibration_horizontal_frames/*.jpg')
    chessboard_size = (9, 6)  # Number of inner corners per row and column
    square_size = 0.0255  # Size of a square in meters
    corner_output_folder = '../data/output/calibration_horizontal_res/'
    npy_output_folder = "../data/output/calibration_horizontal_npy/"
    # Calibrate the camera and obtain the required points
    ret, mtx, dist, rvecs, tvecs, objpoints, imgpoints = calibrate_camera(chessboard_images, chessboard_size, square_size, corner_output_folder, npy_output_folder)

    if ret:
        print("Camera calibration was successful.")
        print("Camera matrix (intrinsic parameters):\n", mtx)
        print("Distortion coefficients:\n", dist)

        # Re-projection error computation
        error = compute_reprojection_error(objpoints, imgpoints, rvecs, tvecs, mtx, dist)
        print(f"Re-projection error: {error}")

        # Optionally, undistort an image to verify the calibration
        # undistort_image('../data/output/calibration_horizontal_frames/example_image.jpg', mtx, dist)

    else:
        print("Camera calibration failed.")
