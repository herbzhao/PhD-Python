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
n=(1+1.124/(1-0.011087/x**2))**.5


sample1()