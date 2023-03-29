import cv2 as cv
import numpy as np

import tflite_runtime.interpreter as tflite

# # old
# # Load the TFLite model and allocate tensors.
# interpreter = tflite.Interpreter(model_path="model.tflite")
# interpreter.allocate_tensors()

# # Get input and output tensors.
# input_details = interpreter.get_input_details()
# output_details = interpreter.get_output_details()
# print("input_details")
# print(input_details)
# print("output_details")
# print(output_details)

# # # Test the model on random input data.
# # #input_shape = input_details[0]['shape']
# # input_shape = interpreter.get_input_details()[0]
# # #input_data = np.array(np.random.random_sample(input_shape), dtype=np.float32)
# # # input_data = cv.imread("./test_input.png")
# # # interpreter.set_tensor(input_details[0]['index'], input_data)
# img = cv.imread("test_input.jpg")
# new_img = cv.resize(img, (224, 224))
# new_img = new_img.astype(np.float32)
# new_img = np.expand_dims(new_img, axis=0)
# interpreter.set_tensor(input_details[0]['index'], new_img)

# interpreter.invoke()

# # The function `get_tensor()` returns a copy of the tensor data.
# # Use `tensor()` in order to get a pointer to the tensor.
# output_data = interpreter.get_tensor(output_details[0]['index'])
# print(output_data)

TF_MODEL_FILE_PATH = 'model.tflite' # The default path to the saved TensorFlow Lite model

img_height = 180
img_width = 180

# sunflower_url = "https://storage.googleapis.com/download.tensorflow.org/example_images/592px-Red_sunflower.jpg"
# image_path = tf.keras.utils.get_file('Red_sunflower', origin=sunflower_url)
image_path = "test_input.jpg"

img = tf.keras.utils.load_img(
    image_path, target_size=(img_height, img_width)
)
img_array = tf.keras.utils.img_to_array(img)
img_array = tf.expand_dims(img_array, 0) # Create a batch

interpreter = tf.lite.Interpreter(model_path=TF_MODEL_FILE_PATH)
interpreter.get_signature_list()
classify_lite = interpreter.get_signature_runner('serving_default')
# classify_lite
predictions_lite = classify_lite(sequential_1_input=img_array)['outputs']
score_lite = tf.nn.softmax(predictions_lite)
print(
    "This image most likely belongs to {} with a {:.2f} percent confidence."
    .format(class_names[np.argmax(score_lite)], 100 * np.max(score_lite))
)