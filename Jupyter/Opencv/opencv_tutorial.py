# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 00:03:29 2016

@author: Herbee
"""


import numpy as np
import cv2
from matplotlib import pyplot as plt


#load img
img = cv2.imread('cam.jpg',0)


cv2.namedWindow('figure', cv2.WINDOW_NORMAL)  #WINDOW_AUTOSIZE
cv2.imshow('figure',img)
cv2.waitKey(0)
cv2.destroyAllWindows()