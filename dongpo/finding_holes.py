# import the necessary packages
import numpy as np
import cv2
import matplotlib.pyplot as plt

image_path = r'C:\Users\My Pc\Documents\GitHub\PhD-Python\dongpo\C3 - top view -03.jpg'
# load the image, clone it for output, and then convert it to grayscale
image = cv2.imread(image_path)
# crop out the scale bar etc
image = image[0:750, 0:1024]
total_area = 750*1024
# number of pixels per micron
scale_bar = 121

output = image.copy()
print(np.size(image))

# do some image processing to make the circle detection easier
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#  invert the black and white
image_gray = cv2.bitwise_not(image_gray)

# Convert grayscale image to binary
(thresh, image_bw) = cv2.threshold(image_gray, 100, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
#  dialation, erosion etc
#  https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html
#  depending upon the size of kernel
kernel = np.ones((2,2),np.uint8)


# closing to filling tiny holes
image_bw = cv2.morphologyEx(image_bw, cv2.MORPH_CLOSE, kernel)
# eroding to splitting up the connected holes
image_bw = cv2.erode(image_bw,kernel,iterations = 2)
# opening to remove noise
image_bw = cv2.morphologyEx(image_bw, cv2.MORPH_OPEN, kernel)


# #  diplay the pre-processed image
# cv2.imshow("output", image_bw)
# cv2.waitKey(0)

# detect countours
image_temp, contours, hierarchy = cv2.findContours(image_bw, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

# use this to filter out the area that is too big
areas = [cv2.contourArea(contour) for contour in contours]
average_area = np.average(areas)

number_of_circle = 0
radii = []
centers = []


for contour in contours:
    area = cv2.contourArea(contour)
    #  use the average area to filter out too small or too big contour
    if area < average_area*2:
        #  Find and draw Minimum Enclosing Circle
        #  https://docs.opencv.org/3.1.0/dd/d49/tutorial_py_contour_features.html
        (x,y),radius = cv2.minEnclosingCircle(contour)
        center = (int(x),int(y))
        radius = int(radius)
        cv2.circle(output,center,radius,(0,255,0),1)
        #  annotation
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(output,str(number_of_circle),center, font, 0.5,(255,255,255),2,cv2.LINE_AA)

        # 
        number_of_circle += 1
        centers.append([center[0]/scale_bar, center[1]/scale_bar])
        radii.append(radius/scale_bar)

area_fraction = sum(areas)/total_area
print('area fraction is: {}'.format(area_fraction) )


# Note: imagine the circles to be a projection of spheres at different height - considering the maximum radius found is the size of the original sphere
# NOTE: we can then calculate which height did we cross-section the sphere if they are not full size circle
spheres = []
# estimate the Z value
max_radius = max(radii)
for i, radius in enumerate(radii): 
    Z_offset = (max_radius**2 - radius**2)**(1/2)
    spheres.append((centers[i][0], centers[i][1], Z_offset, radius))

#  write the coordinates in a csv file
# print(spheres)
with open(r'C:\Users\My Pc\Documents\GitHub\PhD-Python\dongpo\{}.txt'.format(max_radius), 'w+') as file:
#     file.write('x, y, z, r, \n')
    for sphere in spheres:
        # file.write('{0}, {1}, {2}, {3} \n'.format(sphere[0], sphere[1], sphere[2], sphere[3]))
        file.write('{0} {1}\n'.format(sphere[0], sphere[1]))




# # detect circles in the image
# circles = cv2.HoughCircles(image_bw, cv2.HOUGH_GRADIENT, 0.5, 1)

# # ensure at least some circles were found
# if circles is not None:
#     for circle in circles[0]:
#         # loop over the (x, y) coordinates and radius of the circles
#         x, y, r = [int(i) for i in circle]
#         # draw the circle in the output image, then draw a rectangle
#         # corresponding to the center of the circle
#         # cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]])
#         cv2.circle(output, (x, y), r, (0, 255, 0), 4)
#         #  draw the centre of the circle
#         cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)


# show the output image 
cv2.imshow("image 1", image_bw)
cv2.imshow("image 2", output)
cv2.waitKey(0)