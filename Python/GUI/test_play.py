# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 08:16:46 2016

@author: herbz
"""

import numpy as np
import cv2

#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('C:/Users/herbz/OneDrive - University Of Cambridge/Documents/GitHub/PhD-python/Python/GUI/droplet.avi')

while(cap.isOpened()):
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
