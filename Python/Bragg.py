# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 22:17:29 2016

@author: Herbee
"""

#Import basic module to set up


import matplotlib.pyplot as plt
import numpy as np
import math


fig = plt.figure(figsize=(5,10), dpi=300)
ax = plt.subplot(211)


#Basic parameters
d = 100 #spacing
wavelength = 25
theta = np.pi/6  #incident angle


# crystalliine layers

x_layer = np.linspace(-500,500,500)
y_layer = np.linspace(0, 0, 500)+d
y_layer2 = np.linspace(0, 0, 500)+d
ax.plot(x_layer,y_layer, x_layer,y_layer2)

#mirror line
x_mirror = np.linspace(0,0,500)
y_mirror = np.linspace(0,500,500)
ax.plot(x_mirror,y_mirror,'--')


#line with certain incident angle theta 


x1 = np.linspace(-500, 500, 500)
x_ang = x1/wavelength*2*np.pi
y1 = np.abs(x1) * np.tan(theta) + np.sin(x1)

ax.plot(x1,y1)

#second parallel incident light
y2 = np.abs(x1) * np.tan(theta) + d
ax.plot(x1,y2)

#Calculation of light path difference
light_path = 2*np.sin(theta)*d

phase_shift = light_path/wavelength*np.pi*2

#axis
#ax.set_xlim(-5,5)
#ax.set_ylim(0,10)


#interference result
ax2 = plt.subplot(212)
x_inc = np.linspace(0, 4*np.pi, 500)
y_inc = np.sin(x_inc)
y_phase_shift = np.sin(x_inc+phase_shift)
ax2.plot(x_inc,y_inc,x_inc,y_phase_shift)

y_interference = y_inc + y_phase_shift
ax2.plot(x_inc,y_interference)



