from CNC import chiral_nematic_simulation

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
        n_CNC_water_mixture  = (np.square(np.sqrt(self.CNC[0])*(1-water_volume_fraction)+np.sqrt(water)*water_volume_fraction),
                            np.square(np.sqrt(self.CNC[1])*(1-water_volume_fraction)+np.sqrt(water)*water_volume_fraction))
        return n_CNC_water_mixture

    def pitch_change_only(self):
        ' for swelling with only pitch change (the number of repeats stayed the same)'
        simulation_parameters = {}
        for water_volume_fraction in self.water_infiltration_fractions:
            swollen_thickness = self.original_thickness/(1-water_volume_fraction)
            swollen_pitch = swollen_thickness/self.original_pitch
            # unchanged refractive index
            n_swollen_CNC_water_mixture = self.CNC
            # create a dictionary to store n, pitch and thickness for corresponding water_volume_fraction
            simulation_parameters_set[water_volume_fraction] = {'n': n_swollen_CNC_water_mixture, 'pitch': swollen_pitch, 'thickness': swollen_thickness}
        return simulation_parameters_set

    def refractive_index_change_only(self):
        ' for swelling with only refractive index change (the thickness unchanged)'
        simulation_parameters = {}
        for water_volume_fraction in self.water_infiltration_fractions:
            # unchanged thickness and pitch (filling the pores)
            swollen_thickness = self.original_thickness
            swollen_pitch = self.original_pitch
            n_swollen_CNC_water_mixture = self.CNC_water_mixture_refractive_index(water_volume_fraction)
            # create a dictionary to store n, pitch and thickness for corresponding water_volume_fraction
            simulation_parameters_set[water_volume_fraction] = {'n': n_swollen_CNC_water_mixture, 'pitch': swollen_pitch, 'thickness': swollen_thickness}
        return simulation_parameters_set

    def pitch_change_refractive_index_change(self):
        'for swelling with both refractive index change and pitch change'
        simulation_parameters = {}
        for water_volume_fraction in self.water_infiltration_fractions:
            swollen_thickness = self.original_thickness/(1-water_volume_fraction)
            swollen_pitch = swollen_thickness/self.original_pitch
            n_swollen_CNC_water_mixture = self.CNC_water_mixture_refractive_index(water_volume_fraction)
            # create a dictionary to store n, pitch and thickness for corresponding water_volume_fraction
            simulation_parameters_set[water_volume_fraction] = {'n': n_swollen_CNC_water_mixture, 'pitch': swollen_pitch, 'thickness': swollen_thickness}
        return simulation_parameters_set


if __name__ == "__main__":
    CNC_water_infiltration_simulation = CNC_water_infiltration_simulation_method()
    # define some initial parameters
    CNC_water_infiltration_simulation.CNC = (1.51, 1.59)
    CNC_water_infiltration_simulation.original_pitch = 300e-9
    CNC_water_infiltration_simulation.original_thickness = 3500e-9
    CNC_water_infiltration_simulation.water_infiltration_fractions = [0,0.06,0.14,0.23,0.35,0.44]
    
    simulation_parameters_set = CNC_water_infiltration_simulation.pitch_change_only()
    simulation_parameters_set = CNC_water_infiltration_simulation.refractive_index_change_only()
    simulation_parameters_set = CNC_water_infiltration_simulation.pitch_change_refractive_index_change()

    for condition_set in simulation_parameters_set():
        simulation_parameters_set[condition_set] 
        condition_set



    # Simulation of CNC domain or stacks of domains with z-twist
    chiral_nematic_simulation = chiral_nematic_simulation_method()
    chiral_nematic_simulation.CNC = (1.51, 1.59)
    CNC_layer = chiral_nematic_simulation.create_chiral_nematic_layer(pitch = 300e-9, thickness = 3500e-9, z_rotate_angle = 0)
    #CNC_interface = chiral_nematic_simulation.isotropic_layer(refractive_index = 1.6, thickness = 10e-9)
    #CNC_layer_2 = chiral_nematic_simulation.create_chiral_nematic_layer(material = CNC, half_pitch = 185e-9, thickness = 2000e-9, z_rotate_angle = 0)
    chiral_nematic_simulation.calculate_structure(material_layers = [CNC_layer[0], CNC_layer[1]])

    # simulation conditions: refer to chiral_nematic_simulation.calculate_structure()
    conditions = ['R_RR','R_LL','R_pp','R_sp']
    # save result to csv
    chiral_nematic_simulation.folder = r'C:\Users\herbz\Documents\GitHub\PhD-python\model the light\Berreman4x4-master\examples'
    chiral_nematic_simulation.output_filename = r'simple_chiral_nematic_film'
    chiral_nematic_simulation.output_data_to_csv(conditions = conditions)
    # plot
    chiral_nematic_simulation.plotting(conditions = conditions)