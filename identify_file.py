from tensorflow.tensorflow_identify import Identify
import cv2 as cv

image = cv.imread("/home/pi/exjobb/datasets/benchy75/success_filtered/04-04-2023_07-57-02.jpg")

print(Identify.run(image, verbose=True))