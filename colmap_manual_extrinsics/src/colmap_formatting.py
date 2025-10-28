from scipy.spatial.transform import Rotation as R
import numpy as np
import pyproj

#IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME

yaw, pitch, roll = np.deg2rad([238.11612, -23.968082481265608, -1.6908994239253161])
rot = R.from_euler('zyx', [yaw, pitch, roll])
qw, qx, qy, qz = rot.as_quat()  # [x, y, z, w]
# COLMAP expects qw qx qy qz
qw, qx, qy, qz = qz, qx, qy, qw
print(qw, qx, qy, qz)





lat, lon, alt = 16 + 14/60 + 50.03/3600, 73 + 25/60 + 52.25/3600, -72.7

# Convert to ECEF coordinates
wgs84 = pyproj.Proj(proj='latlong', datum='WGS84')
ecef = pyproj.Proj(proj='geocent', datum='WGS84')

x, y, z = pyproj.transform(wgs84, ecef, lon, lat, alt)
print(x, y, z)















import numpy as np
from scipy.spatial.transform import Rotation as R

yaw, pitch, roll = np.deg2rad([238.11612, -23.968082481265608, -1.6908994239253161])
rot = R.from_euler('zyx', [yaw, pitch, roll])
qw, qx, qy, qz = rot.as_quat()  # returns [x, y, z, w]












import pyproj

# Define Earth model
geod = pyproj.Geod(ellps='WGS84')
ecef = pyproj.Proj(proj='geocent', ellps='WGS84')
lla = pyproj.Proj(proj='latlong', ellps='WGS84')

lat, lon, alt = 16.24723, 73.43118, -72.7  # decimal degrees + altitude

# Convert to ECEF coordinates (meters)
x, y, z = pyproj.transform(lla, ecef, lon, lat, alt)