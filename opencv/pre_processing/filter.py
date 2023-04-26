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
                    maxRatio = 9999 # high value to prevent anything else
                    ci = i
                else:
                    ratio = area / distancemiddle

                if (ratio > maxRatio and distancemiddle < 500 and area > 500):
                    maxRatio = ratio
                    ci = i

        if ci != -1:
            res = contours[ci]
            # get convex hull from largest and most central contour
            hull = cv.convexHull(res)
            return res, hull
    print("error none!")
    return None
        

def filter_image(input_image):
    
    # convert image to hsv format
    hsv = cv.cvtColor(input_image, cv.COLOR_BGR2HSV)
    cv.imwrite("./hsv.jpg", hsv)

    # base hsv values for initail filtering
    lower = np.array([0,100,50])
    higher = np.array([255, 255, 255])

    # filter image based on inital values
    bin_img_data = cv.inRange(hsv, lower, higher)
    cv.imwrite("./firstfilter.jpg", bin_img_data)
    done_masked = np.zeros(bin_img_data.shape).astype(bin_img_data.dtype)

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
                if distancemiddle == 0:
                    maxRatio = 9999 # high value to prevent anything else
                    ci = i
                else:
                    ratio = area / distancemiddle

                if (ratio > maxRatio and distancemiddle < 500 and area > 500):
                    maxRatio = ratio
                    ci = i

        if ci == -1:
            # print("No obj identified!")
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
            cv.imwrite("./firstcontourremoval.jpg", masked)

            # map points from largest contour for cropping
            # smallest_x = res[0][0][0]
            # smallest_y = res[0][0][1]
            # largest_x = res[0][0][0]
            # largest_y = res[0][0][1]
            # for point in res:
            #     if point[0][0] < smallest_x: smallest_x = point[0][0]
            #     if point[0][0] > largest_x: largest_x = point[0][0]
            #     if point[0][1] < smallest_y: smallest_y = point[0][1]
            #     if point[0][1] > largest_y: largest_y = point[0][1]
            smallest_x, smallest_y, largest_x, largest_y = get_crop_values(res)

            # crop image and convert to hsv
            masked_cropped = masked[int(smallest_y+(largest_y-smallest_y)/2):largest_y, smallest_x:largest_x]
            masked_cropped = cv.cvtColor(masked_cropped, cv.COLOR_BGR2HSV)
            masked_shape = masked_cropped.shape
            masked_height = masked_shape[0]-1
            masked_width = masked_shape[1]-1

            #cv.drawContours(hsv, [res], 0, (0,255,0), 3)
            hsv_cropped = hsv[smallest_y:largest_y, smallest_x:largest_x]
            cv.imwrite("./firstcrop.jpg", hsv_cropped)


            hsv_shape = hsv_cropped.shape
            hsv_height = hsv_shape[0]-1
            hsv_width = hsv_shape[1]-1
            
            higher_hsv = hsv_cropped[0:int(hsv_height/2), 0:hsv_width]
            lower_hsv = hsv_cropped[int(hsv_height/2):hsv_height, 0:hsv_width]

            cv.imwrite("./higher.jpg", higher_hsv)
            cv.imwrite("./lower.jpg", lower_hsv)

            hard_hsv_higher = np.array([255, 255, 255])
            hard_hsv_lower = np.array([0, 200, 125])
            light_hsv_higher = np.array([255, 255, 255])
            light_hsv_lower = np.array([0, 120, 100])

            higher_bin = cv.inRange(higher_hsv, hard_hsv_lower, hard_hsv_higher)
            lower_bin = cv.inRange(lower_hsv, light_hsv_lower, light_hsv_higher)


            cv.imwrite("./higher.jpg", higher_bin)
            cv.imwrite("./lower.jpg", lower_bin)

            bin_img_data = np.concatenate((higher_bin, lower_bin), axis=0)
            cv.imwrite("./bin_img_data.jpg", bin_img_data)


            # DO AMAZING THINGS

            return bin_img_data, masked_cropped











            lower = np.array([0,100,80])
            higher = np.array([255, 255, 255])

           # filter image based on inital values
            bin_im2 = cv.inRange(input_cropped, lower, higher)
            cv.imwrite("./masked2.jpg", bin_im2)
            # Draw new contour.
            #res, hull = get_contour(bin_im2)
            # Black everything out that is not in contour.
            # We should now have a nice frame of our print.
            # Maybe crop all corners a little? :P
            # Maybe filter again with (a lot) less aggresive filtering?
            # Then finished? No sampling needed maybe?
            # OR We then sample and filter the cropped image again. We will see

            masked_cropped = cv.bitwise_and(input_cropped, input_cropped, mask=bin_im2)
            

            # sampling colors within the upper parts of the largest and most central contour
            sampling_count = 50000
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

            bin_img_data = cv.inRange(input_image_2, lower, higher)
            cv.imwrite("./aftersampling.jpg", bin_img_data)

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
                        if distancemiddle == 0:
                            maxRatio = 9999 # high value to prevent anything else
                            ci = i
                        else:
                            ratio = area / distancemiddle

                        if (ratio > maxRatio and distancemiddle < 500 and area > 1200):
                            maxRatio = ratio
                            ci = i

                if ci == -1:
                    # print("No obj identified after color sampling!")
                    bin_img_data = np.zeros(bin_img_data.shape).astype(bin_img_data.dtype)
                else:
                    res = contours[ci]
                    # get convex hull from largest and most central contour
                    hull = cv.convexHull(res)
                
                    stencil = np.zeros(bin_img_data.shape).astype(bin_img_data.dtype)
                    contours = [np.array(hull)]
                    color = [255, 255, 255]
                    cv.fillPoly(stencil, contours, color)

                    smallest_x, smallest_y, largest_x, largest_y = get_crop_values(res)

                    bin_img_data = cv.bitwise_and(bin_img_data, stencil)
                    masked_img_data = cv.bitwise_and(input_image_2, input_image_2, mask=bin_img_data)
                    bgr = cv.cvtColor(masked_img_data, cv.COLOR_HSV2BGR)
                    # cv.imwrite("./masked.jpg", bgr[smallest_y:largest_y, smallest_x:largest_x])
                    done_masked = bgr[smallest_y:largest_y, smallest_x:largest_x]
                    bin_img_data = bin_img_data[smallest_y:largest_y, smallest_x:largest_x]

    cv.imwrite("./final.jpg", bin_img_data)

    contours2, _ = get_contour(bin_img_data)
    cv.drawContours(bin_img_data, [contours2], 0, (0,255,0), 10)
    cv.drawContours(bin_img_data, [contours2], -1, (0, 255, 0), 3)

    cv.imwrite("./final2.jpg", bin_img_data)

    return bin_img_data, done_masked
    # return bin_im2, done_masked