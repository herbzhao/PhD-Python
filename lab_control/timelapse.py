'''This code allows automatically taking photos using ueye cockpit'''

from kivy.base import runTouchApp
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp, sp
from kivy.uix.textinput import TextInput
from kivy.config import Config
import pyautogui
import time

def validate_filepath(filepath):
    pass

def system_setup():
    print(Config.get('kivy', 'keyboard_mode'))
    if Config.get('kivy', 'keyboard_mode') != 'system':
        Config.set('kivy', 'keyboard_mode', 'system')
        Config.write()



if __name__ == '__main__':
    system_setup()

    '''The automation by pyautogui'''
    screenWidth, screenHeight = pyautogui.size()
    # initialise the mouse position
    #pyautogui.moveTo(screenWidth/2, screenHeight/2, 0.5)
    
    #pyautogui.pixelMatchesColor(pyautogui.position()[0], pyautogui.position()[1], (130, 135, 144))
    crop_size = 30
    crop_region = (pyautogui.position()[0]-crop_size/2, pyautogui.position()[1]-crop_size/2,
                   crop_size, crop_size)
    screenshot = pyautogui.screenshot(region = crop_region)
    #screenshot.getpixel(pyautogui.position())
    screenshot.save('screen_crop.png')
    print(pyautogui.locateOnScreen('screen_crop.png'))

    
    '''A brief GUI to set time interval for timelapse and file location'''
    notification_board = Popup(title = 'notification', title_size = sp(15))
    notification_content = BoxLayout(orientation = 'vertical')
    notification_board.content = notification_content
    notification_upper_part = BoxLayout(size_hint_y = 0.6)
    notification_lower_part = BoxLayout(size_hint_y = 0.4)
    notification_content.add_widget(notification_upper_part)
    notification_content.add_widget(notification_lower_part)

    # default value for filepath
    # obtain the folder from file chooser
    folder = r'C:\Users\herbz\OneDrive - University Of Cambridge\Documents'
    filename = '20x-TL-CP'
    image_number = 1
    filepath = r'{}\{}-{:03}.jpg'.format(folder, filename, image_number)

    folder_input = TextInput(text = folder)
    filename_input = TextInput(text = filename+'-{:03}.jpg'.format(image_number))

    notification_upper_part.add_widget(folder_input)
    notification_upper_part.add_widget(filename_input)
    notification_lower_part.add_widget(Button(text = 'yes'))



    Window.add_widget(notification_board)
    notification_board.open()
    Window.size = (sp(500), sp(200))


    '''Automatically pick up the file name and add image number based on user input'''
    image_number = filename_input.text[-7:-4]
    filename = filename_input.text[:-8]
    print(filename)
    print(image_number)
    '''while True:
        time.sleep(0.5)
    '''
    
    runTouchApp()