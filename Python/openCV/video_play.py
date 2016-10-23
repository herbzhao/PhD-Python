# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 08:02:42 2016

@author: herbz
"""

import numpy as np
import cv2

cap = cv2.VideoCapture('C:\\Users\\herbz\\OneDrive - University Of Cambridge\\Documents\\GitHub\\PhD-python\\Python\\openCV\\droplet.mp4')

while(1):
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame',gray)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()