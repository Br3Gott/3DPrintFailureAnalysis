import cv2 as cv
import numpy as np
import time
from picamera2 import Picamera2 as PiCamera
import os

import datetime

from opencv.pre_processing.filter import filter_image
from opencv.pixel_observer.pixel import make_pixel

from tensorflow.tensorflow_identify import Identify

camera = PiCamera()
camera.start()
time.sleep(1)

pixel = make_pixel(0.4, 50)

def user_prompt():
    text = ""
    while (text != 'y' and text != 'n'):
        text = input("Failed! Continue monitor? (y/n): ")
    if (text == 'n'):
        print("Exiting...")
        exit()
    else:
        print("Continuing...")

while True:
    display_text = ""
    image = camera.capture_array("main")

    binary_image = filter_image(image)
    cv.imwrite("filtered.jpg", binary_image)
    tf_image = cv.cvtColor(binary_image, cv.COLOR_GRAY2RGB)

    display_text = "====== TensorFlow Status " + time.asctime() + " =====" + "\n"
    # classify with tflite model
    #tf_image = np.expand_dims(binary_image, axis=0)
    classification = Identify.run(tf_image, verbose=False)
    if (np.argmax(classification) == 0):
        display_text += "Print is failing!" + "\n"
        #user_prompt()
    else:
        display_text += "Print is successful!" + "\n"

    display_text += "====== OpenCV Status " + time.asctime() + " =========" + "\n"
    validity, difference = pixel.add(binary_image)

    if not validity == None:
        if not validity:
            display_text += "Pixel count failure! [{:.2f}]".format(difference) + "\n"
        else:
            display_text += "Pixel count is valid! [{:.2f}]".format(difference) + "\n"
        
    display_text += pixel.history_fitting() + "\n"
    display_text += "=========================================================" + "\n"

    os.system('cls' if os.name == 'nt' else 'clear')
    print(display_text)
    time.sleep(2)
