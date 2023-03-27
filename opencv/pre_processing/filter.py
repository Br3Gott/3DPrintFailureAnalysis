import cv2 as cv
import numpy as np

img = cv.imread("./src/cv_input.png")
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

lower = np.array([0,113,113])
higher = np.array([179, 255, 255])

bin_img_data = cv.inRange(hsv, lower, higher)

cv.imwrite("./src/cv_output.png", bin_img_data)