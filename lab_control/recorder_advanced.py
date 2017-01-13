import sys
if sys.version_info > (3,0):
    import tkinter
else:
    import Tkinter as tkinter # for python 2.x, tkinter is spelled as Tkinter 

# https://www.tutorialspoint.com/python/python_gui_programming.htm

top = tkinter.Tk()
# Code to add widgets will go here...
top.mainloop()

