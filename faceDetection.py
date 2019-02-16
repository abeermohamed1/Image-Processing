import numpy as np
import cv2
import os
# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades

#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

#cap = cv2.VideoCapture(0)
#
dic = "./people/"
outDic = "./peopleOut2/"


for filename in os.listdir(dic):
    if filename.endswith(".jpg"):
        imagename = filename
        img = cv2.imread(dic + imagename)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.25, 3)

        print "Found {0} faces!".format(len(faces))

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imwrite(outDic + imagename, img)
        cv2.waitKey(0)
        continue
    else:
        continue
