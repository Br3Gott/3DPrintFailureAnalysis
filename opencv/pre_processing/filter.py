import cv2 as cv
import numpy as np
import random

def filter_image_old(input_image):

    hsv = cv.cvtColor(input_image, cv.COLOR_BGR2HSV)

    #lower = np.array([0,113,113])
    #higher = np.array([179, 255, 255])
    # yellow
    # lower = np.array([20,113,113])
    # higher = np.array([110, 255, 255])
    # lower = np.array([5,115,94])
    # higher = np.array([110, 255, 255])

    #new good orange

    lower = np.array([10,150,132])
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

def filter_image(input_image):
    hsv = cv.cvtColor(input_image, cv.COLOR_BGR2HSV)

    #lower = np.array([0,113,113])
    #higher = np.array([179, 255, 255])
    # yellow
    # lower = np.array([20,113,113])
    # higher = np.array([110, 255, 255])
    # lower = np.array([5,115,94])
    # higher = np.array([110, 255, 255])

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
        masked = cv.bitwise_and(bin_img_data, stencil)
        masked = cv.bitwise_and(input_image, input_image, mask=masked)

        # print("Trying to get a point")
        # print(res)
        # print(res[0][0][0])
        # print(res[0][0][1])

        smallest_x = res[0][0][0]
        smallest_y = res[0][0][1]
        largest_x = res[0][0][0]
        largest_y = res[0][0][1]
        for point in res:
            # print(point)
            if point[0][0] < smallest_x: smallest_x = point[0][0]
            if point[0][0] > largest_x: largest_x = point[0][0]
            if point[0][1] < smallest_y: smallest_y = point[0][1]
            if point[0][1] > largest_y: largest_y = point[0][1]

        # print("sx {} sy {} lx {} ly {}".format(smallest_x, smallest_y, largest_x, largest_y))

        masked_cropped = masked[int(smallest_y+(largest_y-smallest_y)/2):largest_y, smallest_x:largest_x]
        masked_cropped = cv.cvtColor(masked_cropped, cv.COLOR_BGR2HSV)
        masked_shape = masked_cropped.shape
        masked_height = masked_shape[0]-1
        masked_width = masked_shape[1]-1

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

        # print("LH: {} LS: {} LV: {} HH: {} HS: {} HV: {}".format(lowest_h, lowest_s, lowest_v, highest_h, highest_s, highest_v))
        
        hsv = cv.cvtColor(input_image, cv.COLOR_BGR2HSV)

        # if lowest_h > 5: lowest_h -= 5
        # if lowest_s > 5: lowest_s -= 5
        # if lowest_v > 5: lowest_v -= 5

        # if highest_h < 240: highest_h += 5
        # if highest_s < 240: highest_s += 5
        # if highest_v < 240: highest_v += 5

        lower = np.array([lowest_h, lowest_s, lowest_v])
        higher = np.array([highest_h, highest_s, highest_v])

        bin_img_data = cv.inRange(hsv, lower, higher)

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

        #cv.imwrite("./output_linus_is_king.jpg", bin_img_data)
    

    return bin_img_data