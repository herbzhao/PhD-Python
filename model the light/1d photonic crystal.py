# -*- coding: utf-8 -*-
"""
Examples of plots and calculations using the tmm package.
"""

from __future__ import absolute_import, division, print_function

import matplotlib.pyplot as plt
from numpy import array, inf, linspace, pi
from scipy.interpolate import interp1d
from tmm.tmm_core import (coh_tmm, ellips, find_in_structure_with_inf, inc_tmm,
                          position_resolved, unpolarized_RT)

try:
    import colorpy.illuminants
    import colorpy.colormodels
    from . import color
    colors_were_imported = True
except ImportError:
    # without colorpy, you can't run sample5(), but everything else is fine.
    colors_were_imported = False


class transfer_matrix():

    def __init__(self, name):
        self.degree = pi/180
        self.wavelength_min_nm = 150
        self.wavelength_max_nm = 1200
        self.wavelength_range = linspace(wavelength_min_nm, wavelength_max_nm, num=400)

    def material(self, refractive_index, thickness):
        ' usage: air = material(1.55, 250 / material_2_n)'

        # refractive index
        return (refractive_index, thickness)
    
    def material_refractive_index(self, wavelength_dependent_n):
        # empty 2d array
        refractive_index = np.array([[],[]])
        for wavelength in self.wavelength_range:
            np.append(refractive_index, [[wavelength],[refractive_index]])

            

    def new_multilayer(self, number_of_repeats = 10, *materials):
        ' usage: air = material(1.55, 250 / material_2_n)'
        self.d_list = []
        self.n_list = []
        # air on top
        self.d_list.append(inf)
        self.n_list.append(1)
        for i in range(0, number_of_repeats):
            self.d_list.append(material_1_d)
            self.d_list.append(material_2_d)
            self.n_list.append(material_1_n)
            self.n_list.append(material_2_n)
        # air on the bottom
        self.d_list.append(inf)
        self.n_list.append(1)

def sample1():
    """
    Here's a thin non-absorbing layer, on top of a thick absorbing layer, with
    air on both sides. Plotting reflected intensity versus wavenumber, at two
    different incident angles.

    The sensor is like a intergrated sphere (picking up all the reflected light),
    In reality, the illuminated light angle and fibre accepting angle is the same and determined by Numerical Aperture,
    
    in the case of perfect material, this creates no difference.
    """
    degree = pi/180

    wavelength_min_nm = 150
    wavelength_max_nm = 1200
    wavelength = linspace(wavelength_min_nm, wavelength_max_nm, num=400)


    # number of repeats
    n = 10
    material_2_n = 1
    material_1_n = 1.55
    material_2_d = 250 / material_2_n
    material_1_d = 0.000000001 / material_1_n
    # list of layer thicknesses in nm
    d_list = []
    n_list = []
    d_list.append(inf)
    n_list.append(1)
    for i in range(0,n):
        d_list.append(material_1_d)
        d_list.append(material_2_d)
        n_list.append(material_1_n)
        n_list.append(material_2_n)
    d_list.append(inf)
    n_list.append(1)
    # list of refractive indices
    #n_list = [1, 2.2, 3.3+0.3j, 1]

    # initialize lists of y-values to plot
    Rnorm = [] # reflection at normal direction
    R45 = [] # reflection at 45 direction
    for i in wavelength:
		# For normal incidence, s and p polarizations are identical.
		# I arbitrarily decided to use 's'.

        # coh_tmm(pol, n_list, d_list, th_0, lam_vac)
        # th_0 is the angle of incidence: 0 for normal, pi/2 for glancing.
        Rnorm.append(coh_tmm('s', n_list, d_list, 0, i)['R'])
        #R45.append(unpolarized_RT(n_list, d_list, 45*degree, i)['R'])

    plt.figure()
    plt.plot(wavelength, Rnorm, 'blue', label= 'normal')
    #plt.plot(wavelength, R45, 'purple', label= '45')

   #plt.xlabel('k (cm$^{-1}$)')
    plt.xlabel('lambda')
    plt.ylabel('Fraction reflected')
    plt.legend()
    plt.title('Reflection of unpolarized light at 0$^\circ$ incidence (blue), '
              '45$^\circ$ (purple)', fontsize = 50)
    plt.show()

sample1()
