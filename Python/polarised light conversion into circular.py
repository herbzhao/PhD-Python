import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

# This shows a polarised light can be made up with two 
# circular polarised light component (different handedness)
# Chiral structure can reflect same handedness component

mpl.rcParams['legend.fontsize'] = 10

# Get instance of Axis3D
fig = plt.figure(figsize=(5,5),dpi=300)
ax = plt.subplot(111,projection='3d')

#n is the number of periods
n = 3

theta = np.linspace( 0,  2*n*np.pi, 100)

#indicate the rotating axis
x0 = np.linspace(0, 0, 100)
y0 = np.linspace(0, 2*n*np.pi, 100)
z0 = np.linspace(0, 0, 100)
ax.plot(x0, y0 ,z0, label='central', c= 'k')


#component light 1
x1 = np.linspace(0, 0, 100)
y1 = np.linspace(0, 2*n*np.pi, 100)
z1 = np.sin(theta)
#ax.plot(x1, y1 ,z1, label='z-axis')

#component light 2
x2 = np.sin(theta+np.pi/2)  
#this creates the phase difference due to liquid crystal
y2 = np.linspace(0, 2*n*np.pi, 100)
z2 = np.linspace(0, 0, 100)
#ax.plot(x2,y2, z2, label='x-axis')

# 1 + 2 = combined circular polarised light 3  - left handed
x3 = (x1+x2)
y3 = (y1+y2)/2
z3 = z1+z2
ax.plot(x3,y3, z3, label='left hand')


#Right handed circular polarised light 4 

x4 = -1*(x1+x2)
y4 = (y1+y2)/2
z4 = z1+z2
ax.plot(x4,y4,z4, label='right hand')


#New polarised light by combined circular light 3,4
x5 = x3+x4
y5 = (y3+y4)/2
z5 = z3+z4
ax.plot(x5,y5,z5, label='combined')

ax.set_xlim3d(-2,2)
#ax.set_ylim3d(-2,2)
ax.set_zlim3d(-2,2)

#change viewing angle
ax.view_init(azim=45, elev=0)
    
ax.legend()

plt.show()


