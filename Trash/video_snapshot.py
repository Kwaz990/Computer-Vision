import numpy as np
import cv2
from matplotlib import pyplot as plt
import sys
import time
import os


# Get user supplied values
cascPath = "haarcascade_frontalface_default.xml"

def takeSnapShotandSave():
    video_capture = cv2.VideoCapture(0)

    # Take 10 snapshots from video feed
    num = 0
    while num<10:

        # Create the haar cascade
        faceCascade = cv2.CascadeClassifier(cascPath)

        img = cv2.imread("images/group-smiling.jpg",1)
        #Fix for color differences in matplot lib compared to opencv
        b,g,r = cv2.split(img)
        img2 = cv2.merge([r,g,b])

        # Capture frame-by-frame
        ret, frame = video_capture.read()

        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = faceCascade.detectMultiScale(
            frame,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
            #flags = cv2.CV_HAAR_SCALE_IMAGE
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Declare path to save snapshot
        saveSnapPath = './snapShots'

        # Save image to saveSnapPath and increment num counter  
        cv2.imwrite(os.path.join(saveSnapPath,'SnapShot'+str(num)+'.jpg'),frame)
        

        num = num+1    

        # Display the resulting frame
        # Use 'q' to quite video
        cv2.imshow('video',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Us cv2.waitkay(x) where x is the time in milliseconds before incrementing counter.
        # Note that an x value of 0 indicates wait forever
        cv2.waitKey(3000)



    print("Found {0} faces!".format(len(faces)))

    video_capture.release()
    if video_capture.isOpened() == False:
        video_capture.open()

    cv2.destroyAllWindows()

#plt.imshow(frame, cmap = 'gray', interpolation = 'bicubic')
#plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
#plt.show()

if __name__ == "__main__":
    takeSnapShotandSave()


