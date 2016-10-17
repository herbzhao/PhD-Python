import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt

mpl.rcParams['legend.fontsize'] = 10

fig, ax = plt.subplots()

#n is the number of periods
n = 3

theta = np.linspace( 0,  2*n*np.pi, 100)



x1 = np.linspace(0, 0, 100)
y1 = np.linspace(0, 2*n*np.pi, 100)
z1 = np.sin(theta)
ax.plot(x1, y1 ,z1, label='z-axis')


    
ax.legend()

plt.show()