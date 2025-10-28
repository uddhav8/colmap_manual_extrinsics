import math
import numpy as np

# Converts degrees → radians automatically.
# Computes quaternion using yaw-pitch-roll (Z-X-Y) convention.
# Normalizes the quaternion to ensure it represents a valid rotation.
def euler_to_quaternion(yaw_deg, pitch_deg, roll_deg):
    # Convert degrees to radians
    yaw = math.radians(yaw_deg)
    pitch = math.radians(pitch_deg)
    roll = math.radians(roll_deg)

    # Compute half angles
    cy = math.cos(yaw * 0.5)
    sy = math.sin(yaw * 0.5)
    cp = math.cos(pitch * 0.5)
    sp = math.sin(pitch * 0.5)
    cr = math.cos(roll * 0.5)
    sr = math.sin(roll * 0.5)

    # Quaternion calculations (w, x, y, z)
    w = cr * cp * cy + sr * sp * sy
    x = sr * cp * cy - cr * sp * sy
    y = cr * sp * cy + sr * cp * sy
    z = cr * cp * sy - sr * sp * cy

    # Normalize the quaternion
    norm = math.sqrt(w*w + x*x + y*y + z*z)
    w /= norm
    x /= norm
    y /= norm
    z /= norm

    return w, x, y, z

# ✅ Advantages of NumPy version:
# Fast vectorized operations if you have arrays of Euler angles.
# Cleaner syntax and automatic broadcasting for multiple inputs.
# Automatically returns a unit quaternion, ready for 3D rotations.
def euler_to_quaternion_numpy(yaw_deg, pitch_deg, roll_deg):
    """
    Convert Euler angles (yaw, pitch, roll) in degrees to a normalized quaternion (w, x, y, z).
    Assumes Z (yaw) - X (pitch) - Y (roll) rotation order.
    """
    # Convert degrees to radians
    yaw = np.radians(yaw_deg)
    pitch = np.radians(pitch_deg)
    roll = np.radians(roll_deg)

    # Compute half angles
    cy = np.cos(yaw * 0.5)
    sy = np.sin(yaw * 0.5)
    cp = np.cos(pitch * 0.5)
    sp = np.sin(pitch * 0.5)
    cr = np.cos(roll * 0.5)
    sr = np.sin(roll * 0.5)

    # Quaternion components
    w = cr * cp * cy + sr * sp * sy
    x = sr * cp * cy - cr * sp * sy
    y = cr * sp * cy + sr * cp * sy
    z = cr * cp * sy - sr * sp * cy

    # Normalize
    norm = np.sqrt(w**2 + x**2 + y**2 + z**2)
    w /= norm
    x /= norm
    y /= norm
    z /= norm

    return np.array([w, x, y, z])

# Example usage with your values
yaw = 238.11612
pitch = -23.968082481265608
roll = -1.6908994239253161

# q = euler_to_quaternion(yaw, pitch, roll)
q = euler_to_quaternion_numpy(yaw, pitch, roll)
print("Normalized Quaternion (w, x, y, z):", q)
