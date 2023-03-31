from picamera2 import Picamera2
import time
import os
import datetime
import sys
from opencv.pre_processing.filter import filter_image
import cv2 as cv
import numpy as np

picam2 = Picamera2()
capture_config = picam2.create_still_configuration(main={"format": 'RGB888', "size": (3280, 2464)})
picam2.configure(capture_config)


picam2.start()
time.sleep(2)
image_count = 0

# command line argument fail / success
# path = "./dataset#" + datetime.datetime.now().strftime("%Y-%m-%d")
path = "./dataset#" + sys.argv[2]

if sys.argv[1] == "fail":
    if not os.path.exists(path + "/fail_raw"):
        os.makedirs(path + "/fail_raw")
        os.makedirs(path + "/fail_filtered")
        os.makedirs(path + "/fail_masked")
else:
    if not os.path.exists(path + "/success_raw"):
        os.makedirs(path + "/success_raw")
        os.makedirs(path + "/success_filtered")
        os.makedirs(path + "/success_masked")

while True:
    image = None
    curr_date = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    if sys.argv[1] == "fail":
        file_raw = path + "/fail_raw/" + curr_date + ".jpg"
        file_filtered = path + "/fail_filtered/" + curr_date + ".jpg"
        file_masked = path + "/fail_masked/" + curr_date + ".jpg"
    else:
        file_raw = path + "/success_raw/" + curr_date + ".jpg"
        file_filtered = path + "/success_filtered/" + curr_date + ".jpg"
        file_masked = path + "/success_masked/" + curr_date + ".jpg"
    
    image_raw = picam2.capture_array("main")
    image_filtered = filter_image(image_raw)
    image_masked = cv.bitwise_and(image_raw, image_raw, mask=image_filtered)
    cv.imwrite(file_raw, image_raw)
    cv.imwrite(file_filtered, image_filtered)
    cv.imwrite(file_masked, image_masked)
    image_count += 1
    print("Took image: Number {}, Filename {}".format(image_count, file_raw))
    

    time.sleep(10)