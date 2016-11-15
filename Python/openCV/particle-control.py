import numpy as np
import cv2

#video capture
cap = cv2.VideoCapture('droplet.avi')  # this is the number of camera
#recrod video
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('result.avi',fourcc,25.0,(640,480))


# this is for background subtraction
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)) # this is the windows size ? 

fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()
#fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()

while(1):
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    img2, cnts, _ = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in cnts:
    	area = cv2.contourArea(c)
    	if area < 100 or area > 1000:
    		continue
    	(x,y,w,h) = cv2.boundingRect(c)
    	cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
    	#print (area)
     

    out.write(frame)  # record video
    
    cv2.imshow('Image', frame)
    #cv2.imshow('Threshold',fgmask)
    
    k = cv2.waitKey(25) & 0xff
    if k == 27: #esc
        break
    
    
cap.release()
cv2.destroyAllWindows()