# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 08:02:42 2016

@author: herbz
"""

import numpy as np
import cv2

#cap = cv2.VideoCapture('C:\\Users\\herbz\\OneDrive - University Of Cambridge\\Documents\\GitHub\\PhD-python\\Python\\openCV\\output.avi')

cap = cv2.VideoCapture(0)

#recrod video
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('result.avi',fourcc,20.0,(640,480))


while(1):
    
    ret, frame = cap.read()
    #print(ret)
#    out.write(frame)  # record video
    cv2.imshow('frame',frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
#out.release()
cv2.destroyAllWindows()