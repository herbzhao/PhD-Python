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
    record_options_frame.pack_forget() # hide the message_box for screenshot
def show_message_box():
    record_options_frame.pack() # reappear message_box after screenshot
    # hotkeys 
    message_box.bind('<Return>', start_record) 
    # http://www.python-course.eu/tkinter_events_binds.php
    message_box.bind('<Escape>', stop_record) 
    message_box.bind('<F1>', record_mouse)
    message_box.bind('<F2>', record_image)
    message_box.bind('<F3>', record_mouse)
    message_box.bind('<F4>', record_mouse)

def create_message_box():
    global message_box
    global record_options_frame
    global start_record
    # create a window tkinter.Tk() to host all components
    message_box = tkinter.Tk()
    record_options_frame = tkinter.Frame(message_box)
    record_options_frame.pack()

    task = tkinter.IntVar() # the result of radiobutton
    mouse_option = tkinter.Radiobutton(
        record_options_frame, text = "Remember mouse location (F1)", 
        variable = task, value = 1)
    img_option = tkinter.Radiobutton(
        record_options_frame, text = "Remember image (F2)", 
        variable = task, value = 2)
    keyboard_option = tkinter.Radiobutton(
        record_options_frame, text = "Keyboard input/hotkey (F3)", 
        variable = task, value = 3)
    timing_option = tkinter.Radiobutton(
        record_options_frame, text = "Timing (F4)", 
        variable = task, value = 4)
    
    def start_record(*argv):
        if task.get() == 1:
            record_mouse()
        if task.get() == 2:
            record_image()
        if task.get() == 3:
            record_keyboard()
        if task.get() == 4:
            set_timing()

    ok_button = tkinter.Button(record_options_frame, text = 'OK', command = start_record) 
    cancel_button = tkinter.Button(record_options_frame, text = 'Cancel', command = stop_record)
    # add all the elements go GUI
    for i in [mouse_option, img_option, keyboard_option, timing_option]:
        i.pack(anchor = tkinter.W)
    for i in [ok_button, cancel_button]:
        i.pack(side = tkinter.LEFT)

    # hotkeys 
    message_box.bind('<Return>', start_record) # http://www.python-course.eu/tkinter_events_binds.php
    message_box.bind('<Escape>', stop_record) 
    message_box.bind('<F1>', record_mouse)
    message_box.bind('<F2>', record_image)
    message_box.bind('<F3>', record_mouse)
    message_box.bind('<F4>', record_mouse)
    
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
    mouse_option_frame = tkinter.Frame(message_box)
    mouse_option_frame.pack()
    task = tkinter.IntVar() # the result of radiobutton
    left_click_option = tkinter.Radiobutton(
        mouse_option_frame, text = "left click", 
        variable = task, value = 1)
    right_click_option = tkinter.Radiobutton(
        mouse_option_frame, text = "right click", 
        variable = task, value = 2)
    scroll_option = tkinter.Radiobutton(
        mouse_option_frame, text = "scroll (+ for up, - for down)", 
        variable = task, value = 3)
    scroll_amount_input = tkinter.Entry(mouse_option_frame)
    scroll_amount = scroll_amount_input.get()
    
    def record_mouse_action(*argv):
        mouse_option_frame.pack_forget()
        choice = task.get()
        if choice == 1:
            print('left click')
        if choice == 2:
            print('right click')
        if choice == 3:
            print('scroll {}'.format(scroll_amount))
        show_message_box()
    
    ok_button = tkinter.Button(mouse_option_frame, text = 'OK', command = record_mouse_action) 
    cancel_button = tkinter.Button(mouse_option_frame, text = 'Cancel', command = stop_record)

    for i in [left_click_option, right_click_option, scroll_option, scroll_amount_input]:
        i.pack(side = tkinter.LEFT)
    for i in [ok_button, cancel_button]:
        i.pack()

    # hotkeys 
    message_box.bind('<Return>', record_mouse_action) # http://www.python-course.eu/tkinter_events_binds.php
    message_box.bind('<Escape>', stop_record) 
    message_box.bind('<F1>', record_mouse_action(1))
    message_box.bind('<F2>', record_mouse_action(2))
    message_box.bind('<F3>', record_mouse_action(3))

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
