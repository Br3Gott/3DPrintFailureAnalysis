#####################################################
# Script to test for broken/invalid files.          #
# Prints all invalid files to help troubleshooting. #
# Only allows extensions valid for TensorFlow       #
#####################################################


from pathlib import Path
import imghdr

data_dir = "./datasets/print_data/fail/"
image_extensions = [".jpg"]  # add there all your images file extensions

img_type_accepted_by_tf = ["bmp", "gif", "jpeg", "png"]
for filepath in Path(data_dir).rglob("*"):
    if filepath.suffix.lower() in image_extensions:
        img_type = imghdr.what(filepath)
        if img_type is None:
            print(f"{filepath} is not an image")
        elif img_type not in img_type_accepted_by_tf:
            print(f"{filepath} is a {img_type}, not accepted by TensorFlow")