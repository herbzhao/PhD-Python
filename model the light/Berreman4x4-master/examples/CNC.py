#!/usr/bin/python
# encoding: utf-8

# Berreman4x4 example
# Author: O. Castany, C. Molinaro

# Example of a cholesteric liquid crystal

import numpy, Berreman4x4
from numpy import sin, sqrt, abs
from Berreman4x4 import c, pi, e_y, e_z, e_x
import matplotlib.pyplot as pyplot

# use pandas for data output 
import pandas as pd


class chiral_nematic_simulation_method():
    def __init__(self):
        # simulation wavelength range
        self.wavelength_range = (300e-9, 800e-9)   # range of simulation
        self.wavelength_list = numpy.linspace(self.wavelength_range[0], self.wavelength_range[1], 200) # number of calculated wavelength
        # Normal incidence, Reduced incidence wavenumber
        self.Kx = 0.0
        self.k0_list = 2*pi/self.wavelength_list    #'k0' : wave vector in vacuum, k0 = ω/c = 2pi/lambda
        # the illumination and analysing mode - refer to chiral_nematic_simulation.calculate_structure()
        self.simulation_modes = ['R_RR','R_LL','R_pp','R_sp']
        # a dictionary to store all the simulated results
        self.all_data = {}
        # run some methods in the beginning 
        self.materials()

    def materials(self):
        # Materials
        self.glass = Berreman4x4.IsotropicNonDispersiveMaterial(1.55)
        self.water = 1.33
        self.CNC = (1.51, 1.59)
        self.front = Berreman4x4.IsotropicHalfSpace(self.glass)
        self.back = Berreman4x4.IsotropicHalfSpace(self.glass)

    def create_isotropic_layer(self, refractive_index = 1.55, thickness = 10e-9):
        'Create an isotropic layer'
        isotropic_material = Berreman4x4.IsotropicNonDispersiveMaterial(refractive_index)
        # keep the syntax uniform, create two elements with same thickness
        return  [Berreman4x4.HomogeneousIsotropicLayer(isotropic_material, thickness/2), Berreman4x4.HomogeneousIsotropicLayer(isotropic_material, thickness/2)]

    def create_chiral_nematic_layer(self, refractive_index=(1.51, 1.59), pitch=300e-9, thickness=2000e-9, z_rotate_angle=0):
        ''' 
        The periodicity determines the length of helical axis - anything other than pi gives a incomplete structure and N should be 1

        z_rotate_angle rotate the whole structure around helical axis
        '''
        # Creates a uniaxial (bi-refringent) non-dispersive material: https://www.tulane.edu/~sanelson/eens211/uniaxial_minerals.htm
        # An optical axis is a line along with rotational symmetry 
        nematic = Berreman4x4.UniaxialNonDispersiveMaterial(refractive_index[0], refractive_index[1])  # ne along z
        
        # Returns rotation matrix defined by a unit rotation vector and an angle
        # rotation of pi/2 along y
        R = Berreman4x4.rotation_v_theta(e_y, pi/2)             
        # Change non-dispersive material into a rotated material with the rotation matrix (apply rotation from z to x)
        chiral_nematic = nematic.rotated(R)          

        # apply another rotation around z axis
        R_z = Berreman4x4.rotation_v_theta(e_z, z_rotate_angle)         
        chiral_nematic = chiral_nematic.rotated(R_z)     

        # Create structure based on thickness. The quotient is repeated layer and modulo as excessive bit to add on top
        N = int(thickness // pitch)
        excessive_fraction = (thickness % pitch)/pitch
        # excessive structure that does not finish a whole pitch
        chiral_nematic_excessive = Berreman4x4.TwistedMaterial(material=chiral_nematic, d=pitch*excessive_fraction, angle=-2*pi*excessive_fraction, div=80)
        chiral_nematic_excessive_layer = Berreman4x4.InhomogeneousLayer(chiral_nematic_excessive)

        # full pitch of left handed (angle = -2*pi)
        chiral_nematic = Berreman4x4.TwistedMaterial(material=chiral_nematic, d=pitch, angle=-2*pi, div=30)
        # create repeated layer for multiple pitches
        chiral_nematic_layer = Berreman4x4.InhomogeneousLayer(chiral_nematic)
        chiral_nematic_layer = Berreman4x4.RepeatedLayers(layers=[chiral_nematic_layer], n=N)

        return [chiral_nematic_layer, chiral_nematic_excessive_layer]


    def calculate_structure(self, materials_layers, description):
        'actual part to do the TMM simulation'
        # the final structure to be simulated
        # also draw the structure 
        self.structure = Berreman4x4.Structure(self.front, materials_layers, self.back)
        self.structure.drawStructure(description=description)
        # Calculation with Berreman4x4
        data = Berreman4x4.DataList([self.structure.evaluate(self.Kx,k0) for k0 in self.k0_list])

        self.simulation_results = {}

        ####################### all the results ###################################
        'this bit is obsolete now, keep it for reference'
        # Naming convention (Fujiwara, p. 220):
        # 't_ps' : transmitted 'p' component for an 's' incident wave
        # 't_ss' : transmitted 's' component for an 's' incident wave
        # 'r_LR' : Reflection of LCP channel from a RCP light
        self.simulation_results['T_pp'] = data.get('T_pp')
        self.simulation_results['T_ps'] = data.get('T_ps')
        self.simulation_results['T_ss'] = data.get('T_ss')
        self.simulation_results['T_sp'] = data.get('T_sp')
        self.simulation_results['T_RR'] = data.get('T_RR')
        self.simulation_results['T_LL'] = data.get('T_LL')

        # Transmission coefficients for incident unpolarized light:
        self.simulation_results['T_pn'] = 0.5 * (self.simulation_results['T_pp'] + self.simulation_results['T_ps'])
        self.simulation_results['T_sn'] = 0.5 * (self.simulation_results['T_sp'] + self.simulation_results['T_ss'])
        self.simulation_results['T_nn'] = self.simulation_results['T_sn'] + self.simulation_results['T_pn']

        # Transmission coefficients for 's' and 'p' polarized light, with 
        # unpolarized measurement.
        self.simulation_results['T_ns'] = self.simulation_results['T_ps'] + self.simulation_results['T_ss']
        self.simulation_results['T_np'] = self.simulation_results['T_pp'] + self.simulation_results['T_sp']

        ############################## Reflectance #########################
        # Jones matrices for the circular wave basis
        # Second R and L is the incident light (Right handed)
        # Third is the filter channel before sensor
        self.simulation_results['R_RR'] = data.get('R_RR')
        self.simulation_results['R_LL'] = data.get('R_LL')
        # Cross polarisation and Parallel polarisation
        self.simulation_results['R_ss'] = data.get('R_ss')
        self.simulation_results['R_pp'] = data.get('R_pp')
        self.simulation_results['R_sp'] = data.get('R_sp')
        self.simulation_results['R_ps'] = data.get('R_ps')

        return data

    def multiple_materials_layers(self, description='CNC simulation', layers=None):
        'input the layers and output the simulation results'        
        # flatten the list of lists and form the materials_layers
        materials_layers = [layer for pair in layers for layer in pair]
        # run simulation and append the data to self.all_data
        self.all_data[description] = self.calculate_structure(materials_layers, description=description)

        

    def multiple_materials_layers_parameter_sets(self, layer1_parameters_set=None, layer2_parameters_set=None, interface_parameters_set=None):
        'Use multiple parameters_set of differnet conditions to simulate (different water infiltration..)'
        # ensures the dictionary key 'condition' is the same for each set
        for condition in layer1_parameters_set:
            CNC_layer_1 = self.create_chiral_nematic_layer(
                                    refractive_index=layer1_parameters_set[condition]['n'],
                                    pitch=layer1_parameters_set[condition]['pitch'],
                                    thickness=layer1_parameters_set[condition]['thickness'],
                                    z_rotate_angle=layer1_parameters_set[condition]['rotation'])
        
            if not layer2_parameters_set is None:
                CNC_layer_2 = self.create_chiral_nematic_layer(
                                        refractive_index=layer2_parameters_set[condition]['n'],
                                        pitch=layer2_parameters_set[condition]['pitch'],
                                        thickness=layer2_parameters_set[condition]['thickness'],
                                        z_rotate_angle=layer2_parameters_set[condition]['rotation'])

            if not interface_parameters_set is None:    
                interface_layer = self.create_isotropic_layer(
                                        refractive_index=interface_parameters_set[condition]['n'], 
                                        thickness=interface_parameters_set[condition]['thickness'])
            # glue the layers together
            if interface_parameters_set is None:
                if layer2_parameters_set is None:
                    layers = [CNC_layer_1]
                else:
                    layers = [CNC_layer_1, CNC_layer_2]
            else:
                layers = [CNC_layer_1, interface_layer, CNC_layer_2]
            # run the simulation
            self.multiple_materials_layers(description=i,layers=layers)
        # save result to csv
        self.export_data_to_csv()
        self.plotting()
        
    

    def analytical_verification(self):
        'analytical results, ignore for now'

        birefirengence = abs(self.CNC[0] - self.CNC[1])  # birefriengence
        n_ave = (self.CNC[0] + self.CNC[1])/2 # average n

        ###########################################################################
        # Text output: eigenvalues and eigenvectors of the transmission matrix for 
        # a wavelength in the middle of the stop-band.
        i = numpy.argmin(abs(lbda_list-lbda_B))     # index for stop-band center
        T = data[i].T_ti                            # transmission matrix
        eigenvalues, eigenvectors = numpy.linalg.eig(T)
        numpy.set_printoptions(precision=3)
        print("\nTransmission in the middle of the stop-band...\n")
        print("Eigenvalues of the Jones transmission matrix:")
        print(eigenvalues)
        print("Corresponding power transmission:")
        print(abs(eigenvalues)**2)
        print("Corresponding eigenvectors:")
        print(eigenvectors)
        # Note: the transformation matrix to the eigenvector basis is
        # B = numpy.matrix(eigenvectors), and the matrix B⁻¹ T B is diagonal.
        print("Normalization to the 'p' componant:")
        print(eigenvectors/eigenvectors[0,:])
        print("Ratio 's'/'p':")
        print(abs(eigenvectors[1,:]/eigenvectors[0,:]))
        print("Complex angle (°) (+90°: L, -90°: R)")
        print(180/pi*numpy.angle(eigenvectors[1,:]/eigenvectors[0,:]))
        # We observe that the eigenvectors are nearly perfectly polarized circular waves

        ############################################################################
        # Analytical calculation for the maximal reflection
        R_th = numpy.tanh(Dn/n_med*pi*h/p)**2
        lbda_B = p * n_med      # peak wavelenght
        lbda_B1, lbda_B2 = p*no, p*ne   #peak width


    def plotting(self, simulation_modes=['R_RR', 'R_LL', 'R_ps', 'R_sp']):
        'plot all the conditions with all the modes'
        fig = pyplot.figure()
        ax = fig.add_subplot("111")
        for condition in self.all_data:
            for mode in self.simulation_modes:
                ax.plot(self.wavelength_list, self.all_data[condition].get(mode), label='{} in {}'.format(condition, mode))

        ax.legend(loc='center right', bbox_to_anchor=(1.00, 0.50))

        ax.set_title("chiral nematic structure")
        ax.set_xlabel(r"Wavelength $\lambda_0$ (m)")
        ax.set_ylabel(r"Normalised transmitance $T$ and reflectance $R$")
        #fmt = ax.xaxis.get_major_formatter()
        #fmt.set_powerlimits((-3,3))
        # draw the refractive index variation
        #self.structure.drawStructure()
        pyplot.show()

    def export_data_to_csv(self, simulation_modes=['R_RR', 'R_LL', 'R_ps', 'R_sp']):
        ''' 
        use panda to save the table into csv
        '''

        self.data_to_save = {}
        # this is the numpy array for wavelength
        self.data_to_save['wavelength'] = self.wavelength_list
        # these are the numpy array for intensity at different condition and mode
        for condition in self.all_data:
            for mode in self.simulation_modes:
                self.data_to_save['{}_{}'.format(condition, mode)] = self.all_data[condition].get(mode)

        self.df = pd.DataFrame(self.data_to_save)
        # reverse the columns
        columns = self.df.columns.tolist()
        columns = columns[-1:] + columns[:-1] 
        self.df = self.df[columns]
        self.df.to_csv(self.folder +'\\'+ self.output_filename + '.csv',  sep=',')
        print('saved to ' + self.folder +'\\'+ self.output_filename + '.csv')



if __name__ == "__main__":
    # Simulation of CNC domain or stacks of domains with z-twist
    chiral_nematic_simulation = chiral_nematic_simulation_method()
    # the folder to save csv
    chiral_nematic_simulation.output_filename = 'big and small'
    chiral_nematic_simulation.folder = r'C:\Users\herbz\Documents\GitHub\PhD-python\model the light\Berreman4x4-master\examples'
    
    # simulation conditions: refer to chiral_nematic_simulation.calculate_structure()
    chiral_nematic_simulation.simulation_modes = ['R_RR','R_LL']

    ########## create parameters for multiple layers () ##################
    CNC = (1.51, 1.59)
    layer1_parameters_set = {}
    layer1_parameters_set['test1'] = {'n': CNC, 'pitch': 300e-9, 'thickness': 600e-9, 'rotation': 0}
    layer1_parameters_set['test2'] = {'n': CNC, 'pitch': 300e-9, 'thickness': 600e-9, 'rotation': 0}

    # if only want to simulate one domain, set layer2_parameters_set and interface_parameters_set to None
    # layer2_parameters_set = None 
    layer2_parameters_set = {}
    layer2_parameters_set['test1'] = {'n': CNC, 'pitch': 300e-9, 'thickness': 600e-9, 'rotation': pi/2}
    layer2_parameters_set['test2'] = {'n': CNC, 'pitch': 300e-9, 'thickness': 600e-9, 'rotation': pi/2}

    # interface_parameters_set = None
    interface_parameters_set = {}
    interface_parameters_set['test1'] = {'n':1.55, 'thickness':200e-9}
    interface_parameters_set['test2'] = {'n':1.55, 'thickness':1000e-9}

    # run the simulation!
    chiral_nematic_simulation.multiple_materials_layers_parameter_sets(
                                        layer1_parameters_set=layer1_parameters_set,
                                        layer2_parameters_set=layer2_parameters_set,
                                        interface_parameters_set=interface_parameters_set)

