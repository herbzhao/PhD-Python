# import the necessary packages
import numpy as np
import cv2
from scale_bar_utility import scale_bar_finder_class 
from preprocessing import preprocessor_class
from contour_detect import contour_detector_class

# import matplotlib.pyplot as plt

folder_name = r"D:\Dropbox\000 - Inverse opal balls\Correlation analysis"
image_name = 'X1- plasma 4min -143'
image_path = r'{}\images\{}.jpg'.format(folder_name, image_name)
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
preprocessor.convert_to_grayscale()
# Warning: three parameters to change

# NOTE: for the smaller holes e.g. C5_plasma 5min_109.jpg
# preprocessor.adjust_contrast_and_brightness(alpha=4, beta=-550)
# preprocessor.convert_to_binary(method='normal', thresh=100, block_size=5, C_value=2)
# preprocessor.morphologrical_transformation(kernel_size=3, steps=['erosion', 'dilation', 'erosion', 'closing', 'opening', 'dilation', ])

# NOTE: for the smaller holes e.g. C2-2min -134.jpg
# preprocessor.adjust_contrast_and_brightness(alpha=2.5, beta=-300)
# preprocessor.convert_to_binary(method='normal', thresh=100, block_size=5, C_value=2)
# preprocessor.morphologrical_transformation(kernel_size=3, steps=['erosion', 'erosion', 'dilation', 'dilation', 'erosion'])

# NOTE: for the smaller holes e.g. X4-2min -157.jpg
# preprocessor.adjust_contrast_and_brightness(alpha=2, beta=-250)
# preprocessor.convert_to_binary(method='normal', thresh=100, block_size=5, C_value=2)
# preprocessor.morphologrical_transformation(kernel_size=2, steps=['erosion', 'erosion', 'dilation', 'dilation', 'erosion'])

# NOTE: for the bigger holes  e.g. X3- plasma 4min -104.jpg
# preprocessor.adjust_contrast_and_brightness(alpha=10, beta=-1000)
# preprocessor.convert_to_binary(method='normal', thresh=100, block_size=5, C_value=2)
# preprocessor.morphologrical_transformation(kernel_size=3, steps=['erosion', 'dilation', 'erosion', 'closing', 'opening', 'dilation', ])

# NOTE: for the bigger holes  e.g. X1- plasma 4min -142.jpg
preprocessor.adjust_contrast_and_brightness(alpha=4, beta=-150)
preprocessor.adjust_contrast_and_brightness(alpha=0.8, beta=0)
preprocessor.convert_to_binary(method='normal', thresh=100, block_size=5, C_value=2)
preprocessor.morphologrical_transformation(kernel_size=3, steps=['erosion', 'erosion',  'erosion',  'dilation', 'closing',  'opening'])

# NOTE: for the bigger holes  e.g. C3 - top view -03.jpg
# preprocessor.adjust_contrast_and_brightness(alpha=4, beta=-400)
# preprocessor.convert_to_binary(method='normal', thresh=100, block_size=5, C_value=2)
# preprocessor.morphologrical_transformation(kernel_size=3, steps=['erosion', 'dilation', 'erosion', 'closing', 'opening', 'dilation', ])


image = preprocessor.image
#  create a copy of the original image for displaying the holes
image_output = image.copy()
image_bw = preprocessor.image_bw

#  NOTE: contour detection and drawing circles
contour_detector = contour_detector_class(image_bw, image_output)
contour_detector.find_contours()
# Warning: one parameter to change
# contour_areas = contour_detector.filter_contours(method='distribution', excluding_portion=0.05, upper_k=5, lower_k=0.1)
contour_areas = contour_detector.filter_contours(method='absolute_area', excluding_portion=0.05, upper_k=3, lower_k=0.3)

centers_pixel, radii_pixel = contour_detector.find_bounding_circles(show=False)
image_output = contour_detector.image_output

# Convert pixel into real unit
centers_um =[[center_pixel[0]*scale_bar, center_pixel[1]*scale_bar] for center_pixel in centers_pixel]
radii_um = [radii_pixel*scale_bar for radii_pixel in radii_pixel]

area_fraction = sum(contour_areas)/total_area
print('area fraction is: {}'.format(area_fraction))


# Note: imagine the circles to be a projection of spheres at different height - considering the maximum radius found is the size of the original sphere
# NOTE: we can then calculate which height did we cross-section the sphere if they are not full size circle
spheres = []
# estimate the Z value
max_radius = max(radii_um)
for i, radius in enumerate(radii_um): 
    Z_offset = (max_radius**2 - radius**2)**(1/2)
    spheres.append((centers_um[i][0], centers_um[i][1], Z_offset, radius))

#  write the coordinates in a csv file
# print(spheres)
with open(r'{}\data\{}.txt'.format(folder_name, image_name), 'w+') as file:
#     file.write('x, y, z, r, \n')
    for sphere in spheres:
        # file.write('{0}, {1}, {2}, {3} \n'.format(sphere[0], sphere[1], sphere[2], sphere[3]))
        file.write('{0} {1} {2}\n'.format(sphere[0], sphere[1], sphere[3]))

# show the output image 
image_output = np.hstack((image, image_output))

cv2.imshow("Overlay image", image_output)
cv2.imwrite( r"{}\data\{}.jpg".format(folder_name, image_name), image_output);
cv2.waitKey(0)
