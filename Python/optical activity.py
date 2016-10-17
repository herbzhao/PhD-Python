import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

# This one shows combined light of 
# two Circular polarised light with phase difference 

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


# RHCP component light 1 - vertical
r_x1 = np.linspace(0, 0, 100)
r_y1 = np.linspace(0, 2*n*np.pi, 100)
r_z1 = np.sin(theta)
#ax.plot(r_x1, r_y1 ,r_z1, label='z-axis')

# RHCP component light 2 - horizontal
r_x2 = np.sin(theta-np.pi/2)  
#this creates the phase difference due to liquid crystal
r_y2 = np.linspace(0, 2*n*np.pi, 100)
r_z2 = np.linspace(0, 0, 100)
#ax.plot(r_x2,r_y2, r_z2, label='x-axis')


#RHCP
r_x = r_x1  + r_x2
r_y = r_y1
r_z = r_z1 + r_z2

ax.plot(r_x,r_y,r_z, label='RHCP')


#------------------------------------------------

# LHCP component light 1 - vertical

phase_diff = np.pi/1   #phase difference
ax.text(5, 0, 0, "Phase difference = ", color='red')
ax.text(5, 0, -1, str(phase_diff/np.pi/2), color='red')


l_x1 = np.linspace(0, 0, 100)
l_y1 = np.linspace(0, 2*n*np.pi, 100)
l_z1 = np.sin(theta+phase_diff)
#ax.plot(l_x1, l_y1 ,l_z1, label='z-axis')

# LHCP component light 2- horizontal
l_x2 = np.sin(theta-np.pi/2+phase_diff)* -1
#this creates the phase difference due to liquid crystal
l_y2 = np.linspace(0, 2*n*np.pi, 100)
l_z2 = np.linspace(0, 0, 100)
#ax.plot(l_x2,l_y2, l_z2, label='x-axis')

#LHCP
l_x = l_x1  + l_x2
l_y = l_y1
l_z = l_z1 + l_z2

ax.plot(l_x,l_y,l_z, label='LHCP')

#------------------------------------------------


#Combined linear light - exit
lin_x = r_x + l_x
lin_y = (r_y + l_y)/2
lin_z = r_z + l_z

ax.plot(lin_x,lin_y,lin_z, label='combined',c ='r')


ax.set_xlim3d(-2,2)
#ax.set_ylim3d(-2,2)
ax.set_zlim3d(-2,2)

#change viewing angle
#ax.view_init(azim=45, elev=0)
    
ax.legend()

plt.show()


