import numpy as np
import cv2
from matplotlib import pyplot as plt
import sys
import os
import datetime
import time




cv2.namedWindow("preview")
vc = cv2.VideoCapture(cv2.CAP_DSHOW)
#vc = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
facedict = {}
emotions =["anger","disgust","fear","happy","neutral","sad","surprise"]
#To crop face in an image
def crop_face(clahe_image, face):
    for (x, y, w, h) in face:
        faceslice = clahe_image[y:y+h, x:x+w]
        faceslice = cv2.resize(faceslice, (350, 350))
    facedict["face%s" %(len(facedict)+1)] = faceslice
    return faceslice
def build_set(emotions):
    check_folders(emotions)
    for i in range(0, len(emotions)):
        save_face(emotions[i])
    print("Great,You are Done!" )
    cv2.destroyWindow("preview")
    cv2.destroyWindow("webcam")
#To check if folder exists, create if doesnt exists
def check_folders(emotions): 
    for x in emotions:
        if os.path.exists("dataset\\%s" %x):
            pass
        else:
            os.makedirs("dataset\\%s" %x)
#To save a face in a particular folder
def save_face(emotion):
    print("\n\nplease look " + emotion)
#To create timer to give time to read what emotion to express
    for i in range(0,5):
        print(5-i)
        time.sleep(1)
    #To grab 50 images for each emotion of each person
    while len(facedict.keys()) < 51: 
        open_webcamframe()
    #To save contents of dictionary to files
    for x in facedict.keys(): 
        cv2.imwrite("dataset_set\\%s\\%s.jpg" %(emotion,  len(glob.glob("dataset\\%s\\*" %emotion))), facedict[x])
    facedict.clear() #clear dictionary so that the next emotion can be stored
def open_webcamframe():
    counter = 0 
    while counter < len(emotions):
        rval, frame = vc.read()
        if rval ==False:
            print('Frame is empty...Error')
            cv2.imshow("preview", frame)
            key = cv2.waitKey(40)
            if key == 27: # exit on ESC
                print(key)
                break
        if vc.isOpened(): # try to get the first frame
            rval, frame = vc.read()
            print("Frame full...")
            #To convert image into grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            clahe_image = clahe.apply(gray)
           #To run classifier on frame
            face = face_cascade.detectMultiScale(clahe_image, scaleFactor=1.1, minNeighbors=15, minSize=(10, 10), flags=cv2.CASCADE_SCALE_IMAGE)
           #To draw rectangle around detected faces
            for (x, y, w, h) in face: 
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2) #draw it on "frame", (coordinates), (size), (RGB color), thickness 2
#Use simple check if one face is detected, or multiple (measurement error unless multiple persons on image)
                if len(face) == 1: 
                    faceslice = crop_face(clahe_image, face)
                    cv2.imshow("webcam", frame)
                    counter +=1
                return faceslice#slice face from image
           
            else:
                counter +=1 
                print("no/multiple faces detected, passlsing over frame")
    cv2.destroyWindow("preview")
    cv2.destroyWindow("webcam")
build_set(emotions)

# Transfer learning using VGG-16
img_width, img_height = 350, 350
top_model_weights_path = 'bottleneck_fc_model.h5'
train_data_dir = 'dataset'
nb_train_samples = 1011
epochs = 50
batch_size = 1
def save_bottlebeck_features():
    #Function to compute VGG-16 CNN for image feature extraction.
    train_target = []
    
    datagen = ImageDataGenerator(rescale=1. / 255)
    # build the VGG16 network
    model = applications.VGG16(include_top=False,weights='imagenet')
    generator_train = datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode=None,
        shuffle=False)
    
    for i in generator_train.filenames:
        train_target.append(i[:])
bottleneck_features_train = model.predict_generator(generator_train, nb_train_samples // batch_size)
   
bottleneck_features_train = bottleneck_features_train.reshape(1011,51200)
    
   
np.save(open('data_features.npy', 'wb'), bottleneck_features_train)
np.save(open('data_labels.npy', 'wb'), np.array(train_target))
save_bottlebeck_features()