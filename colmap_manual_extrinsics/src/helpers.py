import os
import re
import numpy as np
import pyproj
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS, GPSTAGS
from scipy.spatial.transform import Rotation as R

# Function to verify if the file is a valid image
def verify_img(img_path):
    try:
        verify_response = Image.open(img_path).verify()
        print(f'{verify_response} was returned by verify')
        if verify_response == None:
            print(f"{os.path.basename(img_path)} is a valid image.")
        return True
    except Exception as e:
        print(f"Invalid image ({os.path.basename(img_path)}): {e}")
        return False

# extract exif data from image file, specify which data is needed (GPS and IMU Data)
def extract_exif(img_path, tag_id):    
    try:
        exif_data = Image.open(img_path)._getexif() # Extract EXIF data. Dictionary
        if exif_data: # Check if EXIF data is available
            # print all the tags available
            for id, val in exif_data.items(): # looping through all the tags present in exifdata
                tag_name = TAGS.get(id, id) # getting the tag name instead of tag id. Adds a Default Value. If the tag isn’t found, instead of returning None, it will return the original tagid itself.
                #print(f"{id:15}: {tag_name:25}: {val}") # printing the metadata

            #exif = {TAGS.get(tag_id, tag_id): value for tag_id, value in exif_data.items()} # Map EXIF tag IDs to names
            #return exif.get(tag_id)
            return exif_data.get(tag_id)
        else:
            print("No EXIF data found.")
            return None
    except Exception as e:
        print(f"Error opening image: {e}")
        return None

# Extract GPS Data (Lat,Long,Alt)
def extract_gps_cartesean(gps_info):
    gps_data = {}
    for key, value in gps_info.items():
        gps_tag_name = GPSTAGS.get(key, key) # Get the GPS tag name
        gps_data[gps_tag_name] = value
        print (gps_data)
        print(f"{key:15}: {gps_tag_name:25}: {gps_info[key]}")
    '''
    def dms_to_dd(dms):
        degrees, minutes, seconds = dms
        return degrees + minutes/60 + seconds/3600

    latitude_dms = data[2]
    longitude_dms = data[4]

    latitude_dd = dms_to_dd(latitude_dms)
    longitude_dd = dms_to_dd(longitude_dms)

    # Altitude (assume the third element of the tuple is altitude)
    latitude_alt = latitude_dms[2]
    longitude_alt = longitude_dms[2]

    print("Latitude:", latitude_dd)
    print("Longitude:", longitude_dd)
    print("Altitude (lat):", latitude_alt)
    print("Altitude (lon):", longitude_alt)'''
    """
    data = {
    'GPSLatitudeRef': 'N',
    'GPSLatitude': (16.0, 14.0, 50.0303304),
    'GPSLongitudeRef': 'E',
    'GPSLongitude': (73.0, 25.0, 52.2505909),
    'GPSAltitude': 72.71359807460891
    }

    def dms_to_dd(dms, ref):
        degrees, minutes, seconds = dms
        dd = degrees + minutes/60 + seconds/3600
        if ref in ['S', 'W']:
            dd = -dd
        return dd

    latitude = dms_to_dd(data['GPSLatitude'], data['GPSLatitudeRef'])
    longitude = dms_to_dd(data['GPSLongitude'], data['GPSLongitudeRef'])
    altitude = data['GPSAltitude']

    print("Latitude (decimal degrees):", latitude)
    print("Longitude (decimal degrees):", longitude)
    print("Altitude (meters):", altitude)
    """

# Extract IMU (Yaw, Pitch, Roll) from user comment as Euler angles
def extract_euler_angles(user_comment):
    # Extract numbers after Yaw, Pitch, and Roll using regex
    yaw_match = re.search(r"Yaw:([-\d\.]+)", user_comment)
    pitch_match = re.search(r"Pitch:([-\d\.]+)", user_comment)
    roll_match = re.search(r"Roll:([-\d\.]+)", user_comment)

    yaw = float(yaw_match.group(1)) if yaw_match else None
    pitch = float(pitch_match.group(1)) if pitch_match else None
    roll = float(roll_match.group(1)) if roll_match else None

    print (f"Yaw: {yaw}, Pitch: {pitch}, Roll: {roll}")
    return (yaw, pitch, roll)

# Convert GPS → Cartesian Translation (TX, TY, TZ)
def gps_to_translation(gps_cartesean):
    lat, lon, alt = 16 + 14/60 + 50.03/3600, 73 + 25/60 + 52.25/3600, -72.7 # Convert GPS coordinates into decimal degrees and assign altitude

    # Convert to ECEF coordinates
    wgs84 = pyproj.Proj(proj='latlong', datum='WGS84')
    ecef = pyproj.Proj(proj='geocent', datum='WGS84')

    x, y, z = pyproj.transform(wgs84, ecef, lon, lat, alt)
    print(x, y, z)

    # If you have multiple images, you can subtract the first image’s position to make a local coordinate system centered at the first camera.
    # tx, ty, tz = x - x0, y - y0, z - z0
    # Now (tx, ty, tz) becomes your translation vector for images.txt.

def euler_to_quaternion(euler_angles):
    '''
    Common aerospace / navigation convention is:
    yaw → z-axis
    pitch → y-axis
    roll → x-axis
    So the Euler order is 'zyx'.
    '''
    r = R.from_euler('zyx', euler_angles, degrees=True) # Quaternions are computed with angles in radians. Create rotation from Euler angles (degrees=True). degrees=True means the input angles are in degrees, not radians.
    quaternion_angles = r.as_quat(scalar_first=True) # Convert to quaternion (w, x, y, z)
    print (quaternion_angles)
    return quaternion_angles

# imgPath = 'C:/Users/Uddhav/Nextcloud/Projects/Project_Files/Software_Development/Python/20251022_colmap_manual_extrinsics/colmap_manual_extrinsics/assets/image.jpg'
imgPath = "C:/Users/Uddhav/Nextcloud/Projects/Media_Files/3D_Scans_Datasets/20250902_Gaon_Tree_Root/IMG_20250902_144630.123.jpg"
verify_img(imgPath)

gpsInfo = extract_exif(imgPath, 34853)
print(gpsInfo)
gpsCartn = extract_gps_cartesean(gpsInfo)
print(gpsCartn)
transVal = gps_to_translation(gpsCartn)
print(transVal)

usrCmnt = extract_exif(imgPath, 37510)
print(usrCmnt) #ASCIIYaw:238.11612,Pitch:-23.968082481265608,Roll:-1.6908994239253161
orntEuler = extract_euler_angles(usrCmnt)
print(orntEuler)
orntQuat = euler_to_quaternion(orntEuler)
print(orntQuat)