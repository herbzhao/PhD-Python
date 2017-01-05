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
from kivy.uix.popup import Popup

'''import layout'''
#  A layout is a special kind of widget that manages the size and/or position of its child widgets
from kivy.uix.floatlayout import FloatLayout
# Floatlayout can be resized, moved easily
from kivy.uix.anchorlayout import AnchorLayout

# uix module holds the user interface elements like layouts and widgets.

'''import misc'''

def anchoring(x,y, widget):
    '''anchoring(centre, left, btn1)'''
    a_layout = AnchorLayout(anchor_x=x, anchor_y=y, )
    a_layout.add_widget(widget)
    
    return a_layout
        
class Container(FloatLayout):
    def __init__(self, **kwargs):
        super(Container, self).__init__(**kwargs)
       
        
        
        def press_right(instance):
            print('going right')
        def press_left(instance):
            print('going left')
        def press_top(instance):
            print('going top')            
        def press_bot(instance):
            print('going bottom')
            # degree of zoom
        
        btn_right = Button(text='>', font_size= '100 sp', size_hint=(0.1, 0.7))
        #size hint scales with the total window size
        btn_right.bind(on_press=press_right)
        anchor_right = anchoring('right', 'center',btn_right)
        
        btn_left = Button(text='<', font_size= '100 sp', size_hint=(0.1, 0.7))
        btn_left.bind(on_press=press_left)
        anchor_left = anchoring('left','center',btn_left)
        
        btn_top = Button(text='^', font_size= '100 sp', size_hint=(0.7, 0.1))
        btn_top.bind(on_press=press_top)
        anchor_top = anchoring('center','top',btn_top)
        
        btn_bot = Button(text='v', font_size= '100 sp', size_hint=(0.7, 0.1))
        btn_bot.bind(on_press=press_bot)
        anchor_bot = anchoring('center','bottom',btn_bot)
        
        
        zoom_control = Scatter(size_hint = (None,None), do_rotation=False, do_scale=True, do_translation=True,  scale = 2, scale_min= 1, scale_max=3, auto_bring_to_front = True)

        zoom_object = Image(source='random.png')
        #zoom_object = Label(text = 'test', halign = 'center', valign = 'middle')
        zoom_control.add_widget(zoom_object)
        anchor_mid = anchoring('center','center',zoom_control)
                
        # this shows the actual zoom_control size in real time (Async)

        def zoom_feedback(arg1, arg2):
            print(str(zoom_control.top))
            pass
                
        zoom_control.bind(top = zoom_feedback)
        
        
        
        self.add_widget(anchor_right)
        self.add_widget(anchor_left)
        self.add_widget(anchor_top)
        self.add_widget(anchor_bot)   
        self.add_widget(anchor_mid)
        

        
            

class kiwi_app(App):
#only ever need to change the name of Myapp
    def build(self):
    #function initialize and return your Root Widget. 
        container = Container()
        return container



if __name__ == '__main__':
    kiwi_app().run()

    