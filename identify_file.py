from tf.tensorflow_identify import Identify
import cv2 as cv

image = cv.imread("<path to file>")

print(Identify.run(image, verbose=True))