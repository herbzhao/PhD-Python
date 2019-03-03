# import the necessary packages
import numpy as np
import cv2
from scale_bar_utility import scale_bar_finder_class 

# import matplotlib.pyplot as plt


image_name = 'X3- plasma 4min -108'
image_path = r'images\{}.jpg'.format(image_name)
# load the image
image = cv2.imread(image_path)

# NOTE: find scale bar -- making it a bit slow?
scale_bar_finder = scale_bar_finder_class(image)
# number of pixels per micron/nanometer --
scale_bar = scale_bar_finder.draw_scale_bar()

# crop out the scale bar etc
image = image[0:760, 0:1024]
total_area = 760*1024

#  create a copy of the original image for displaying the holes
output = image.copy()


# do some image processing to make the circle detection easier
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#  invert the black and white
image_gray = cv2.bitwise_not(image_gray)

# change brightness and contrast
# https://docs.opencv.org/3.4/d3/dc1/tutorial_basic_linear_transform.html
alpha = 1.5 # Simple contrast control
beta = 0    # Simple brightness control
for y in range(image.shape[0]):
    for x in range(image.shape[1]):
        image_gray[y,x] = np.clip(alpha*image_gray[y,x] + beta, 0, 255)
        # for c in range(image.shape[2]):
        #     image_gray[y,x,c] = np.clip(alpha*image_gray[y,x,c] + beta, 0, 255)


# show the output image 
# cv2.imshow("original image", output)
cv2.imshow("Gray image for thresholding", image_gray)
cv2.waitKey(0)
cv2.destroyAllWindows()


# Convert grayscale image to binary
(thresh, image_bw) = cv2.threshold(image_gray, 100, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

# NOTE: dialation, erosion etc
#  https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html
# NOTE: this is the value that changes based on image basis
#   depending on the scale bar, the kernal size should change accordingly
kernel = np.ones((3,3),np.uint8)

# closing to filling tiny holes
image_bw = cv2.morphologyEx(image_bw, cv2.MORPH_CLOSE, kernel)

# eroding to splitting up the connected holes
image_bw = cv2.erode(image_bw,kernel,iterations = 2)
# opening to remove noise
image_bw = cv2.morphologyEx(image_bw, cv2.MORPH_OPEN, kernel)
#  closing:  It is useful in closing small holes inside the foreground objects, or small black points on the object.
# image_bw = cv2.morphologyEx(image_bw, cv2.MORPH_CLOSE, kernel)
# Dilation
# image_bw = cv2.dilate(image_bw,kernel,iterations = 2)


# #  diplay the pre-processed image
# cv2.imshow("output", image_bw)
# cv2.waitKey(0)

# NOTE: detect countours
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
    if area:
    # if area < average_area*2:
        #  Find and draw Minimum Enclosing Circle
        #  https://docs.opencv.org/3.1.0/dd/d49/tutorial_py_contour_features.html
        (x,y),radius = cv2.minEnclosingCircle(contour)
        center = (int(x),int(y))
        radius = int(radius)
        cv2.circle(output,center,radius,(0,255,0),1)
        #  annotation
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(output,str(number_of_circle),center, font, 0.5,(255,255,255),2,cv2.LINE_AA)

        number_of_circle += 1
        centers.append([center[0]*scale_bar, center[1]*scale_bar])
        radii.append(radius*scale_bar)

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
with open(r'data\{}.txt'.format(image_name), 'w+') as file:
#     file.write('x, y, z, r, \n')
    for sphere in spheres:
        # file.write('{0}, {1}, {2}, {3} \n'.format(sphere[0], sphere[1], sphere[2], sphere[3]))
        file.write('{0} {1} {2}\n'.format(sphere[0], sphere[1], sphere[3]))



# show the output image 
cv2.imshow("Binary threshold", image_bw)
cv2.imshow("Overlay image", output)
cv2.imwrite( "data\{}.jpg".format(image_name), output );
cv2.waitKey(0)