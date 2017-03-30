'''Element capture

Prompt users to choose what is the event: mouse click, image memorise or keyboard action

whenever the action is recorded, a paragraph of python code is also written. (potentially calling functions from a library)

Record 4 actions:
1st mouse 
2nd image recognition
3rd keyboard_input
4th timing: wait time, repeat, etc.

It should write commands in another python file 
which calls another python library to achieve those functions

'''

import sys
import time
from datetime import datetime

import pyautogui

if sys.version_info < (3, 0):
    import Tkinter as tkinter
    # from tkinter import tkMessageBox  as messagebox
else:
    import tkinter
    from tkinter import messagebox

def system_setup():
    global screenWidth, screenHeight, image_number
    image_number = 1
    pyautogui.FAILSAFE = True
    screenWidth, screenHeight = pyautogui.size()

def hide_message_box():
    for i in ('<Escape>','<Return>', '<F1>', '<F2>'):
        message_box.unbind_all(i)# http://www.python-course.eu/tkinter_events_binds.php
    message_box.destroy() # hide the message_box for screenshot

def show_message_box():
    create_message_box() # reappear message_box after screenshot

def create_message_box():
    global message_box
    # create a window tkinter.Tk() to host all components
    message_box = tkinter.Tk()
    task = tkinter.IntVar() # the result of radiobutton
    
    buttons = {}

    for i,j,k in [
        ('mouse_option',"Remember mouse location (F1)", record_mouse),
        ('image_option',"Remember image (F2)", record_image),
        ('keyboard_option', "Keyboard input/hotkey (F3)", record_keyboard),
        ('timing_option',"Timing (F4)", record_mouse),
        ('cancel_button', "Cancel (ESC)", stop_record)]:
        buttons[i] = tkinter.Button(message_box, text = j, command = k).pack(fill = tkinter.X)
    # hotkeys 
    for i, j in (('<Escape>', stop_record), ('<F1>',record_mouse), ('<F2>', record_image)):
        message_box.bind(i, j) # http://www.python-course.eu/tkinter_events_binds.php
    
    screen_width = message_box.winfo_screenwidth() # width of the screen
    screen_height = message_box.winfo_screenheight() # height of the screen
    message_box_width = 300
    message_box_height = 300
    message_box_x = int((screen_width - message_box_width)/2)
    message_box_y = int((screen_height - message_box_height)/2)
    message_box.geometry('{}x{}+{}+{}'.format(message_box_width, message_box_height, message_box_x, message_box_y))
    message_box.focus_force()
    message_box.mainloop()
    
def stop_record(*argv):
    raise SystemExit

def record_mouse(*argv):
    hide_message_box()
    if pyautogui.confirm(
        '''Move mouse to memoriable location.\n
        Press enter to memorise the location''') == 'Cancel':
        show_message_box() # if user click "Cancel", show the message_box
        return
    recorded_mouse_position = pyautogui.position()
    mouse_message_box = tkinter.Tk()
    mouse_message_box.focus_force()
   

    task = tkinter.IntVar() # the result of radiobutton
    def record_left_click(*argv):
        print('left click')
    def record_right_click(*argv):
        print('right click')
    def record_scroll(*argv):
        scroll_amount = scroll_amount_input.get()
        print('scroll {}'.format(scroll_amount))

    #mouse_message_box.unbind_all(i)# http://www.python-course.eu/tkinter_events_binds.php
    #mouse_message_box.destroy()
    #show_message_box()

    right_click_option = tkinter.Radiobutton(
        mouse_message_box, text = "right click", indicatoron = 0,
        variable = task, value = 2, command = record_right_click)
    left_click_option = tkinter.Radiobutton(
        mouse_message_box, text = "left click", indicatoron = 0,
        variable = task, value = 1, command = record_left_click)
    scroll_option = tkinter.Radiobutton(
        mouse_message_box, text = "scroll (+ for up, - for down)", indicatoron = 0,
        variable = task, value = 3, command = record_scroll)
    scroll_amount_input = tkinter.Entry(mouse_message_box)
    cancel_button = tkinter.Button(mouse_message_box, text = 'Cancel', command = stop_record)
    # add all the elements go GUI
    for i in [right_click_option, left_click_option, scroll_option, scroll_amount_input, cancel_button]:
        i.pack(side = tkinter.LEFT)

    # hotkeys 
    for i, j in [
        ('<Escape>', stop_record),
        ('<F1>', record_right_click), ('<F2>', record_left_click), 
        ('<F3>', record_scroll)]:
        mouse_message_box.bind(i, j)


    return recorded_mouse_position

def record_image(*argv):
    '''Record any image from screen to later come back'''
    message_box.withdraw() # hide the message_box for screensho
    global image_number
    global screenWidth, screenHeight
    default_sensitivity = 30
    screen_unit = min(screenWidth, screenHeight)/1000
    sensitivity = pyautogui.prompt(
        text='(0-10) higher value, more sensitive',
        title='sensitivity' ,
        default=default_sensitivity)
    if sensitivity == None:
        message_box.deiconify() # if user click "Cancel", show the message_box
        return 
    try:
        if int(sensitivity) >= 0 and int(sensitivity) <= 100:
            sensitivity = int(sensitivity)         
        else:
            sensitivity = default_sensitivity
    except:
        sensitivity = default_sensitivity
        
    
    crop_size = sensitivity * screen_unit # Higher value, higher sensitivity
    pyautogui.moveTo(pyautogui.size()[0], 0) # move mouse out of window - avoid animation when mouse stay on buttons

    screenshot_full = pyautogui.screenshot('screenshot_full.png')
    
    if pyautogui.confirm(
        '''Move mouse to memoriable location.\n
        Press enter to memorise the screen crop of this area''') == 'Cancel':
        message_box.deiconify() # if user click "Cancel", show the message_box
        return 
    mouse_position = pyautogui.position()
    crop_region = (
        int(mouse_position[0]-crop_size/2),
        int(mouse_position[1]-crop_size/2),
        int(mouse_position[0]+crop_size/2),
        int(mouse_position[1]+crop_size/2))
    screenshot_crop = screenshot_full.crop(crop_region)
    screenshot_crop.save('screenshot_crop_{:02}.png'.format(image_number))
    image_number += 1
    message_box.deiconify() # show the message_box again
    return screenshot_crop


def record_filepath():
    folder = pyautogui.prompt(title='Paste the filepath here.', default=r'C:\Users\Public\Documents\tz275\20170104\Hydrophobic\test')
    if folder is None:
        raise SystemExit
    filename = pyautogui.prompt(title='type filename here', default=r'20x-TL-CP-001.jpg')
    if folder is None:
        raise SystemExit
    image_number = int(filename[-7:-4])
    return folder, filename, image_number

def save_to_file(folder, filename, image_number):
    if os.path.exists(folder):
        pass
    else:
        os.makedirs(folder)
    filename = filename[:-8]
    filepath = folder + '\\' + filename + '-{:03}'.format(image_number)
    secs_between_keys = 0.05
    pyautogui.hotkey('ctrl','a')
    pyautogui.hotkey('delete')
    pyautogui.typewrite(filepath+'\n', interval = secs_between_keys)
    print(filepath)





if __name__ == '__main__':
    system_setup()
    create_message_box()
