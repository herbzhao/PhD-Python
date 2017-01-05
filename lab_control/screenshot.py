'screen shot crop function'

# Import Pillow:
import pyautogui


'''Record any image from screen to later come back'''
crop_size = 100 # Higher value, higher sensitivity
pyautogui.moveTo(pyautogui.size()[0], 0) # move mouse out of window
# Take a screenshot without mouse on any button
screenshot_full= pyautogui.screenshot('screenshot_full.png')
if pyautogui.confirm('''Move mouse to memoriable location.\n
                     Press enter to memorise the button image''') == 'Cancel':
    raise SystemExit # if user click "Cancel", stop whole program
mouse_position = pyautogui.position()
crop_region = (
    int(mouse_position[0]-crop_size/2),
    int(mouse_position[1]-crop_size/2),
    int(mouse_position[0]+crop_size/2),
    int(mouse_position[1]+crop_size/2))
screenshot_crop = screenshot_full.crop(crop_region)
screenshot_crop.save('screenshot_crop.png')
