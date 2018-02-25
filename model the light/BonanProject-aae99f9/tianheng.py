# cd to the directory

import tm4.simClasses as sim
import matplotlib.pyplot as plt
import numpy as np
from tm4.colourTools import specToRGB

# to output the data into excel
import pandas as pd




class chiral_nematic_simulation():
    def __init__(self):
        # simulation wavelength range
        self.wlRange = np.linspace(300,900,300)
        pass

    def materials(self):
        self.CNC = sim.UniaxialMaterial(1.586,1.524) # this might not be right
        #self.CNC = sim.UniaxialMaterial(1.544,1.618)
        self.air = sim.HomogeneousNondispersiveMaterial(1)
        self.cellulose = sim.HomogeneousNondispersiveMaterial(1.55)
        # Set the glass as a practical backend
        self.glass = sim.HomogeneousNondispersiveMaterial(1.52)
        self.front = sim.IsotropicHalfSpace(self.air)
        self.airhalf= sim.IsotropicHalfSpace(self.air)
        self.glasshalf = sim.IsotropicHalfSpace(self.glass)

        # set space before and after the sample
        self.s = sim.OptSystem()
        # set space before and after the sample
        self.s.setHalfSpaces(self.airhalf ,self.glasshalf)
        


    def simple_film(self):
        # helicoidal structure with CNC, pitch and thickness
        heli = sim.HeliCoidalStructure
        h1 = heli(self.CNC,180,1000)
        # set structure for simulation
        self.s.setStructure([h1])
        result = self.s.scanSpectrum(self.wlRange)
        plt.plot(result[0],result[1], color = specToRGB(result))
        

    def chiral_nematic_film(self, materials, half_pitch = 180, thickness = 1000):
        # helicoidal structure with CNC, pitch and thickness
        heli = sim.HeliCoidalStructure
        h1 = heli(materials, half_pitch, thickness, d = 30)
        # set structure for simulation
        self.s.setStructure([h1])
        result = self.s.scanSpectrum(self.wlRange)
        plt.plot(result[0],result[1], color = specToRGB(result))
        return result
    

    def save_simulation_to_csv(self, simulated_results):
        # use panda to save the table into csv
        self.df = pd.DataFrame(simulated_results)
        # reverse the columns
        columns = self.df.columns.tolist()
        columns = columns[-1:] + columns[:-1] 
        self.df = self.df[columns]
        self.df.to_csv(self.folder +'\\'+ self.output_filename + '.csv',  sep=',')
        print('saved to ' + self.folder +'\\'+ self.output_filename + '.csv')


    def plot_spectrum(self):
        plt.rcParams['figure.figsize'] = (8,6)
        plt.rcParams['savefig.dpi'] = 100
        # change font size, axis  etc..
        plt.show()

    def CNC_water_mixture_refractive_index(self, water_volume_fraction):
        water = 1.33
        CNC = (1.586, 1.524)
        # dielectric constant epsilon is sqrt of refractive index
        # for composite materials, dielectric constant calculation: 
        # e = e1*v1 + e2*v2  v is the volume fraction   http://www.sciencedirect.com/science/article/pii/S0030401899006951
        CNC_water_mixture  = (np.square(np.sqrt(CNC[0])*(1-water_volume_fraction)+np.sqrt(water)*water_volume_fraction),
                            np.square(np.sqrt(CNC[1])*(1-water_volume_fraction)+np.sqrt(water)*water_volume_fraction))

        self.CNC_water_mixture  = sim.UniaxialMaterial(CNC_water_mixture[0], CNC_water_mixture[1])
        return self.CNC_water_mixture
        


def simulation_situations(simulation_situation):
    # for breathing test
    original_pseudo_layers = 50
    original_half_pitch = 150
    # this is the dictionary for panda to convert
    simulated_results = {}

    if simulation_situation == 'pitch_change_ignore_refractive_change':
        # for swelling with only pitch change (the number of repeats stayed the same)
        for water_volume_fraction in [0,0.06,0.14,0.23,0.35,0.44]:
            swollen_thickness = original_half_pitch*original_pseudo_layers/(1-water_volume_fraction)
            swollen_half_pitch = swollen_thickness/original_pseudo_layers
            simulated_result = chiral_simulation.chiral_nematic_film(materials = chiral_simulation.CNC, 
                                                  half_pitch = swollen_half_pitch, 
                                                  thickness = swollen_thickness)
            # wavelength
            simulated_results['wavelength'] = simulated_result[0]
            # intensity
            simulated_results['{} vol%'.format(water_volume_fraction)] = simulated_result[1]

    if simulation_situation == 'refractive_index_change_ignore_pitch_change':
        #for swelling with only refractive index change
        for water_volume_fraction in [0,0.1,0.2,0.3,0.4,0.5,0.6,0.65]:
            swollen_thickness = original_half_pitch*original_pseudo_layers/(1-water_volume_fraction)
            swollen_half_pitch = swollen_thickness/original_pseudo_layers
            CNC_water_mixture = chiral_simulation.CNC_water_mixture_refractive_index(water_volume_fraction)
            # the water is getting in between the CNC layers wihtout swelling the CNC
            simulated_result = chiral_simulation.chiral_nematic_film(materials = CNC_water_mixture, 
                                                  half_pitch = original_half_pitch, 
                                                  thickness = swollen_thickness)
            # wavelength
            simulated_results['wavelength'] = simulated_result[0]
            # intensity
            simulated_results['{} vol%'.format(water_volume_fraction)] = simulated_result[1]

    if simulation_situation == 'pitch_change_refractive_index_change':
        # for swelling with both refractive index change and pitch change
        for water_volume_fraction in [0,0.03, 0.06, 0.14,0.23,0.35,0.44]:
            swollen_thickness = original_half_pitch*original_pseudo_layers/(1-water_volume_fraction)
            swollen_half_pitch = swollen_thickness/original_pseudo_layers
            CNC_water_mixture = chiral_simulation.CNC_water_mixture_refractive_index(water_volume_fraction)
            simulated_result = chiral_simulation.chiral_nematic_film(materials = CNC_water_mixture, 
                                                  half_pitch = swollen_half_pitch, 
                                                  thickness = swollen_half_pitch*original_pseudo_layers)
            # wavelength
            simulated_results['wavelength'] = simulated_result[0]
            # intensity
            simulated_results['{} vol%'.format(water_volume_fraction)] = simulated_result[1]



    if simulation_situation == 'film_with_different_color_and_thickness':
        # for CNC with different film thickness
        RGB_half_pitch = [150, 185, 210]
        droplet_thickness = [2000, 8000]

        for film_thickness in droplet_thickness:
            for color_half_pitch in RGB_half_pitch:
                simulated_result = chiral_simulation.chiral_nematic_film(
                                        materials = chiral_simulation.CNC,
                                        half_pitch = color_half_pitch,
                                        thickness = film_thickness)
                # wavelength
                simulated_results['wavelength'] = simulated_result[0]
                # intensity
                simulated_results['thickness {}_pitch {}'.format(film_thickness, color_half_pitch)] = simulated_result[1]
        
    return(simulated_results)




chiral_simulation = chiral_nematic_simulation()
chiral_simulation.folder = r'D:\GDrive\Research\BIP\Humidity sensor project\data\Simulation'
chiral_simulation.output_filename = r'film_with_different_color_and_thickness'

chiral_simulation.materials()
simulated_results = simulation_situations('film_with_different_color_and_thickness')

chiral_simulation.save_simulation_to_csv(simulated_results)

chiral_simulation.plot_spectrum()
