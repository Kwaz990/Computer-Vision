import numpy as np
import cv2
from matplotlib import pyplot as plt
import sys
import os
import datetime
from app import db
from app.models import Person, User
from random import randint


## This script analyizes pictureds found in a specified directory
# and determines if a face is found. If a face is found it will commit info to the dbs  ew34`2 

# Get user supplied values
#image = ("Pretty_Asians.png", 0)
cascPath = "haarcascade_frontalface_default.xml"






# establish database credentials

## def connect():
#    global dbname
#    dbname = '/groupfrontend/app.db'
#    global connection
#    connection = sqlite3.connect(dbname)
#    global cursor
#    cursor=connection.cursor()
#    return connection, cursor


#def close(connection, cursor):
#    connection.commit()
#    cursor.close()
#    connection.close()




moodrating = randint(1,5)
facesBoolean = None
expressionInteger = 0
timeStamp = datetime.datetime.now()






#function to commit facial expression integer (a 1-5 integer) and boolean for face detected.
def commitFacialData(facesBoolean,expressionInteger,timeStamp):
    #connection, cursor = connect()
    face = facesBoolean
    mood = expressionInteger
    time = timeStamp
   # currentuser = User.query.filter_by(username=current_user.username).first()
    #api_key = random.randint(10000, 99000)
    #SQL2 = '''INSERT INTO Person (mood, timestamp, faceBoolean) VALUES(?, ?, ?, ?)'''
 # values2 = (mood, time, face)
    newFacialData = Person(timestamp = time, mood = expressionInteger, faceBoolean = facesBoolean, user_id = 1)  
    #cursor.execute(SQL2, values2)
    #close(connection, cursor)
    db.session.add(newFacialData)
    db.session.commit()
    print(True)
    return True





# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

snaps = os.listdir('snapShots')
counter = 0






while counter < 2:
#while counter < len(snaps): 
    for file in snaps:
        if file.endswith(".jpg"):
            i = file


#snap_files = [f for f in snaps if os.path.isfile(os.path.join(snaps, f))]
        #for i in snap_files:

            img = cv2.imread('snapShots/{}'.format(i))
#img = cv2.imread("images/group-smiling.jpg",1)
#Fix for color differences in matplot lib compared to opencv
            b,g,r = cv2.split(img)
            img2 = cv2.merge([r,g,b])

# Detect faces in the image
            faces = faceCascade.detectMultiScale(
            img2,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        #flags = cv2.CV_HAAR_SCALE_IMAGE
            )





# Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(img2, (x, y), (x+w, y+h), (0, 255, 0), 2)



                print("Found {0} faces!".format(len(faces)))

                #if 1 or more faces are detected make a db commit with boolean value and ineger value for facial expression
                if len(faces) > 0:
                    facesBoolean = True
                    expressionInteger += moodrating
                    commitFacialData(facesBoolean,expressionInteger,timeStamp)







                plt.imshow(img2, cmap = 'gray', interpolation = 'bicubic')
                plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
                plt.show()
                counter +=1
                print('there are {} snapshots'.format(len(snaps)))
                print('counter = {}'.format(counter))
                print('filename is {}'.format(i))




# Read the image
#pretty_asians = cv2.imread("./images/Pretty_Asians.png")
#gray = cv2.cvtColor(pretty_asains, cv2.COLOR_BGR2GRAY)








#cv2.imshow("Faces found", pretty_asains)
#cv2.waitKey(0)
