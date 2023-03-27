import cv2 as cv
import numpy as np

def filter_image(input_url, output_url):
    img = cv.imread(input_url)
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    lower = np.array([0,113,113])
    higher = np.array([179, 255, 255])

    bin_img_data = cv.inRange(hsv, lower, higher)

    cv.imwrite(output_url, bin_img_data)