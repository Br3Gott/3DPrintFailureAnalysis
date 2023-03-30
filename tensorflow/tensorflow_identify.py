import cv2 as cv
import numpy as np

import tflite_runtime.interpreter as tflite

# Load the TFLite model and allocate tensors.
interpreter = tflite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load input image and set input tensor
img = cv.imread("test_input2.jpg")
new_img = cv.resize(img, (180, 180))
new_img = new_img.astype(np.float32)
new_img = np.expand_dims(new_img, axis=0)
interpreter.set_tensor(input_details[0]['index'], new_img)

# Invoke tflite interpreter
interpreter.invoke()

# Fetch output data from tensor
output_data = interpreter.get_tensor(output_details[0]['index'])

# Pretty print result
class_names = ["Fail", "Success"]
print(
    "This image most likely belongs to {} with a {:.2f} percent confidence."
    .format(class_names[np.argmax(output_data)], 100 * np.max(output_data))
)