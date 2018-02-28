import numpy as np
from CNC import chiral_nematic_simulation_method
import matplotlib.pyplot as plt

class CNC_water_infiltration_simulation_method():
    def __init__(self):
        self.water = 1.33
        # input value to change this
        self.CNC = (1.51, 1.59) 
        self.original_pitch = 300e-9
        self.original_thickness = 3500e-9
        self.water_infiltration_fractions = [0,0.06,0.14,0.23,0.35,0.44]
    
    def CNC_water_mixture_refractive_index(self, water_volume_fraction):
        'Calculate the new refractive index based on volume fraction'
        # dielectric constant epsilon is sqrt of refractive index
        # for composite materials, dielectric constant calculation: 
        # e = e1*v1 + e2*v2  v is the volume fraction   http://www.sciencedirect.com/science/article/pii/S0030401899006951
        n_CNC_water_mixture  = (np.square(np.sqrt(self.CNC[0])*(1-water_volume_fraction)+np.sqrt(self.water)*water_volume_fraction),
                            np.square(np.sqrt(self.CNC[1])*(1-water_volume_fraction)+np.sqrt(self.water)*water_volume_fraction))
        return n_CNC_water_mixture

    def pitch_change_only(self):
        ' for swelling with only pitch change (the number of repeats stayed the same)'
        simulation_parameters_set = {}
        for water_volume_fraction in self.water_infiltration_fractions:
            swollen_thickness = self.original_thickness/(1-water_volume_fraction)
            swollen_pitch = swollen_thickness/(self.original_thickness/self.original_pitch)
            # unchanged refractive index
            n_swollen_CNC_water_mixture = self.CNC
            # create a dictionary to store n, pitch and thickness for corresponding water_volume_fraction
            simulation_parameters_set[water_volume_fraction] = {'n': n_swollen_CNC_water_mixture, 'pitch': swollen_pitch, 'thickness': swollen_thickness, 'rotation': 0}
        return simulation_parameters_set

    def refractive_index_change_only(self):
        ' for swelling with only refractive index change (the thickness unchanged)'
        simulation_parameters_set = {}
        for water_volume_fraction in self.water_infiltration_fractions:
            # unchanged thickness and pitch (filling the pores)
            swollen_thickness = self.original_thickness
            swollen_pitch = self.original_pitch
            n_swollen_CNC_water_mixture = self.CNC_water_mixture_refractive_index(water_volume_fraction)
            # create a dictionary to store n, pitch and thickness for corresponding water_volume_fraction
            simulation_parameters_set[water_volume_fraction] = {'n': n_swollen_CNC_water_mixture, 'pitch': swollen_pitch, 'thickness': swollen_thickness, 'rotation': 0}
        return simulation_parameters_set

    def pitch_change_refractive_index_change(self):
        'for swelling with both refractive index change and pitch change'
        simulation_parameters_set = {}
        for water_volume_fraction in self.water_infiltration_fractions:
            swollen_thickness = self.original_thickness/(1-water_volume_fraction)
            swollen_pitch = swollen_thickness/(self.original_thickness/self.original_pitch)
            n_swollen_CNC_water_mixture = self.CNC_water_mixture_refractive_index(water_volume_fraction)
            # create a dictionary to store n, pitch and thickness for corresponding water_volume_fraction
            simulation_parameters_set[water_volume_fraction] = {'n': n_swollen_CNC_water_mixture, 'pitch': swollen_pitch, 'thickness': swollen_thickness, 'rotation': 0}
        return simulation_parameters_set


if __name__ == "__main__":    
    # Simulation of CNC domain or stacks of domains with z-twist
    chiral_nematic_simulation = chiral_nematic_simulation_method()
    # Normally use it 0~1, higher the number, slower the simulation
    chiral_nematic_simulation.simulation_accuracy = 0.7
    # simulation conditions: refer to chiral_nematic_simulation.calculate_structure()
    chiral_nematic_simulation.simulation_modes = ['R_LL']

    # range of wavelength to be simulated
    wavelength_range = (300e-9, 1000e-9)
    chiral_nematic_simulation.set_WLrange(wavelength_range)    

    # get parameters form water swelling
    CNC_water_infiltration_simulation = CNC_water_infiltration_simulation_method()
    # define some initial parameters
    CNC_water_infiltration_simulation.CNC = (1.51, 1.59)
    CNC_water_infiltration_simulation.original_pitch = 300e-9
    CNC_water_infiltration_simulation.original_thickness = 3500e-9
    CNC_water_infiltration_simulation.water_infiltration_fractions = [0,0.06,0.14,0.23,0.35,0.44]
    
    # type of water swelling mechanisms 
    simulation_parameters_set = CNC_water_infiltration_simulation.pitch_change_refractive_index_change()
     # the folder to save csv
    chiral_nematic_simulation.output_filename = 'pitch_change_refractive_index_change'
    chiral_nematic_simulation.folder = r'C:\Users\herbz\Documents\GitHub\PhD-python\model the light\Berreman4x4-master\examples'
    
    # simulation
    layer1_parameters_set = simulation_parameters_set
    layer2_parameters_set = None
    interface_parameters_set = None
    chiral_nematic_simulation.multiple_materials_layers_parameter_sets(
                                        layer1_parameters_set=layer1_parameters_set,
                                        layer2_parameters_set=layer2_parameters_set,
                                        interface_parameters_set=interface_parameters_set)

    # show the plot in the end to prevent jam
    plt.show()