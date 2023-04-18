import cv2 as cv
import numpy as np

def filter_image(input_image):
    hsv = cv.cvtColor(input_image, cv.COLOR_BGR2HSV)

    #lower = np.array([0,113,113])
    #higher = np.array([179, 255, 255])
    # yellow
    # lower = np.array([20,113,113])
    # higher = np.array([110, 255, 255])
    # lower = np.array([5,115,94])
    # higher = np.array([110, 255, 255])

    #new good orange
    lower = np.array([0,80,100])
    higher = np.array([255, 255, 255])

    bin_img_data = cv.inRange(hsv, lower, higher)

    # contour filtering
    contours, hierarchy = cv.findContours(bin_img_data, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) #detecting contours
    length = len(contours)
    maxArea = -1
    if length > 0:
        for i in range(length):  # find the biggest contour (according to area)
            temp = contours[i]
            area = cv.contourArea(temp)
            if area > maxArea:
                maxArea = area
                ci = i

        res = contours[ci]
        hull = cv.convexHull(res) #applying convex hull technique
        
        stencil = np.zeros(bin_img_data.shape).astype(bin_img_data.dtype)
        contours = [np.array(hull)]
        color = [255, 255, 255]
        cv.fillPoly(stencil, contours, color)
        bin_img_data = cv.bitwise_and(bin_img_data, stencil)

    return bin_img_data