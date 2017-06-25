# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 20:09:06 2016

@author: Bonan
"""

import simClasses as sim
import matplotlib.pyplot as plt
import numpy as np
from colourTools import specToRGB
plt.rcParams['figure.figsize'] = (8,6)
plt.rcParams['savefig.dpi'] = 100
#%%
#define materials
CNC = sim.UniaxialMaterial(1.586,1.524) # this might not be right
air = sim.HomogeneousNondispersiveMaterial(1)
cellulose = sim.HomogeneousNondispersiveMaterial(1.55)
water = sim.HomogeneousNondispersiveMaterial(1.33)
# Set the glass as a practical backend
glass = sim.HomogeneousNondispersiveMaterial(1.55)
front = sim.IsotropicHalfSpace(air)
airhalf= sim.IsotropicHalfSpace(air)
glasshalf = sim.IsotropicHalfSpace(glass)
s = sim.OptSystem()
s.setHalfSpaces(airhalf,glasshalf)
#set chiral material
heli = sim.HeliCoidalStructure
h1 = heli(material = CNC, pitch = 150, t = 1000)  # t is thickness
s.setStructure([h1])
wlRange = np.linspace(350,850,200)
print('Followings are added to the scope')
print('Materials: CNC, air, cellulosem, glass')
print('HalfSpace: airhalf, glasshalf')
print('OptSystem:s')
print('heli as HeliCoidalStructure')
print('wlRange as 400 to 800 nm')

def plotSpectrum(OptSys, wlRange):
    result = OptSys.scanSpectrum(wlRange)
    plt.plot(result[0],result[1], color = specToRGB(result))
    plt.show()
    return 

def mix_material(proportion = [1,1,1], materials = [CNC, air, water]):
    for i,j in zip(proportion, materials):
        print(i, j)



def swelling(dry_pitch, wet_pitch, step):
    pitch_range = np.linspace(dry_pitch, wet_pitch, step)
    for i in pitch_range:
        h1 = heli(material = CNC, pitch = i, t = 2000)  # t is thickness
        s.setStructure([h1])
        s.Theta = 1
        res = s.scanSpectrum(wlRange)
        plt.plot(res[0],res[1])
        
def plot_CNC(pitch, thickness):
    h1 = heli(material = CNC, pitch = pitch, t = thickness)  # t is thickness
    s.setStructure([h1])
    s.Theta = 1
    res = s.scanSpectrum(wlRange)
    plt.plot(res[0],res[1])


# different pitch distance for red shift
for pitch in [150,200,250,300,350,400]:
    i = 10 # number of layers
    plot_CNC(pitch = pitch, thickness = pitch*i)



plt.show()



