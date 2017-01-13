
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



message_box = tkinter.Tk()
frame = tkinter.Frame(message_box)
frame.pack()


task = tkinter.IntVar() # the result of radiobutton
left_click_option = tkinter.Radiobutton(
    frame, text = "left click", 
    variable = task, value = 1)
right_click_option = tkinter.Radiobutton(
    frame, text = "right click", 
    variable = task, value = 2)
scroll_option = tkinter.Radiobutton(
    frame, text = "scroll (+ for up, - for down)", 
    variable = task, value = 3)

for i in [left_click_option,right_click_option,scroll_option]:
    i.pack()


frame.pack_forget()
message_box.mainloop()