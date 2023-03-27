import cv2 as cv
import time

from pre_processing.filter import filter_image
from pixel_observer.pixel import make_pixel

# Open videostream
camera_stream = cv.VideoCapture(0)
pixel = make_pixel(0.4, 50)

while True:
    #image = camera_stream.read()
    image = cv.imread("./pre_processing/src/cv_input.png")

    binary_image = filter_image(image)

    #classify
    #tensor.detect ...
    # takes time so simulate it
    time.sleep(0.5)

    print("====== OpenCV Status ", time.asctime(), " =====")
    if (not pixel.add(binary_image)):
        print("FAILED")
        exit()
        
    pixel.print_history_fitting()
    print("=====================================================")