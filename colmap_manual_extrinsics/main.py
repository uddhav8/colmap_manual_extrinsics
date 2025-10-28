# Import modules
import os
from src import helpers

# Assign directory
IMAGES_PATH = "C:/Users/Uddhav/Nextcloud/Projects/Media_Files/3D_Scans_Datasets/20250902_Gaon_Tree_Root/"

# Check if the path specified is a valid directory
if os.path.isdir(IMAGES_PATH):
    print("The path specified is a valid directory")

    files = os.listdir(IMAGES_PATH) # list of files

    # Check if the directory is not empty
    if files:
        print("Not empty directory")

        valid_images = [] # A list of all valid file names in the given dir

        for file in files:  # For each file in the dir
            file_path = os.path.join(IMAGES_PATH, file)
            try:
                # Check if file is a valid image
                if helpers.verify_img(file_path): # joining directory and file name and sending it with function
                    if file.lower().endswith(('.jpg', '.jpeg')) and os.stat(file_path).st_size > 0: # ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')
                        valid_images.append(file) # Add image to list of valid images
                else:
                    print("Skipping this file.")
            except Exception as e:
                print(f"Error verifying {file}: {e}")

        print(f"Valid images found: {valid_images}")

        for image in valid_images: # For each valid image in the dir
            file_path = os.path.join(IMAGES_PATH, image)
            try:
                gps_info = helpers.extract_exif(file_path, 34853) # 34853 is the tag ID for GPSInfo           
                user_comment = helpers.extract_exif(file_path, 37510) # 37510 is the tag ID for UserComment
                
                print(f"{image}: GPS = {gps_info}, IMU = {user_comment}")
                
                gps_cartesean = helpers.extract_gps_cartesean(gps_info) # helpers to extract only gps latitude, longitude, altitude (degrees, degrees, metres)
                orientation_euler = helpers.extract_euler_angles(user_comment) # helpers to extract only euler angles from IMU Data stored as EXIF user comment 
                
                translation_values = helpers.gps_to_translation(gps_cartesean) # helper to convert gps cartesean (deg, min, sec ) to translation values (TX, TY, TZ)
                orientation_quaternion = helpers.euler_to_quaternion(orientation_euler) # helper to convert euler to quaternions
                
                # reformat by joining and write to colmnap .txt file. Reference of camera and image id neede.
                # IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME
            except Exception as e:
                print(f"Error extracting EXIF from {image}: {e}")
    else:
        print("Empty directory")
else:
    print("The path is either for a file or not valid")