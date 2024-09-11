import numpy as np
import cv2
import xml.etree.ElementTree as ET

# Function to extract 3D bounding box corners from the XML annotation file
def extract_3d_bbox_corners_from_xml(xml_file_path, image_filename):
    """
    Extract 3D bounding box corners from the XML annotation file.

    Args:
    - xml_file_path (str): Path to the XML annotation file.
    - image_filename (str): Filename of the image to extract corners for.

    Returns:
    - corners (dict): Dictionary containing the corners of the cuboid.
    """
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Find the 'image' element with the specific filename
    for image in root.findall('image'):
        if image.get('name') == image_filename:
            corners = {}
            cuboid = image.find('cuboid')
            if cuboid is not None:
                # Extract each corner position
                corners['xtl1'] = (float(cuboid.get('xtl1')), float(cuboid.get('ytl1')))
                corners['xbl1'] = (float(cuboid.get('xbl1')), float(cuboid.get('ybl1')))
                corners['xtr1'] = (float(cuboid.get('xtr1')), float(cuboid.get('ytr1')))
                corners['xbr1'] = (float(cuboid.get('xbr1')), float(cuboid.get('ybr1')))
                corners['xtl2'] = (float(cuboid.get('xtl2')), float(cuboid.get('ytl2')))
                corners['xbl2'] = (float(cuboid.get('xbl2')), float(cuboid.get('ybl2')))
                corners['xtr2'] = (float(cuboid.get('xtr2')), float(cuboid.get('ytr2')))
                corners['xbr2'] = (float(cuboid.get('xbr2')), float(cuboid.get('ybr2')))
            return corners

    return None


def convert_2d_to_3d(camera_matrix, corners_2D, depths):
    """
    Convert 2D corners back to 3D space in the camera coordinate system.

    Args:
    - camera_matrix (ndarray): The camera intrinsic matrix.
    - corners_2D (list): List of 2D pixel coordinates of the 3D bounding box corners.
    - depths (list): List of depth values for each corner.

    Returns:
    - corners_3D (ndarray): Array containing the 3D coordinates of the bounding box corners.
    """
    corners_3D = []
    K_inv = np.linalg.inv(camera_matrix)

    for (u, v), Z in zip(corners_2D, depths):
        # Scale down the depth value by 36
        Z = Z / 36.0
        uv1 = np.array([[u], [v], [1]])
        # Calculate 3D coordinates in the camera coordinate system
        xyz_camera = K_inv @ (uv1 * Z)
        corners_3D.append(xyz_camera.flatten())

    return np.array(corners_3D)


def get_depth_from_npy(depth_npy_path, corners_2D):
    """
    Get the depth values from a .npy file for the specified 2D pixel positions.

    Args:
    - depth_npy_path (str): Path to the .npy file containing depth data.
    - corners_2D (list): List of 2D pixel coordinates of the 3D bounding box corners.

    Returns:
    - depths (list): List of depth values for each corner.
    """
    depth_data = np.load(depth_npy_path)
    depths = [depth_data[int(v), int(u)] for (u, v) in corners_2D]
    return depths

# Paths
camera_matrix_path = '../data/output/calibration/camera_matrix.npy'
dist_coeffs_path = '../data/output/calibration/dist_coeffs.npy'
depth_npy_path = '../data/output/depth_imgs/test_car_wo_timestamp_raw_depth_meter.npy'
xml_file_path = '../data/annotation/annotations_2.xml'
image_filename = 'test_car_wo_timestamp.jpg'

# Load camera intrinsic matrix
camera_matrix = np.load(camera_matrix_path)
dist_coeffs = np.load(dist_coeffs_path)

print("Loaded Camera Matrix:\n", camera_matrix)
print("Loaded Distortion Coefficients:\n", dist_coeffs)

# Extract 3D bounding box corners from the XML file
corners_2D = extract_3d_bbox_corners_from_xml(xml_file_path, image_filename)

if corners_2D:
    print(f"Extracted 2D corners from {image_filename}:")
    for key, value in corners_2D.items():
        print(f"{key}: {value}")

    # Convert the dictionary of corners to a list for further processing
    corners_2D_list = list(corners_2D.values())

    # Get depth values from the .npy file for each 2D corner
    depths = get_depth_from_npy(depth_npy_path, corners_2D_list)

    # Convert 2D corners back to 3D coordinates
    corners_3D = convert_2d_to_3d(camera_matrix, corners_2D_list, depths)

    print("3D coordinates of the bounding box corners in camera space:\n", corners_3D)
else:
    print(f"No corners found for {image_filename} in {xml_file_path}")

# # Load the camera intrinsic matrix
# camera_matrix = np.load('../data/output/calibration/camera_matrix.npy')
# dist_coeffs = np.load('../data/output/calibration/dist_coeffs.npy')

# # Example of using loaded camera matrix and distortion coefficients
# print("Loaded Camera Matrix:\n", camera_matrix)
# print("Loaded Distortion Coefficients:\n", dist_coeffs)

# # Extract 3D bounding box corners from the annotation XML
# xml_file_path = '../data/annotation/annotations_2.xml'
# image_filename = 'TimeVideo_20240901_180247_30feet_frame_0000.jpg'
# corners_3d = extract_3d_bbox_corners_from_xml(xml_file_path, image_filename)

# if corners_3d:
#     print(f"Extracted 3D bounding box corners from {image_filename}:")
#     for key, value in corners_3d.items():
#         print(f"{key}: {value}")
# else:
#     print(f"No corners found for {image_filename} in {xml_file_path}")


# # 2D pixel coordinates of the 3D bounding box corners in the image
# top_front_left = (955.06, 233.27)    # TFL
# bottom_front_left = (955.06, 633.41) # BFL
# top_front_right = (1145.69, 233.17)   # TFR
# bottom_front_right = (1145.69, 633.41) # BFR
# top_back_left = (1164.76, 193.55)     # TBL
# bottom_back_left = (1164.76, 593.59)  # BBL
# top_back_right = (974.22, 193.66)    # TBR
# bottom_back_right = (974.22, 593.60) # BBR

# # List of 2D pixel coordinates of the 3D bounding box corners
# corners_2D = [
#     top_front_left,    
#     bottom_front_left, 
#     top_front_right,   
#     bottom_front_right,
#     top_back_left,     
#     bottom_back_left,  
#     top_back_right,    
#     bottom_back_right  
# ]

# # Define the depth values for each corner (example depths, should be replaced with actual data)
# depths = [3.048, 3.048, 3.048, 3.048, 3.148, 3.148, 3.148, 3.148]  # Replace with actual depth values

# # Convert 2D corners back to 3D space
# corners_3D = []
# K_inv = np.linalg.inv(camera_matrix)

# for (u, v), Z in zip(corners_2D, depths):
#     uv1 = np.array([[u], [v], [1]])
#     # Calculate 3D coordinates in the camera coordinate system
#     xyz_camera = K_inv @ (uv1 * Z)
#     corners_3D.append(xyz_camera.flatten())

# corners_3D = np.array(corners_3D)

# print("3D coordinates of the bounding box corners in camera space:\n", corners_3D)
