# import the necessary packages
import numpy as np
import cv2
from scale_bar_utility import scale_bar_finder_class 
from preprocessing import preprocessor_class
from contour_detect import contour_detector_class
import os
import pandas as pd


# import matplotlib.pyplot as plt

folder_name = r"D:\Dropbox\000 - Inverse opal balls\Correlation analysis\images\20200317 - IOB 1to50 repeat\jpg"
image_name = 'Red (8k 15s 70C)-89'
image_path = r'{}\{}.jpg'.format(folder_name, image_name)
print(image_path)
# load the image
image = cv2.imread(image_path)

# NOTE: find scale bar -- making it a bit slow?
scale_bar_finder = scale_bar_finder_class(image)
# number of pixels per micron/nanometer --
scale_bar = scale_bar_finder.draw_scale_bar()

#  NOTE: preprocessing, convert to binary image for feature extraction
preprocessor = preprocessor_class(image)
total_area = preprocessor.cropping()

preprocessor.convert_to_grayscale(show=False)
# Warning: three parameters to change


# NOTE: for the bigger holes top vieww  e.g. C2 - blue balls -no plasma -140
# preprocessor.adjust_contrast_and_brightness(alpha=4, beta=-500)
# preprocessor.convert_to_binary(method='adaptive', thresh=100, block_size=51, C_value=2)
# preprocessor.morphologrical_transformation(kernel_size=3, steps=['erosion', 'dilation', 'erosion', 'closing', 'opening', 'dilation', ])

# NOTE: for the blue ball in paper
# preprocessor.adjust_contrast_and_brightness(alpha=1, beta=-100)
# preprocessor.convert_to_binary(method='adaptive', thresh=100, block_size=51, C_value=3)
# preprocessor.morphologrical_transformation(kernel_size=3, steps=['erosion', 'dilation', 'erosion', 'closing', 'opening', 'dilation', ])

# CHANGE: for the blue ball in paper
# preprocessor.adjust_contrast_and_brightness(alpha=1, beta=-80)
# preprocessor.convert_to_binary(method='adaptive', thresh=100, block_size=51, C_value=3)
# preprocessor.morphologrical_transformation(kernel_size=3, steps=['erosion', 'dilation', 'erosion', 'closing', 'opening', 'dilation', ])

# CHANGE: for the green ball in paper
preprocessor.adjust_contrast_and_brightness(alpha=1, beta=-70)
preprocessor.convert_to_binary(method='adaptive', thresh=100, block_size=121, C_value=3)
preprocessor.morphologrical_transformation(kernel_size=3, steps=['erosion', 'dilation', 'erosion', 'closing', 'opening', 'dilation', ])


# CHANGE: for the red ball in paper
# preprocessor.adjust_contrast_and_brightness(alpha=1, beta=-120)
# preprocessor.convert_to_binary(method='adaptive', thresh=100, block_size=121, C_value=3)
# preprocessor.morphologrical_transformation(kernel_size=3, steps=['erosion', 'dilation', 'erosion', 'closing', 'opening', 'dilation', ])




image = preprocessor.image
#  create a copy of the original image for displaying the holes
image_output = image.copy()
image_bw = preprocessor.image_bw

# contour detection and drawing circles
contour_detector = contour_detector_class(image_bw, image_output)
contour_detector.find_contours()

# Warning: one parameter to change
# contour_areas = contour_detector.filter_contours(method='distribution', excluding_portion=0.05, upper_k=5, lower_k=0.1)
# contour_areas = contour_detector.filter_contours(method='absolute_area', excluding_portion=0.1, upper_k=3, lower_k=0.5)
centers_pixel, radii_pixel = contour_detector.find_bounding_circles(show=False)

# convert center and radius to a dict and then to dataframe
circles = list(zip(centers_pixel, radii_pixel))
circles = [{'x': circle[0][0], 'y': circle[0][1], 'r': circle[1]} for circle in circles]
circles = pd.DataFrame(circles)

# circles = circles[800:]

# CHANGE: dropout of the outliers !
# filter out the circles too large, too small or touching
circles = contour_detector.circle_dropout(circles, method='boundary', lower_quantile=0.1, upper_quantile=0.9, upper_k=10, lower_k=0.2)
# circles = contour_detector.circle_dropout(circles, method='quantile', lower_quantile=0.1, upper_quantile=1, upper_k=1, lower_k=0.3)
circles = contour_detector.collision_detection(circles)
circles = contour_detector.circle_dropout(circles, method='boundary', lower_quantile=0.1, upper_quantile=0.9, lower_k=0.1, upper_k=10)




# plot out the circles after dropout
for _, circle in circles.iterrows():
    contour_detector.draw_circles(circle)


circles = circles.sort_values(by=['r'], ascending=False)
circles = circles.reset_index(drop=True)


# calculate the area of circles
total_circle_area = np.sum([circles['r'] ** 2 * 3.14])
area_fraction = total_circle_area / total_area
print('area fraction is: {}'.format(area_fraction))


image_output = contour_detector.image_output
# Convert pixel into real unit
# circles_um = [{'x': circle['x']*scale_bar, 'y': circle['y']*scale_bar, 'r': circle['r']*scale_bar} for circle in circles]
circles = circles.apply(lambda x: x*scale_bar)




# Note: imagine the circles to be a projection of spheres at different height - considering the maximum radius found is the size of the original sphere
# NOTE: we can then calculate which height did we cross-section the sphere if they are not full size circle
spheres = []
# estimate the Z value
max_radius = max(circles['r'])
circles['z'] = circles['r'].map(lambda r: (max_radius**2 - r**2)**(1/2))

result_folder = folder_name + '\\result'
if not os.path.exists(result_folder):
        os.mkdir(result_folder)
#  write the coordinates in a csv file
# print(spheres)
with open(r'{}\{}_circle.txt'.format(result_folder, image_name), 'w+') as file:
#     file.write('x, y, z, r, \n')
    file.write('area fraction: {}\n'.format(area_fraction))
    file.write('largest radius: {}\n'.format(max(circles['r'])))
    file.write('average radius: {}\n'.format(np.average(circles['r'])))


    for _, circle in circles.iterrows():
        # file.write('{0}, {1}, {2}, {3} \n'.format(sphere[0], sphere[1], sphere[2], sphere[3]))
        file.write('{0} {1} {2}\n'.format(circle['x'], circle['y'], circle['r']))

with open(r'{}\{}_sphere.txt'.format(result_folder, image_name), 'w+') as file:
#     file.write('x, y, z, r, \n')
    file.write('area fraction: {}\n'.format(area_fraction))
    file.write('largest radius: {}\n'.format(max(circles['r'])))

    for _, circle in circles.iterrows():
        # file.write('{0}, {1}, {2}, {3} \n'.format(sphere[0], sphere[1], sphere[2], sphere[3]))
        file.write('{0} {1} {2}\n'.format(circle['x'], circle['y'], circle['z'], circle['r']))


# show the output image 
image_output = np.hstack((image, image_output))

cv2.imshow("Overlay image", image_output)

cv2.imwrite( r"{}\{}.jpg".format(result_folder, image_name), image_output);
cv2.waitKey(0)
