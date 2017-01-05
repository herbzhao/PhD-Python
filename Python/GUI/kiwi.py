# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 09:15:28 2016

@author: herbz
"""

import kivy
kivy.require('1.9.1') # replace with your current kivy version !
from kivy.app import App
# base Class of your App inherits from the App class

'''import widgets'''
from kivy.uix.label import Label
# texts
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
# This can be moved, resized and rotated by interactions
# including the child widgets

'''import layout'''
#  A layout is a special kind of widget that manages the size and/or position of its child widgets
from kivy.uix.floatlayout import FloatLayout
# Floatlayout can be resized, moved easily
from kivy.uix.gridlayout import GridLayout


# uix module holds the user interface elements like layouts and widgets.

def on_motion(self, touch):
    print(touch.profile)


class kiwi_app(App):
#only ever need to change the name of Myapp
    def build(self):
    #function initialize and return your Root Widget. 

        f_layout = FloatLayout()
        scatter_obj = Scatter()
        hello = Label(text='Hello!',
                  font_size=150)
        wimg = Image(source='random.png')
        f_layout.add_widget(scatter_obj)
        # this add child widget to layout
        scatter_obj.add_widget(wimg)

        on_motion()
        
        return f_layout

        
if __name__ == '__main__':
    kiwi_app().run()

    