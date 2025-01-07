# Bachelors Thesis in Computer Science and Engineering

## Utilizing Computer Vision and Machine Learning to detect and handle 3D printing failures autonomously with a limited dataset.
Bachelor Thesis in Computer Science by Linus Thorsell and David Sohl at Linköping University.

### Thesis Research Question

How can we utilize computer vision and machine learning
to detect and handle 3D printing failures autonomously
with a limited training dataset?

***

### Thesis Introduction

3D-Printers and their additive manufacturing methods have become quite popular during the last decade and are a great way of prototyping products. Additive manufacturing works by layering melted plastic to create intricate 3D parts where almost anything can be created. Even if 3D printing sounds like a simple process a lot of things can go wrong and many factor are at play during printing. During additive manufacturing the printing process often produce some byproducts such as toxic fumes from melting plastics at high temperatures, 3D printers are therefore recommended to be kept in well ventilated areas and away from people. Due to these high temperatures in 3D printing there are risks for electrical, material and mechanical fires. This requires printers to be regularly monitored, so that they do not catch fire while unattended. This presents a problem where it is not recommended to inhale the printing fumes but require you to be observant for errors. Emerging technologies regarding computer vision and artificial intelligence promises to allow for automating tasks that have previously required a human. Such task are for example monitoring the printing progress of a 3D printer.

Another central issue of current 3D printing technology is that creating detailed and larger models can take a very long time, this is another motivating factor for creating an autonomous system that can monitor the system in its entirety, since it is neither cost effective nor healthy for personnel to watch over the printer during the long print jobs.

### Keep reading the full thesis here: [Google Drive Document](https://drive.google.com/file/d/1CYKXol5aLj0p3fodsFr81RXP4OuGD8Eu/view?usp=sharing)
***

# Files
[Datasets](https://files.havre.dev/FailureAnalysis/datasets/)
[Testcases](https://files.havre.dev/FailureAnalysis/testcases/)
[ISO Image]()
***

# Usage
Download the [ISO Image]() and flash it on the Raspberry Pi.

Start the Raspberry Pi.

Connect to the Raspberry Pi using `ssh pi@<Raspberry Pi IP>` and input password `raspberry`.

Change the default password.

Create and input the required constants in the `constants.py` in the root directory of the project.

Restart the Raspberry Pi.

Open the OctoPrint control panel at: `<Raspberry Pi IP>`

Change the Webcam URL link to: `http://<Raspberry Pi IP>:8080/video`

Press `Activate` in the `Failure Analysis` tab to start monitoring.

Enjoy safe printing!

### Contributions to this specific repository are not going to be accepted. But feel free to fork the project for personal use.
