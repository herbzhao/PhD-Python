# import the necessary packages
import cv2
import numpy as np

class preprocessor_class():
    ''' do some image processing to make the circle detection easier '''
    def __init__(self, image):
        self.image = image
    
    def cropping(self, x1=0, x2=1024, y1=0, y2=760):
        ''' crop out the scale bar etc '''
        self.image = self.image[y1:y2, x1:x2]
        total_area = abs((x2-x1)*(y2-y1))
        return total_area


    def convert_to_grayscale(self, invert=True, show=True):
        ''' convert image to grayscale for later thresholding''' 
        self.image_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        if invert is True:
            #  invert the black and white
            self.image_gray = cv2.bitwise_not(self.image_gray)
        if show is True:
            cv2.imshow("Inversed gray image", self.image_gray)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def filtering(self, method='bilateral', show=True):
        ''' apply different filters, not yet finalised''' 
        # https://docs.opencv.org/3.0-beta/modules/imgproc/doc/filtering.html
        if method == 'bilateral':
            self.image_bw = cv2.bilateralFilter(self.image_gray,9,75,75)
        elif method == 'median':
            self.image_bw = cv2.medianBlur(self.image_gray,5)
        elif method == 'gaussian':
            self.image_bw = cv2.GaussianBlur(self.image_gray,(5,5),0)
        if show is True:
            cv2.imshow("Filtered image", self.image_gray)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def adjust_contrast_and_brightness(self, alpha=1.8, beta=50, show=True):
        ''' change brightness and contrast '''
        # https://docs.opencv.org/3.4/d3/dc1/tutorial_basic_linear_transform.html
        self.image_gray = self.image_gray*float(alpha) + beta
        # to prevent wrapping by unit8, use np.clip
        # https://stackoverflow.com/questions/7547557/numpy-uint8-pixel-wrapping-solution
        self.image_gray = np.clip(self.image_gray, 0, 255)
        self.image_gray = self.image_gray.astype('uint8')

        if show is True:
            cv2.imshow("Adjusted Contrast and brightness", self.image_gray)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def convert_to_binary(self, method='normal', thresh=100, block_size=5, C_value=2, show=True):
        # https://docs.opencv.org/3.4/d7/d4d/tutorial_py_thresholding.html
        # Convert grayscale image to binary
        # Can try adaptive thresholding and otsu
        if method == 'normal':
            (retVal, self.image_bw) = cv2.threshold(self.image_gray, thresh, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        elif method == 'adaptive':
            # Block Size - 	Size of a pixel neighborhood that is used to calculate a threshold value for the pixel: 3, 5, 7, and so on.
            # C -	Constant subtracted from the mean or weighted mean (see the details below). Normally, it is positive but may be zero or negative as well.
            self.image_bw = cv2.adaptiveThreshold(self.image_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, C_value)
        elif method == 'otsu':
            (retVal, self.image_bw) = cv2.threshold(self.image_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        if show is True:
            cv2.imshow("Binary image", self.image_bw)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


    def morphologrical_transformation(self, kernel_size=1, steps=['closing', 'opening'], show=True):
        ''' operations based on the image shape: Dialation, erosion etc, '''
        #  https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html
        # WARNING: this is the value that changes based on image basis
        #   depending on the scale bar, the kernal size should change accordingly
        kernel = np.ones((kernel_size, kernel_size),np.uint8)

        for step in steps:
            if step == 'erosion':
                # eroding to splitting up the connected holes
                self.image_bw = cv2.erode(self.image_bw, kernel, iterations=1)
            elif step == 'dilation':
                # increases the white region in the image or size of foreground object increases.
                self.image_bw = cv2.dilate(self.image_bw,kernel, iterations=1)
            elif step == 'closing':
                # closing to remove small holes inside the foreground objects: Dilation followed by Erosion.
                self.image_bw = cv2.morphologyEx(self.image_bw, cv2.MORPH_CLOSE, kernel)
            elif step == 'opening':
                # opening to remove noise: another name of Erosion followed by Dilation
                self.image_bw = cv2.morphologyEx(self.image_bw, cv2.MORPH_OPEN, kernel)

        if show is True:
            cv2.imshow("Morphological Transformation", self.image_bw)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

  

if __name__ == "__main__":
    folder_name = r"D:\Dropbox\000 - Inverse opal balls\Correlation analysis" +"\\"
    image_name = 'X4-2min -158'
    image_path = r'{}images\{}.jpg'.format(folder_name, image_name)
    # load the image, clone it for output, and then convert it to grayscale
    image = cv2.imread(image_path)
    preprocessor = preprocessor_class(image)
    preprocessor.cropping()
    preprocessor.convert_to_grayscale()
    # preprocessor.filtering(method='bilateral')
    preprocessor.adjust_contrast_and_brightness(alpha=2, beta=-250)
    # preprocessor.adjust_contrast_and_brightness(alpha=3, beta=-250)
    # preprocessor.adjust_contrast_and_brightness(alpha=1, beta=-50)
    preprocessor.convert_to_binary(method='normal', thresh=100, block_size=5, C_value=2)
    preprocessor.morphologrical_transformation(kernel_size=2, steps=['closing', 'opening', 'erosion', 'erosion', 'dilation'])

    image_bw = preprocessor.image_bw
    image_output = image.copy()

