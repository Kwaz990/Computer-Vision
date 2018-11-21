import numpy as np
import cv2
from matplotlib import pyplot as plt
import sys


# Get user supplied values
cascPath = "haarcascade_frontalface_default.xml"


video_capture = cv2.VideoCapture(0)

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

img = cv2.imread("images/group-smiling.jpg",1)
#Fix for color differences in matplot lib compared to opencv
b,g,r = cv2.split(img)
img2 = cv2.merge([r,g,b])


while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
        #flags = cv2.CV_HAAR_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



print("Found {0} faces!".format(len(faces)))

video_capture.release()
if video_capture.isOpened() == False:
    video_capture.open()

cv2.destroyAllWindows()

#plt.imshow(frame, cmap = 'gray', interpolation = 'bicubic')
#plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
#plt.show()




