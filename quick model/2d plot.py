import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt

mpl.rcParams['legend.fontsize'] = 10

fig, ax = plt.subplots()

#n is the number of periods
n = 3

theta = np.linspace( 0,  0.5*np.pi, 100)

x1 = np.linspace(0, 90, 100)
y1 = np.sin(theta)
y2 = 1/np.sin(theta)
ax.plot(x1, y1, label='sin(theta)')
ax.plot(x1, y2, label = 'sin(theta)^-1')
ax.set_xlim((30, 90)) 
ax.set_ylim((0,y2[30]))



ax.legend(fontsize = 30)

plt.show()