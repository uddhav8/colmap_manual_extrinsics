import os
import re
import pycolmap
from PIL import Image, ExifTags
from scipy.spatial.transform import Rotation as R

# === CONFIG ===
IMAGE_DIR = "path/to/your/images"          # Folder with input images
DB_PATH = "path/to/your/colmap/database.db" # Path to your COLMAP database

# --- Helper: extract EXIF user comment ---
def get_user_comment(image_path):
    try:
        img = Image.open(image_path)
        exif = img._getexif()
        if not exif:
            return None

        for tag_id, value in exif.items():
            tag = ExifTags.TAGS.get(tag_id, tag_id)
            if tag == "UserComment":
                if isinstance(value, bytes):
                    try:
                        value = value.decode("utf-8", errors="ignore")
                    except Exception:
                        value = value.decode("latin1", errors="ignore")
                return value
    except Exception as e:
        print(f"⚠️ Error reading EXIF from {image_path}: {e}")
    return None


# --- Helper: parse yaw/pitch/roll from comment ---
def parse_ypr(comment):
    if not comment:
        return None

    # Use regex to find numeric values after Yaw, Pitch, Roll
    yaw_match = re.search(r"Yaw:([-\d\.]+)", comment)
    pitch_match = re.search(r"Pitch:([-\d\.]+)", comment)
    roll_match = re.search(r"Roll:([-\d\.]+)", comment)

    if not (yaw_match and pitch_match and roll_match):
        return None

    return (
        float(yaw_match.group(1)),
        float(pitch_match.group(1)),
        float(roll_match.group(1)),
    )


# --- Helper: convert YPR → quaternion (qw, qx, qy, qz) ---
def ypr_to_quaternion(yaw, pitch, roll):
    # Convert Euler angles to quaternion (ZYX order for yaw-pitch-roll)
    r = R.from_euler("ZYX", [yaw, pitch, roll], degrees=True)
    qx, qy, qz, qw = r.as_quat()  # scipy gives (x, y, z, w)
    return qw, qx, qy, qz


# --- Helper: update database entry ---
def update_database(image_name, qw, qx, qy, qz, conn):
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE images
        SET prior_qw=?, prior_qx=?, prior_qy=?, prior_qz=?
        WHERE name=?;
        """,
        (qw, qx, qy, qz, image_name),
    )
    conn.commit()


# === MAIN SCRIPT ===
def main():
    conn = sqlite3.connect(DB_PATH)

    updated = 0
    for filename in os.listdir(IMAGE_DIR):
        if not filename.lower().endswith((".jpg", ".jpeg", ".png", ".tif")):
            continue

        path = os.path.join(IMAGE_DIR, filename)
        comment = get_user_comment(path)
        ypr = parse_ypr(comment)

        if ypr:
            yaw, pitch, roll = ypr
            qw, qx, qy, qz = ypr_to_quaternion(yaw, pitch, roll)
            update_database(filename, qw, qx, qy, qz, conn)
            print(f"✅ Updated {filename} | Yaw={yaw:.2f}, Pitch={pitch:.2f}, Roll={roll:.2f}")
            updated += 1
        else:
            print(f"⚠️ No valid YPR in {filename}")

    conn.close()
    print(f"\n✅ Done. Updated {updated} image(s) in database: {DB_PATH}")


if __name__ == "__main__":
    main()
