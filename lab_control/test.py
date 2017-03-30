
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


elements = {}

for i,j in [
    ('mouse_option',"Remember mouse location (F1)"),
    ('img_option',"Remember image (F2)"),
    ('keyboard_option', "Keyboard input/hotkey (F3)"),
    ('timing_option',"Timing (F4)")]:
    elements[i] = j

print(elements['mouse_option'])