# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 23:26:02 2016

@author: herbz
"""

# import the necessary packages
import numpy as np
import cv2
#C:\Users\herbz\Anaconda3\Library\etc\haarcascades

face_cascade = cv2.CascadeClassifier('C:\\Users\\herbz\\Anaconda3\\Library\\etc\\haarcascades\\haarcascade_frontalface_alt.xml')

cap = cv2.VideoCapture(2)
#img = cv2.imread('C:\\Users\\herbz\\OneDrive - University Of Cambridge\\Documents\\GitHub\\PhD-python\\Python\\openCV\\test.png')
while(1):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()

