import numpy
import peakutils
from peakutils.plot import plot as pplot
from matplotlib import pyplot

centers = (30.5, 72.3)
x = numpy.linspace(0, 120, 121)
y = (peakutils.gaussian(x, 5, centers[0], 3) +
    peakutils.gaussian(x, 7, centers[1], 10) +
    numpy.random.rand(x.size))
print(type(y))
pyplot.figure(figsize=(10,6))
pyplot.plot(x, y)
pyplot.title("Data with noise")

indexes = peakutils.interpolate(x,y, width = 10)
print(type(indexes))
print(x[indexes], y[indexes])
pyplot.figure(figsize=(10,6))
pplot(x, y, indexes)
pyplot.title('First estimate')

pyplot.show()
