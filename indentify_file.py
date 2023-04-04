from tensorflow.tensorflow_identify import Indentify
import cv2 as cv

image = cv.imread("/home/pi/exjobb/datasets/benchy2/success_filtered/31-03-2023_08-46-26.jpg")

print(Indentify.run(image, verbose=True))