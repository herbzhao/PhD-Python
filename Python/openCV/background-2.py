# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 00:35:34 2016

@author: herbz
"""

import numpy as np
import cv2

cap = cv2.VideoCapture('C:\\Users\\herbz\\OneDrive - University Of Cambridge\\Documents\\GitHub\\PhD-python\\Python\\openCV\\droplet.avi')

fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()

while(1):
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame)

    cv2.imshow('frame',fgmask)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()