# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 00:26:51 2016

@author: herbz
"""

import numpy as np
import cv2

cap = cv2.VideoCapture(0)  # this is the number of camera

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)) # this is the windows size ? 

fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()
#fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()

while(1):
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    
    cv2.imshow('frame',fgmask)
    k = cv2.waitKey(25) & 0xff
    if k == 27: #esc
        break
    
    
cap.release()
cv2.destroyAllWindows()