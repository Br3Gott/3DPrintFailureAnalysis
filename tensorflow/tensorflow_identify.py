import cv2 as cv
import numpy as np

import tflite_runtime.interpreter as tflite

class Indentify:
    def run(input_image, verbose=False):

        # Load the TFLite model and allocate tensors.
        interpreter = tflite.Interpreter(model_path="./tensorflow/model.tflite")
        class_names = ["Fail", "Success"]
        interpreter.allocate_tensors()

        # Get input and output tensors.
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        if verbose:
            print("input details")
            print(input_details)
            print("output details")
            print(output_details)

        # Load input image and set input tensor
        # img = cv.imread("./tensorflow/test_input.jpg")
        img = input_image
        new_img = cv.resize(img, (180, 180))
        new_img = new_img.astype(np.float32)
        # temp fix for binary image
        new_img = cv.cvtColor(new_img, cv.COLOR_GRAY2RGB)
        new_img = np.expand_dims(new_img, axis=0)

        interpreter.set_tensor(input_details[0]['index'], new_img)

        # Invoke tflite interpreter
        interpreter.invoke()

        # Fetch output data from tensor
        output_data = interpreter.get_tensor(output_details[0]['index'])

        # Pretty print result
        if verbose:
            print(
                "This image most likely belongs to {} with a {:.2f} percent confidence."
                .format(class_names[np.argmax(output_data)], 100 * np.max(output_data))
            )

        return class_names[np.argmax(output_data)]