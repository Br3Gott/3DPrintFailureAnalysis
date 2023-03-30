import cv2
from filter import filter_image

vidcap = cv2.VideoCapture('1.mp4')
success,image = vidcap.read()
count = 0
while success:
  cv2.imwrite("./frames/frame%d.jpg" % count, filter_image(image))     # save frame as JPEG file      
  
  for i in range(0, 10):
    success,image = vidcap.read()
  
  print('Read a new frame: ', success)
  count += 1