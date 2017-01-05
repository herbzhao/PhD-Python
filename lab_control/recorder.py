'''Element capture'''
import pyautogui  # http://pyautogui.readthedocs.io/en/latest/cheatsheet.html
import time
from datetime import datetime


def system_setup():
    pyautogui.FAILSAFE = True

def record_image():
    '''Record any image from screen to later come back'''
    global image_number
    crop_size = 15 # Higher value, higher sensitivity
    pyautogui.moveTo(pyautogui.size()[0], 0) # move mouse out of window
    # Take a screenshot without mouse on any button
    screenshot_full= pyautogui.screenshot('screenshot_full.png')
    if pyautogui.confirm(
        '''Move mouse to memoriable location.\n
        Press enter to memorise the screen crop of this area''') == 'Cancel':
        raise SystemExit # if user click "Cancel", stop whole program
    mouse_position = pyautogui.position()
    crop_region = (
        int(mouse_position[0]-crop_size/2),
        int(mouse_position[1]-crop_size/2),
        int(mouse_position[0]+crop_size/2),
        int(mouse_position[1]+crop_size/2))
    screenshot_crop = screenshot_full.crop(crop_region)
    screenshot_crop.save('screenshot_crop_{:02}.png'.format(image_number))
    return screenshot_crop

def record_mouse_position():
    if pyautogui.confirm(
        '''Move mouse to memoriable location.\n
        Press enter to memorise the location''') == 'Cancel':
        raise SystemExit
    recorded_mouse_position = pyautogui.position()
    return recorded_mouse_position


def recorder():
    global image_number
    while True:
        recorded_item = pyautogui.confirm(text = 'Record item is a ?', buttons=['image', 'location', 'Cancel'])
        if recorded_item == 'image':
            recorded_item = record_image()
            image_number +=1
        elif recorded_item == 'location':
            recorded_item = record_mouse_position()
            f = open('recorded_locations.txt', 'a+')
            f.write('{:%Y-%m-%d %H:%M} \n'.format(datetime.now()))
            f.write(str(recorded_item)+'\n')
            f.close()
        else:
            raise SystemExit


if __name__ == '__main__':
    system_setup()
    image_number = 1
    recorder()
    

    



