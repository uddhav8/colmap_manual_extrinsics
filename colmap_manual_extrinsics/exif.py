import exifread

# Open the image
file_path = 'image.jpg'

# Open image file for reading (must be in binary mode)
with open(file_path, "rb") as file_handle:

    # Return Exif tags
    tags = exifread.process_file(file_handle)