# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 22:34:33 2016

@author: herbz
"""

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
from kivy.core.window import Window

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
       
        # few more parameters for scaling
        normal_scale = 5
        zoom_in_scale = 6
        zoom_out_scale = 4
        x_sensitive= Window.center[0]/3
        y_sensitive = Window.center[1]/3
        


        # Scatter that can be zoom and translate
        controller = Scatter(size_hint = (None,None), do_rotation=False, do_scale=True, do_translation=True,  scale = normal_scale, scale_min= zoom_out_scale, scale_max=zoom_in_scale, auto_bring_to_front = True, center = Window.center)

        
        # a reference object to show the zoom and move
        #control_object = Image(source='random.png')
        control_object = Label(text = '')
        controller.add_widget(control_object)
        
        
        # this provides actions when moving and zooming the scatter objects
        def control_feedback(arg1, arg2):
            if controller.center[0] - Window.center[0] >x_sensitive:
                indicator.text = 'move right'
                map_scatter.center = (map_scatter.center[0]+move_step,map_scatter.center[1])

            elif controller.center[0] - Window.center[0] < -1* x_sensitive:
                indicator.text ='move left'
                map_scatter.center = (map_scatter.center[0]-move_step,map_scatter.center[1])
               
            elif controller.center[1] - Window.center[1] > y_sensitive:
                indicator.text ='move top'
                map_scatter.center = (map_scatter.center[0],map_scatter.center[1]+move_step)

            elif controller.center[1] - Window.center[1] < -1*y_sensitive:
                indicator.text = 'move down'
                map_scatter.center = (map_scatter.center[0],map_scatter.center[1]-move_step)      
               
            #after taking actions, reset scatter location
            controller.center = Window.center
            
            
            if controller.scale < zoom_out_scale*1.1:
                indicator.text = 'zoom out'
                map_scatter.scale = map_scatter.scale - zoom_step
            
                
                
            elif controller.scale > zoom_in_scale*0.9:
                indicator.text = 'zoom in'
                map_scatter.scale = map_scatter.scale + zoom_step
                
               
                
            #after taking actions, reset scatter zoom
            controller.scale = normal_scale
                
        # bind the touch with function
        controller.bind(on_touch_up = control_feedback)
        
        # a label to show the state of movement
        indicator = Label(text='indicator', size_hint = (None,None))
        indicator_bot = anchoring('left', 'bottom', indicator)

        # a mock up map_object
        map_scatter = Scatter(scale = 5,  center = Window.center, do_rotation=False, do_scale=False, do_translation=False,  size_hint = (None,None))
        map_object = Image(source='map_obj.jpg')
        map_scatter.add_widget(map_object)
        
        #few more data for mock image
        zoom_step = 2
        move_step = 200
        
        
        # add widget to the GUI
        self.add_widget(controller)
        self.add_widget(map_scatter)
        self.add_widget(indicator_bot)
        
        
        
                
        # this shows the actual zoom_control size in real time (Async)

            

class kiwi_app(App):
#only ever need to change the name of Myapp
    def build(self):
    #function initialize and return your Root Widget. 
        container = Container()
        return container



if __name__ == '__main__':
    kiwi_app().run()

    