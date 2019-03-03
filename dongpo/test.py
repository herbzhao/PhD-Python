# import the necessary packages
import cv2
import easygui

# user mouse click to obtain the scale bar
# https://www.pyimagesearch.com/2015/03/09/capturing-mouse-click-events-with-python-and-opencv/
start_point, end_point = [(),()]
def mouse_select_area(event, x, y, flags, param):
    ''' a method that capture coordinates of the distance on sample '''
    global start_point, end_point
    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        start_point = (x,y)
    if event == cv2.EVENT_LBUTTONUP:
        end_point = (x,y)

image_name = 'X3- plasma 4min -109'
image_path = r'images\{}.jpg'.format(image_name)
# load the image, clone it for output, and then convert it to grayscale
image = cv2.imread(image_path)

clone = image.copy()
cv2.namedWindow("draw_scale_bar")
cv2.setMouseCallback("draw_scale_bar", mouse_select_area)

# keep looping until the 'q' key is pressed
while True:
    # display the image and wait for a keypress
    cv2.imshow("draw_scale_bar", image)
    key = cv2.waitKey(20) & 0xFF

    # draw the rectangle for the user clicked points 
    if end_point != ():
            image = clone.copy()
            cv2.rectangle(image, start_point, end_point, (0, 255, 0), 2)
            scale_bar_pixel = end_point[0] - start_point[0]
            start_point, end_point = [(),()]

    
    # if the 'x' or 'esc' key is pressed, break from the loop
    if key == ord("x") or key == 27:
        break
    
    # if the 'enter'  key is pressed, break from the loop
    if key == 13:
        scale_bar_nm = easygui.enterbox("What's the scale bar in um?", 'Pixel distance: {}'.format(scale_bar_pixel), '1')
        scale_bar_pixel_to_nm = float(scale_bar_pixel)/float(scale_bar_nm)
        print(scale_bar_pixel_to_nm)
        break

