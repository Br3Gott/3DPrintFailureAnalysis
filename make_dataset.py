import os
import shutil
import sys
import tarfile

output_file = sys.argv[1]

with open('./datasets/dataset_folders.txt', 'r') as f:
    dataset_folders = [line.rstrip() for line in f]

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
