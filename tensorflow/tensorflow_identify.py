import cv2 as cv
import numpy as np
from PIL.Image import fromarray 

import tflite_runtime.interpreter as tflite

class Identify:
    def run(input_image, verbose=False):

        TF_MODEL_FILE_PATH = '/home/pi/exjobb/tensorflow/model.tflite' # The default path to the saved TensorFlow Lite model

        interpreter = tflite.Interpreter(model_path=TF_MODEL_FILE_PATH)

        interpreter.get_signature_list()

        classify_lite = interpreter.get_signature_runner('serving_default')
        classify_lite

        new_img = cv.resize(input_image, (300, 300))
        new_img = new_img.astype(np.float32)
        new_img = np.expand_dims(new_img, axis=0)

        predictions_lite = classify_lite(sequential_input=new_img)["dense_1"]

        # calculate the softmax of a vector
        def softmax(vector):
            e = np.exp(vector)
            return e / e.sum()

        score_lite = softmax(predictions_lite)

        class_names = ["Fail", "Success"]


        if (verbose == True):
            print(
                "Is {} with a {:.2f} percent confidence."
                .format(class_names[0], 100 * score_lite[0][0])
            )

            print(
                "Is {} with a {:.2f} percent confidence."
                .format(class_names[1], 100 * score_lite[0][1])
            )


        return [score_lite[0][0]*100, score_lite[0][1]*100]