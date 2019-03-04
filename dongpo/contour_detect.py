# import the necessary packages
import cv2
import numpy as np
from preprocessing import preprocessor_class


class contour_detector_class():
    ''' find the contours and find circles '''
    def __init__(self, image_bw, image_output):
        self.image_bw = image_bw
        self.image_output = image_output

    def find_contours(self):
        ''' detect countours on bw image'''
        temp_image, self.contours, hierarchy = cv2.findContours(self.image_bw, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    def filter_contours(self, method='distribution', excluding_portion = 0.01, upper_k=5, lower_k=0.1):
        ''' use this to filter out the area that is too big or too small'''
        contour_areas = [cv2.contourArea(contour) for contour in self.contours]
        #  create a numpy array for outlier analysis
        contour_areas_np = np.array(contour_areas)
        average_area = np.average(contour_areas_np)
        contour_areas_np.sort()
        if method == 'distribution':
            ''' removing the percentage of population as the outlier '''
            upper_area_bound = contour_areas_np[int(len(contour_areas_np)*(1-excluding_portion))]
            lower_area_bound = contour_areas_np[int(len(contour_areas_np)*(excluding_portion))]
        elif method == 'absolute_area':
            ''' using distance from average area to define the outlier '''
            upper_area_bound = average_area*upper_k
            lower_area_bound = average_area*lower_k

        contours_to_remove = []
        # remove the contours with area too large or too small
        for i, area in enumerate(contour_areas):
            if area <= lower_area_bound:
                contours_to_remove.append(i)
            if area >= upper_area_bound:
                contours_to_remove.append(i)
        # this is the contours after removal
        self.contours = [contour for i, contour in enumerate(self.contours) if i not in contours_to_remove]
        contour_areas = [cv2.contourArea(contour) for contour in self.contours]
        return contour_areas

    def find_bounding_circles(self, annotation=False, show=True):
        ''' find the minimum enclosing circles around the contour and record the radius etc'''
        number_of_circle = 0
        radii_pixel = []
        centers_pixel = []
        for contour in self.contours:
                #  Find and draw Minimum Enclosing Circle
                #  https://docs.opencv.org/3.1.0/dd/d49/tutorial_py_contour_features.html
                number_of_circle += 1
                (x,y),radius = cv2.minEnclosingCircle(contour)
                center = (int(x),int(y))
                centers_pixel.append([center[0], center[1]])
                radius = int(radius)
                radii_pixel.append(radius)

                # draw circles on output image
                cv2.circle(self.image_output,center,radius,(0,255,0),1)
                if annotation is True:
                    #  annotation
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(self.image_output,str(number_of_circle),center, font, 0.5,(255,255,255),2,cv2.LINE_AA)
            
        if show is True:
            cv2.imshow("Circles", self.image_output)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        return centers_pixel, radii_pixel


if __name__ == "__main__":
    folder_name = r"D:\Dropbox\000 - Inverse opal balls\Correlation analysis" +"\\"
    image_name = 'X4-2min -158'
    image_path = r'{}images\{}.jpg'.format(folder_name, image_name)
    # load the image, clone it for output, and then convert it to grayscale
    image = cv2.imread(image_path)
    scale_bar = 2

    preprocessor = preprocessor_class(image)
    preprocessor.cropping()
    preprocessor.convert_to_grayscale(show=False)
    preprocessor.convert_to_binary(method='normal', thresh=100, block_size=5, C_value=2, show=False)

    image_bw = preprocessor.image_bw
    image_output = image.copy()

    contour_detector = contour_detector_class(image_bw, image_output)
    contour_detector.find_contours()
    contour_areas = contour_detector.filter_contours(method='distribution', excluding_portion=0.1)
    centers_pixel, radii_pixel = contour_detector.find_bounding_circles()
    centers_um =[[center_pixel[0]*scale_bar, center_pixel[1]*scale_bar] for center_pixel in centers_pixel]
    radii_um = [radii_pixel*scale_bar for radii_pixel in radii_pixel]




