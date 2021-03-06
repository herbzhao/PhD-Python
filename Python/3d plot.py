import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
ax = fig.gca(projection='3d')

#n is the number of periods
n = 3

theta = np.linspace( 0,  2*n*np.pi, 100)

x0 = np.linspace(0, 0, 100)
y0 = np.linspace(0, 2*n*np.pi, 100)
z0 = np.linspace(0, 0, 100)
ax.plot(x0, y0 ,z0, label='central', c= 'k')

x1 = np.linspace(0, 0, 100)
y1 = np.linspace(0, 2*n*np.pi, 100)
z1 = np.sin(theta)
ax.plot(x1, y1 ,z1, label='z-axis')


x2 = np.sin(theta+np.pi/2)  
#this creates the phase difference due to liquid crystal
y2 = np.linspace(0, 2*n*np.pi, 100)
z2 = np.linspace(0, 0, 100)
ax.plot(x2,y2, z2, label='x-axis')


x3 = x1+x2
y3 = (y1+y2)/2
z3 = z1+z2
ax.plot(x3,y3, z3, label='combined')

    
ax.legend()

plt.show()