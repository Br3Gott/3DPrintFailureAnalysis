# Thesis in Computer Science and Engineering

## Utilizing Computer Vision and Machine Learning to detect and handle 3D printing failures autonomously with a limited dataset.

***

## Bachelor Thesis in Computer Science by Linus Thorsell and David Sohl at Linköping University.

***

### Thesis Research Question

How can we utilize computer vision and machine learning
to detect and handle 3D printing failures autonomously
with a limited training dataset?

***

### Introduction to thesis

3D-Printers and their additive manufacturing methods have become quite popular during the last decade and are a great way of prototyping products. Additive manufacturing works by layering melted plastic to create intricate 3D parts where almost anything can be created. Even if 3D printing sounds like a simple process a lot of things can go wrong and many factor are at play during printing. During additive manufacturing the printing process often produce some byproducts such as toxic fumes from melting plastics at high temperatures, 3D printers are therefore recommended to be kept in well ventilated areas and away from people. Due to these high temperatures in 3D printing there are risks for electrical, material and mechanical fires. This requires printers to be regularly monitored, so that they do not catch fire while unattended. This presents a problem where it is not recommended to inhale the printing fumes but require you to be observant for errors. Emerging technologies regarding computer vision and artificial intelligence promises to allow for automating tasks that have previously required a human. Such task are for example monitoring the printing progress of a 3D printer.

Another central issue of current 3D printing technology is that creating detailed and larger models can take a very long time, this is another motivating factor for creating an autonomous system that can monitor the system in its entirety, since it is neither cost effective nor healthy for personnel to watch over the printer during the long print jobs.

### Keep reading the full thesis here: INSERT LINK
***

# Technical Documentation

### Hardware
* Computer: Raspberry Pi 3 B+ (1GB RAM)
* Camera: Raspberry Pi Camera Module CSI-2
* Lighting: Desk lamp and a plastic sheet to diffuse the light.
* 3D Printer: Creality Ender 3

### Software
* Image Processing: OpenCV 4.2.0
* Machine Learning: TensorFlow 2.11.0

### User Guide
Pre-Requisites
* Get a 3D printer similar to the Creality Ender 3 a Raspberry Pi 3B or newer and a Raspberry Pi Camera module.
* Print the hardware mount parts in `/hardware`.

Hardware setup
* Plug in Raspberry Pi Camera module into the camera port on the Raspberry Pi.
* Mount Camera and Raspberry Pi in the provided hardware mount.
* Plug the Raspberry Pi into USB port of printer controller.
* Power the Raspberry Pi with a verified Raspberry Pi power source such as the included power adapter.

Software setup
* Clone repository.
* Install dependencies using `./setup.sh` while in the root directory of the repository.
* Run the program using `./run.py`.
* Visit [localhost:9000](https://localhost:9000/).
* Follow the rest of the guide in your browser.

***

### Contributions to this specific repository are not going to be accepted. But feel free to fork the project for personal use.