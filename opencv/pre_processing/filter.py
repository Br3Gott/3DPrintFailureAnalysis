import cv2 as cv
import numpy as np
import random
import math

def distance(point1x, point1y, point2x, point2y):
    return round(math.sqrt((point1x - point2x)**2 + (point1y - point2y)**2), 2)

def filter_image(input_image):
    
    # convert image to hsv format
    hsv = cv.cvtColor(input_image, cv.COLOR_BGR2HSV)

    # base hsv values for initail filtering
    lower = np.array([0,60,120])
    higher = np.array([255, 255, 255])

    # filter image based on inital values
    bin_img_data = cv.inRange(hsv, lower, higher)

    # contour filtering
    contours, _ = cv.findContours(bin_img_data, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    length = len(contours)
    maxRatio = -1
    height, width = bin_img_data.shape
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
                ratio = area / distancemiddle
                if (ratio > maxRatio and distancemiddle < 500):
                    maxRatio = ratio
                    ci = i
        if ci == -1:
            print("No obj identified!")
            bin_img_data = np.zeros(bin_img_data.shape).astype(bin_img_data.dtype)
        else:
            res = contours[ci]
            # get convex hull from largest and most central contour
            hull = cv.convexHull(res) 
            
            stencil = np.zeros(bin_img_data.shape).astype(bin_img_data.dtype)
            contours = [np.array(hull)]
            color = [255, 255, 255]
            cv.fillPoly(stencil, contours, color)
            # create binary image using stencil
            masked = cv.bitwise_and(bin_img_data, stencil)
            # create masked image based on binary image (containing largest and most central contour)
            masked = cv.bitwise_and(input_image, input_image, mask=masked)

            # map points from largest contour for cropping
            smallest_x = res[0][0][0]
            smallest_y = res[0][0][1]
            largest_x = res[0][0][0]
            largest_y = res[0][0][1]
            for point in res:
                if point[0][0] < smallest_x: smallest_x = point[0][0]
                if point[0][0] > largest_x: largest_x = point[0][0]
                if point[0][1] < smallest_y: smallest_y = point[0][1]
                if point[0][1] > largest_y: largest_y = point[0][1]

            # crop image and convert to hsv
            masked_cropped = masked[int(smallest_y+(largest_y-smallest_y)/2):largest_y, smallest_x:largest_x]
            masked_cropped = cv.cvtColor(masked_cropped, cv.COLOR_BGR2HSV)
            masked_shape = masked_cropped.shape
            masked_height = masked_shape[0]-1
            masked_width = masked_shape[1]-1

            # sampling colors within the upper parts of the largest and most central contour
            sampling_count = 25000
            sampling_points = []
            for x in range(0, sampling_count):
                point = [random.randint(0, masked_width), random.randint(0, masked_height)]
                sampling_points.append(masked_cropped[point[1]][point[0]])
            
            lowest_h = 255
            lowest_s = 255
            lowest_v = 255
            highest_h = 0
            highest_s = 0
            highest_v = 0
            for point in sampling_points:
                if point[2] != 0:
                    if point[0] < lowest_h: lowest_h = point[0]
                    if point[0] > highest_h: highest_h = point[0]
                    if point[1] < lowest_s: lowest_s = point[1]
                    if point[1] > highest_s: highest_s = point[1]
                    if point[2] < lowest_v: lowest_v = point[2]
                    if point[2] > highest_v: highest_v = point[2]

            # global offsets for hsv values
            # if lowest_h > 5: lowest_h -= 5
            # if lowest_s > 5: lowest_s -= 5
            # if lowest_v > 5: lowest_v -= 5

            # if highest_h < 240: highest_h += 5
            # if highest_s < 240: highest_s += 5
            # if highest_v < 240: highest_v += 5

            # sampled colors for largest and most central contour
            lower = np.array([lowest_h, lowest_s, lowest_v])
            higher = np.array([highest_h, highest_s, highest_v])

            bin_img_data = cv.inRange(hsv, lower, higher)

            # contour filtering
            contours, _ = cv.findContours(bin_img_data, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            length = len(contours)
            maxRatio = -1
            height, width = bin_img_data.shape
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
                        ratio = area / distancemiddle
                        if (ratio > maxRatio and distancemiddle < 500):
                            maxRatio = ratio
                            ci = i

                if ci == -1:
                    print("No obj identified after color sampling!")
                    bin_img_data = np.zeros(bin_img_data.shape).astype(bin_img_data.dtype)
                else:
                    res = contours[ci]
                    # get convex hull from largest and most central contour
                    hull = cv.convexHull(res)
                
                    stencil = np.zeros(bin_img_data.shape).astype(bin_img_data.dtype)
                    contours = [np.array(hull)]
                    color = [255, 255, 255]
                    cv.fillPoly(stencil, contours, color)

                    bin_img_data = cv.bitwise_and(bin_img_data, stencil)

    return bin_img_data