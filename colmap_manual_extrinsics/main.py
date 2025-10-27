from PIL import Image
from PIL.ExifTags import TAGS

import re

# Open the image
image = Image.open('image.jpg')

# Extract EXIF data
exif_data = image._getexif()

user_comment = None

if exif_data is not None:
    for tag_id, value in exif_data.items():
        tag_name = TAGS.get(tag_id, tag_id)
        if tag_name == 'UserComment':
            user_comment = value
            break

if user_comment:
    # UserComment is often stored as bytes, so decode if necessary
    if isinstance(user_comment, bytes):
        try:
            user_comment = user_comment.decode('utf-8', errors='ignore')
        except Exception:
            # Fallback decoding if utf-8 fails
            user_comment = user_comment.decode('latin1', errors='ignore')
    print("User Comment:", user_comment)
else:
    print("No User Comment found")


# Extract numbers after Yaw, Pitch, and Roll using regex
yaw_match = re.search(r"Yaw:([-\d\.]+)", user_comment)
pitch_match = re.search(r"Pitch:([-\d\.]+)", user_comment)
roll_match = re.search(r"Roll:([-\d\.]+)", user_comment)

yaw = float(yaw_match.group(1)) if yaw_match else None
pitch = float(pitch_match.group(1)) if pitch_match else None
roll = float(roll_match.group(1)) if roll_match else None

print("Yaw:", yaw)
print("Pitch:", pitch)
print("Roll:", roll)