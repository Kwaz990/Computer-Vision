import numpy as np
import cv2
from matplotlib import pyplot as plt
import sys


# Get user supplied values
#image = ("Pretty_Asians.png", 0)
cascPath = "haarcascade_frontalface_default.xml"


#img = cv2.imshow("abba.png", 0)

#cv2.waitKey(0) # it waits for any key to be pressed to execute next step

#cv2.destroyAllWindows()


# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

img = cv2.imread("abba.png",0)

# Detect faces in the image
faces = faceCascade.detectMultiScale(
    img,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30)
    #flags = cv2.CV_HAAR_SCALE_IMAGE
)

# Draw a rectangle around the faces
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)



print("Found {0} faces!".format(len(faces)))





plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.show()




# Read the image
#pretty_asians = cv2.imread("./images/Pretty_Asians.png")
#gray = cv2.cvtColor(pretty_asains, cv2.COLOR_BGR2GRAY)








#cv2.imshow("Faces found", pretty_asains)
#cv2.waitKey(0)
