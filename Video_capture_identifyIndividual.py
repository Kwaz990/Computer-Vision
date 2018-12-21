import numpy as np
import cv2
from matplotlib import pyplot as plt
import sys
import time
import face_recognition


# Get user supplied values
cascPath = "haarcascade_frontalface_default.xml"

kwasi_image = face_recognition.load_image_file('./images/known_faces/Kwasi1.jpg')
unkown_image = face_recognition.load_image_file('./images/unkown_faces/SnapShot3.jpg')

video_capture = cv2.VideoCapture(0)


# Get the face encodings for each face in each image file
# Since there could be more than one face in each image, it returns a list of encodings.
# But since I know each image only has one face, I only care about the first encoding in each image, so I grab index 0.
try:
    kwasi_face_encoding = face_recognition.face_encodings(kwasi_image)[0]
    unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
    video_encoding = face_recognition.face_encodings(video_capture)[0]
except IndexError:
    print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
    quit()


known_faces = [
    kwasi_face_encoding
]


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

# results is an array of True/False telling if the unknown face matched anyone in the known_faces array
results = face_recognition.compare_faces(known_faces, unknown_face_encoding)



# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

img = cv2.imread("images/group-smiling.jpg",1)
#Fix for color differences in matplot lib compared to opencv
b,g,r = cv2.split(img)
img2 = cv2.merge([r,g,b])


while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()



    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
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




