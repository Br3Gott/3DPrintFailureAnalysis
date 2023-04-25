import os
import shutil
import sys
import tarfile
import cv2 as cv

with open('./datasets/dataset_folders.txt', 'r') as f:
    dataset_folders = [line.rstrip() for line in f]

output_file = sys.argv[1]

if len(sys.argv) > 2 and sys.argv[2] == "filter":
    #filter all input datasets
    print("Dataset filter selected, starting...")
    from opencv.pre_processing.filter import filter_image

    for folder_name in dataset_folders:

        folders = [f for f in os.listdir("./datasets/{}".format(folder_name)) if "raw" in f] # keep folders with filtered in their names

        for folder in folders:
            print("Processing folder: ./datasets/{}".format(folder))

            if "success" in folder:      
                pre_path = "./datasets/{}/success_".format(folder_name)
                if os.path.isdir("./datasets/{}/success_filtered".format(folder_name)):
                    shutil.rmtree("./datasets/{}/success_filtered".format(folder_name))
                    os.mkdir("./datasets/{}/success_filtered".format(folder_name))
                else:
                    os.mkdir("./datasets/{}/success_filtered".format(folder_name))
            if "fail" in folder:
                pre_path = "./datasets/{}/fail_".format(folder_name)
                if os.path.isdir("./datasets/{}/fail_filtered".format(folder_name)):
                    shutil.rmtree("./datasets/{}/fail_filtered".format(folder_name))
                    os.mkdir("./datasets/{}/fail_filtered".format(folder_name))
                else:
                    os.mkdir("./datasets/{}/fail_filtered".format(folder_name))

            total_image_count = len(os.listdir("./datasets/{}/{}".format(folder_name, folder)))
            current_image = 0
            for image_name in os.listdir("./datasets/{}/{}".format(folder_name, folder)):
                image_path = ("./datasets/{}/{}").format(folder_name, folder)
                if (os.path.isfile(os.path.join(image_path, image_name))):
                    image_raw = cv.imread(os.path.join(image_path, image_name))
                    image_filtered, image_masked = filter_image(image_raw)
                    sys.stdout.write("\033[K")
                    current_image += 1
                    print("Writing files {}% [{}/{}]: ({}filtered/{})".format(round((current_image/(total_image_count*2)) * 100), current_image, total_image_count*2, pre_path, image_name), end="\r")
                    cv.imwrite("{}filtered/{}".format(pre_path, image_name), image_filtered)
                    sys.stdout.write("\033[K")
                    

os.mkdir("./datasets/{}".format(output_file))
os.mkdir("./datasets/{}/fail".format(output_file))
os.mkdir("./datasets/{}/success".format(output_file))

print(dataset_folders)
for dataset in dataset_folders:
    print("Adding dataset: ./datasets/{}".format(dataset))

    folders = [f for f in os.listdir("./datasets/{}".format(dataset)) if "filtered" in f] # keep folders with filtered in their names

    for folder in folders:
        print("Processing folder: ./datasets/{}/{}".format(dataset, folder))
        
        pre_path = "./datasets/{}/success/".format(output_file)
        if "fail" in folder:
            pre_path = "./datasets/{}/fail/".format(output_file)

        for image_name in os.listdir("./datasets/{}/{}".format(dataset, folder)):
            image_path = ("./datasets/{}/{}").format(dataset, folder)
            if (os.path.isfile(os.path.join(image_path, image_name))):
                shutil.copy(os.path.join(image_path, image_name), os.path.join(pre_path, image_name))

print("Finished copying images")

print("Compressing image folder")
with tarfile.open("./datasets/{}.tar.gz".format(output_file), "w:gz") as tar:
    tar.add("./datasets/{}".format(output_file), arcname=os.path.basename("./datasets/{}".format(output_file)))

print("Removing temporary folder")
shutil.rmtree("./datasets/{}".format(output_file))

print("Finished! Result: /datasets/{}.tar.gz".format(output_file))
