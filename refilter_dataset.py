import os
import sys
import cv2 as cv
import shutil

print(sys.argv[1])
dataset = sys.argv[1]

from opencv.pre_processing.filter import filter_image

folders = [f for f in os.listdir("./datasets/{}".format(dataset)) if "raw" in f] # keep folders with filtered in their names

for folder in folders:
    print("Processing folder: ./datasets/{}".format(folder))

    if "success" in folder:      
        pre_path = "./datasets/{}/success_".format(dataset)
        if os.path.isdir("./datasets/{}/success_filtered".format(dataset)):
            shutil.rmtree("./datasets/{}/success_filtered".format(dataset))
            os.mkdir("./datasets/{}/success_filtered".format(dataset))
        else:
            os.mkdir("./datasets/{}/success_filtered".format(dataset))
        if os.path.isdir("./datasets/{}/success_masked".format(dataset)):
            shutil.rmtree("./datasets/{}/success_masked".format(dataset))
            os.mkdir("./datasets/{}/success_masked".format(dataset))
        else:
            os.mkdir("./datasets/{}/success_masked".format(dataset))
    if "fail" in folder:
        pre_path = "./datasets/{}/fail_".format(dataset)
        if os.path.isdir("./datasets/{}/fail_filtered".format(dataset)):
            shutil.rmtree("./datasets/{}/fail_filtered".format(dataset))
            os.mkdir("./datasets/{}/fail_filtered".format(dataset))
        else:
            os.mkdir("./datasets/{}/fail_filtered".format(dataset))
        if os.path.isdir("./datasets/{}/fail_masked".format(dataset)):
            shutil.rmtree("./datasets/{}/fail_masked".format(dataset))
            os.mkdir("./datasets/{}/fail_masked".format(dataset))
        else:
            os.mkdir("./datasets/{}/fail_masked".format(dataset))

    for image_name in os.listdir("./datasets/{}/{}".format(dataset, folder)):
        image_path = ("./datasets/{}/{}").format(dataset, folder)
        if (os.path.isfile(os.path.join(image_path, image_name))):
            image_raw = cv.imread(os.path.join(image_path, image_name))
            image_filtered = filter_image(image_raw)
            print("Writing file: {}filtered/{}".format(pre_path, image_name))
            cv.imwrite("{}filtered/{}".format(pre_path, image_name), image_filtered)

            image_masked = cv.bitwise_and(image_raw, image_raw, mask=image_filtered)
            print("Writing file: {}masked/{}".format(pre_path, image_name))
            cv.imwrite("{}masked/{}".format(pre_path, image_name), image_masked)

print("Done")