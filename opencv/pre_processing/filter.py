import cv2 as cv
import numpy as np
import random
import math

def distance(point1x, point1y, point2x, point2y):
    return round(math.sqrt((point1x - point2x)**2 + (point1y - point2y)**2), 2)

def get_crop_values(res):
    smallest_x = res[0][0][0]
    smallest_y = res[0][0][1]
    largest_x = res[0][0][0]
    largest_y = res[0][0][1]
    for point in res:
        if point[0][0] < smallest_x: smallest_x = point[0][0]
        if point[0][0] > largest_x: largest_x = point[0][0]
        if point[0][1] < smallest_y: smallest_y = point[0][1]
        if point[0][1] > largest_y: largest_y = point[0][1]
    
    return smallest_x, smallest_y, largest_x, largest_y

def get_contour(bin_image):
    # contour filtering
    contours, _ = cv.findContours(bin_image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    length = len(contours)
    maxRatio = -1
    height, width = bin_image.shape
    centerx = width/2
    centery = height/2
    if length > 0:
        ci = -1
        for i in range(length):  # find the closest to center and biggest contour (according to area)
            temp = contours[i]
            area = cv.contourArea(temp)
            M = cv.moments(contours[i])
            if M['m00'] != 0:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                distancemiddle = distance(cx, cy, centerx, centery)
                if distancemiddle == 0:
                    ratio = 9999 # high value to prevent anything else
                    ci = i
                else:
                    ratio = area / distancemiddle

                if (ratio > maxRatio and distancemiddle < 1200 and area > 20000):
                    maxRatio = ratio
                    ci = i
        if ci != -1:
            res = contours[ci]
            # get convex hull from largest and most central contour
            hull = cv.convexHull(res)
            return res, hull
        else:
            return [], [] 
    else:
        return [], []

        
def split(image, width, height):
    return image[int(height/2):height, 0:width], image[0:int(height/2), 0:width]

def filter(image):
    lower = np.array([0,100,50])
    higher = np.array([255, 255, 255])

    return cv.inRange(image, lower, higher)

def filter_soft(image):
    light_hsv_higher = np.array([255, 255, 255])
    light_hsv_lower = np.array([0, 120, 100])
    
    return cv.inRange(image, light_hsv_lower, light_hsv_higher)

def filter_hard(image):
    hard_hsv_higher = np.array([255, 255, 255])
    hard_hsv_lower = np.array([0, 165, 150])

    return cv.inRange(image, hard_hsv_lower, hard_hsv_higher)

def filter_image(input_image):
    # convert image to hsv format
    hsv = cv.cvtColor(input_image, cv.COLOR_BGR2HSV)
    cv.imwrite("./hsv.jpg", hsv)

    # base hsv values for initail filtering
    # lower = np.array([0,100,50])
    # higher = np.array([255, 255, 255])

    # filter image based on inital values
    # bin_img_data = cv.inRange(hsv, lower, higher)
    bin_img_data = filter(hsv)

    # cv.imwrite("./firstfilter.jpg", bin_img_data)
    done_masked = np.zeros(bin_img_data.shape).astype(bin_img_data.dtype)

    # if no contour
    contours, hull = get_contour(bin_img_data)
    if len(contours) == 0:
        # print("No obj identified!")
        bin_img_data = np.zeros(bin_img_data.shape).astype(bin_img_data.dtype)
        return bin_img_data, done_masked
    
    stencil = np.zeros(bin_img_data.shape).astype(bin_img_data.dtype)
    contour_fill = [np.array(hull)]
    color = [255, 255, 255]
    cv.fillPoly(stencil, contour_fill, color)
    # create binary image using stencil
    masked = cv.bitwise_and(bin_img_data, stencil)
    # create masked image based on binary image (containing largest and most central contour)
    masked = cv.bitwise_and(input_image, input_image, mask=masked)

    smallest_x, smallest_y, largest_x, largest_y = get_crop_values(contours)

    # crop image and convert to hsv
    masked_cropped = masked[int(smallest_y+(largest_y-smallest_y)/2):largest_y, smallest_x:largest_x]
    masked_cropped = cv.cvtColor(masked_cropped, cv.COLOR_BGR2HSV)
    done_masked = masked_cropped

    hsv_cropped = hsv[smallest_y:largest_y, smallest_x:largest_x]

    hsv_shape = hsv_cropped.shape
    hsv_height = hsv_shape[0]-1
    hsv_width = hsv_shape[1]-1

    if hsv_height > 75:
        lower_hsv, higher_hsv = split(hsv_cropped, hsv_width, hsv_height)

        higher_bin = filter_hard(higher_hsv)

        lower_bin = filter_soft(lower_hsv)

        bin_img_data = np.concatenate((higher_bin, lower_bin), axis=0)

        contours, hull = get_contour(bin_img_data)

        if len(contours) > 0:
            smallest_x, smallest_y, largest_x, largest_y = get_crop_values(contours)
            bin_img_data = bin_img_data[smallest_y:largest_y, smallest_x:largest_x]

            
            contours, hull = get_contour(bin_img_data)
            if len(contours) > 0:
                stencil = np.zeros(bin_img_data.shape).astype(bin_img_data.dtype)
                contours = [np.array(hull)]
                color = [255, 255, 255]
                cv.fillPoly(stencil, contours, color)
                # create binary image using stencil
                bin_img_data =  cv.bitwise_and(bin_img_data, stencil)
            else:
                bin_img_data = np.zeros(bin_img_data.shape).astype(bin_img_data.dtype)
        else:
            bin_img_data = np.zeros(bin_img_data.shape).astype(bin_img_data.dtype)

    else:
        bin_img_data = filter_soft(hsv_cropped)

    cv.imwrite("./final.jpg", bin_img_data)
    return bin_img_data, done_masked