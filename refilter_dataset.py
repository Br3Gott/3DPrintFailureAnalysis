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

    # Create folder structure for output.
    # If directory already exists remove directory and files.
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

    total_image_count = len(os.listdir("./datasets/{}/{}".format(dataset, folder)))
    current_image = 0

    # Go through all images, filter and mask them and place them in the correct folder.
    for image_name in os.listdir("./datasets/{}/{}".format(dataset, folder)):
        image_path = ("./datasets/{}/{}").format(dataset, folder)
        if (os.path.isfile(os.path.join(image_path, image_name))):
            image_raw = cv.imread(os.path.join(image_path, image_name))
            image_filtered, image_masked = filter_image(image_raw)
            sys.stdout.write("\033[K")
            current_image += 1
            print("Writing files {}% [{}/{}]: ({}filtered/{})".format(round((current_image/(total_image_count*2)) * 100), current_image, total_image_count*2, pre_path, image_name), end="\r")
            cv.imwrite("{}filtered/{}".format(pre_path, image_name), image_filtered)

            sys.stdout.write("\033[K")
            current_image += 1
            print("Writing files {}% [{}/{}]: ({}masked/{})".format(round((current_image/(total_image_count*2)) * 100), current_image, total_image_count*2, pre_path, image_name), end="\r")
            cv.imwrite("{}masked/{}".format(pre_path, image_name), image_masked)

print("Done")