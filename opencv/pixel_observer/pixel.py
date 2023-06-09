import cv2 as cv
import numpy as np
import time

class Pixel:
    def __init__(self, error_margin=0.4, history_length=50):
        self.error_margin = error_margin
        self.history_length = history_length
        self.history_pixels = []
        self.history_time = []
        self.start_time = None
        self.fit_a = None
        self.fit_b = None

    def add(self, binary_image):
        if (not self.start_time):
            self.start_time = time.time()
            print("Start time ", self.start_time)

        pixel_count = cv.countNonZero(binary_image)
        current_delta_time = time.time()-self.start_time

        validity, difference = self.is_valid(current_delta_time, pixel_count)

        self.history_pixels.append(pixel_count)
        self.history_time.append(current_delta_time)

        if len(self.history_pixels) > self.history_length:
            self.history_pixels.pop(0)
            self.history_time.pop(0)

        return validity, difference

    def print_history_values(self):
        print(self.history_time)
        print(self.history_pixels)
    
    def history_fitting(self):
        if self.fit_a == None:
            return "Collecting data for prediction..."
        else:
            return "{:.2f}".format(self.fit_a) + " * x + " + "{:.2f}".format(self.fit_b)

    def is_valid(self, next_time, next_pixels):
        if len(self.history_time) < self.history_length:
            return None, 0

        self.fit_a, self.fit_b = np.polyfit(self.history_time, self.history_pixels, 1)

        expected_next = self.fit_a*next_time+self.fit_b
        difference = abs(expected_next-next_pixels)
        #print("Difference: {:.2f} ".format(difference))
        
        if difference > 100:
            return False, difference
        return True, difference

def make_pixel(error_margin, history_length):
    return Pixel(error_margin, history_length)