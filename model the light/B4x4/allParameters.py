import B4x4
mySimulation = B4x4.Factory()

##### set parameters here ###########
mySimulation.nSuperstrate = 1
mySimulation.nSubstrate = 1.555
mySimulation.pitch= 200         #   pitch in nm (180 degree twist)
mySimulation.no=    1.586         #    refractive index of ordinary ray
mySimulation.ne=    1.524         #   refractive index of extraordinary ray
mySimulation.nSuperstrate= 1  # refractive index of superstrate (air=        # n = 1)
mySimulation.nSubstrate= 1.44    #   refractive index of suberstrate (PS=        # n = 1.59, SiO2=        # n=1.55)
mySimulation.stack=  100        #   number of pitches (180 degree twist) in the structure
mySimulation.angle= 0         #  angle of incidence in degrees
mySimulation.lbda_min= 400      #   wavelength min (in meters)
mySimulation.lbda_max= 800      #   wavelength max (in meters)
mySimulation.points=  500       #  number of data points in simulation
mySimulation.slices=  100       # number of discrete anisotropic layers per 180 twist
#####################################

result = mySimulation.calculateL()
result.plot()
result.save('myResult.txt')