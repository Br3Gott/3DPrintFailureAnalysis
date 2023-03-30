from picamera2 import Picamera2
import time
import os
import datetime
import sys
from opencv.pre_processing.filter import filter_image
import cv2 as cv
import numpy as np

picam2 = Picamera2()
picam2.start()
time.sleep(2)
image_count = 0

# command line argument fail / success
# path = "./dataset#" + datetime.datetime.now().strftime("%Y-%m-%d")
path = "./dataset#" + sys.argv[2]

if sys.argv[1] == "fail":
    if not os.path.exists(path + "/fail"):
        os.makedirs(path + "/fail")
else:
    if not os.path.exists(path + "/success"):
        os.makedirs(path + "/success")

while True:
    image = None
    if sys.argv[1] == "fail":
        file = path + "/fail/" + datetime.datetime.now().time().strftime("%H-%M-%S") + ".jpg"
    else:
        file = path + "/success/" + datetime.datetime.now().time().strftime("%H-%M-%S") + ".jpg"
    
    image = picam2.capture_array("main")
    image = filter_image(image)
    cv.imwrite(file, image)
    image_count += 1
    print("Took image: Number {}, Filename {}".format(image_count, file))
    

    time.sleep(10)