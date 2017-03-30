# -*- coding: utf-8 -*-
"""
Examples of plots and calculations using the tmm package.
"""

from __future__ import division, print_function, absolute_import

from tmm.tmm_core import (coh_tmm, inc_tmm, unpolarized_RT, ellips,
                       position_resolved, find_in_structure_with_inf)

from numpy import pi, linspace, inf, array
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

try:
    import colorpy.illuminants
    import colorpy.colormodels
    from . import color
    colors_were_imported = True
except ImportError:
    # without colorpy, you can't run sample5(), but everything else is fine.
    colors_were_imported = False


# "5 * degree" is 5 degrees expressed in radians
# "1.2 / degree" is 1.2 radians expressed in degrees
degree = pi/180

def plot():
    plt.show()

def sample1():
    """
    Here's a thin non-absorbing layer, on top of a thick absorbing layer, with
    air on both sides. Plotting reflected intensity versus wavenumber, at two
    different incident angles.
    """
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
    wavelength_min_nm = 150
    wavelength_max_nm = 1200
    wavelength = linspace(wavelength_min_nm, wavelength_max_nm, num=400)

    # initialize lists of y-values to plot
    Rnorm = [] # reflection at normal direction
    R45 = [] # reflection at 45 direction
    for i in wavelength:
		# For normal incidence, s and p polarizations are identical.
		# I arbitrarily decided to use 's'.
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