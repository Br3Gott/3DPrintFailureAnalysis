# Running testsuite should:
# * Look through the data folder for testcases.
# * Run all testcases with the given model.
# * Return stats on how it performs.

import json
import os
import cv2 as cv
import numpy as np

from opencv.pre_processing.filter import filter_image
from opencv.pixel_observer.pixel import make_pixel

import tensorflow as tf
from tensorflow import keras

def identify_testsuite(img):
    TF_MODEL_FILE_PATH = "./tf/model.tflite"  # The default path to the saved TensorFlow Lite model

    interpreter = tf.lite.Interpreter(model_path=TF_MODEL_FILE_PATH)

    interpreter.get_signature_list()

    classify_lite = interpreter.get_signature_runner("serving_default")
    classify_lite

    new_img = cv.resize(img, (300, 300))
    new_img = new_img.astype(np.float32)
    new_img = np.expand_dims(new_img, axis=0)

    predictions_lite = classify_lite(sequential_input=new_img)["dense_1"]

    # calculate the softmax of a vector
    def softmax(vector):
        e = np.exp(vector)
        return e / e.sum()

    score_lite = softmax(predictions_lite)

    if (score_lite[0][0] < score_lite[0][1]):
        return False
    return True

print("+-------------------------------------------------------------------+")
print("| Testsuite for Print Observer.                                     |")
print("| These tests will test the entire softwares functionality.         |")
print("| It will do this by similating a print going through the software. |")
print("| It tests both filtering and detection.                            |")
print("+-------------------------------------------------------------------+")

results = []

testcases = os.listdir("./testsuite/data")
print("List of tests to run: {}".format(testcases))

for testcase in testcases:
    # Load dataset values.
    data_file = open("./testsuite/data/{}/data.json".format(testcase))
    data = json.load(data_file)

    print("==== Currently Testing ====")
    print("Name: {}".format(data["name"]))
    print("Description: {}".format(data["description"]))

    image_names = os.listdir("./testsuite/data/{}/images".format(testcase))
    # print("Available Images: {}".format(image_names))

    # Loop through images, do the entire process
    # keep track of fails / success
    fail_boundary = data["fail_boundary"]
    passing_boundary = data["passing_boundary"]
    history = [True, True, True, True, True]
    failed = {
        "failed": None,
        "failed_at_layer": None
    }

    for i, image in enumerate(image_names):
        # print(i)
        # print(image)
        img_name = image
        image = cv.imread("./testsuite/data/{}/images/{}".format(testcase, image))
        binary_image, masked_image = filter_image(image)
        tf_image = cv.cvtColor(binary_image, cv.COLOR_GRAY2RGB)
        if identify_testsuite(tf_image) == False:
            # Big success
            # print("Success")
            history.pop(0)
            history.append(True)
        else:
            # Big fail
            # print("Fail")
            history.pop(0)
            history.append(False)
            print("Failed: {}".format(img_name))
            # cv.imwrite("./{}_out.jpg".format(img_name), tf_image)

        # print(sum(history))
        if sum(history) < 3:
            # We failed
            failed["failed"] = True
            failed["failed_at_layer"] = i
            break
    
    print("===== Testing Results =====")

    if failed["failed"] and failed["failed_at_layer"] > data["fail_boundary"] and data["passing_boundary"] > failed["failed_at_layer"]:
        print("Result: SUCCESS.")
        results.append({
            "testcase:": data["name"],
            "result": True,
            "lower_layer": data["fail_boundary"],
            "actual_layer": failed["failed_at_layer"],
            "higher_layer": data["passing_boundary"]
        })
    elif not failed["failed"] and not data["fail_boundary"]:
        print("Result: SUCCESS.")
        results.append({
            "testcase:": data["name"],
            "result": True,
            "lower_layer": data["fail_boundary"],
            "actual_layer": failed["failed_at_layer"],
            "higher_layer": data["passing_boundary"]
        })
    else:
        print("Result: FAILED.")
        results.append({
            "testcase:": data["name"],
            "result": False,
            "lower_layer": data["fail_boundary"],
            "actual_layer": failed["failed_at_layer"],
            "higher_layer": data["passing_boundary"]
        })
    
    if len(results) > 0:
        print(results[len(results)-1])
    if False:
        print("Raw Data:")
        if data["fail_boundary"]:
            print("Should fail after: {}".format(data["fail_boundary"]))
            print("Should fail before: {}".format(data["passing_boundary"]))
        else:
            print("Should not fail.")

        if failed["failed"]:
            print("Observer observed failure at: {}".format(failed["failed_at_layer"]))
        else:
            print("Observer did not observe any failure.")

    print("===========================")

success_count = 0
for result in results:
    if result["result"] == True:
        success_count += 1

print("+=========================+")
print("|    TestSuite Summary    |")
print("+=========================+")
print("Performed {} testruns".format(len(results)))
print("{} tests succeeded".format(success_count))
print("{} tests failed".format(len(results)-success_count))