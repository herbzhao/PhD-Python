#!/usr/bin/python
# encoding: utf-8

# Berreman4x4 example
# Author: O. Castany, C. Molinaro

# Example of a cholesteric liquid crystal

import numpy, Berreman4x4
from numpy import sin, sqrt, abs
from Berreman4x4 import c, pi, e_y
import matplotlib.pyplot as pyplot

# Materials
glass = Berreman4x4.IsotropicNonDispersiveMaterial(1.55)
front = back = Berreman4x4.IsotropicHalfSpace(glass)

# Cholesteric parameters
# Liquid crystal oriented along the x direction
(no, ne) = (1.53, 1.58)
Dn = ne-no  # birefriengence
n_med = (ne + no)/2 # average n

# Creates a uniaxial (bi-refringent) non-dispersive material: https://www.tulane.edu/~sanelson/eens211/uniaxial_minerals.htm
# An optical axis is a line along with rotational symmetry 
LC = Berreman4x4.UniaxialNonDispersiveMaterial(no, ne)  # ne along z
# Returns rotation matrix defined by a unit rotation vector and an angle
R = Berreman4x4.rotation_v_theta(e_y, pi/2) # rotation of pi/2 along y
# Change non-dispersive material into a rotated material with the rotation matrix
LC = LC.rotated(R)                          # apply rotation from z to x
# Cholesteric pitch:
p = 300e-9
# half pitch of left handed (angle = -pi)
TN = Berreman4x4.TwistedMaterial(material=LC, d=p/2, angle=-pi, div=30)
TN_interface = Berreman4x4.TwistedMaterial(material=LC, d=p/2/2, angle=-pi/2, div=30/8)


# A layer made of one material - thickness is already specified by material
# Inhomogeneous layer, repeated layer, and structure
IL = Berreman4x4.InhomogeneousLayer(TN)
IL_interface = Berreman4x4.InhomogeneousLayer(TN_interface)
N = 15      # number half pitch repetitions
h = N * p/2 # thickness


# Repetition of a structure.
# (layers=None, n=2, before=0, after=0)
L = Berreman4x4.RepeatedLayers(layers=[IL], n=N)

#  the final structure to be simulated
s = Berreman4x4.Structure(front, [L, IL_interface, L], back)

# Normal incidence, Reduced incidence wavenumber
Kx = 0.0

# Calculation parameters
(lbda_min, lbda_max) = (400e-9, 800e-9)   # range of simulation
lbda_list = numpy.linspace(lbda_min, lbda_max, 200) # number of calculated wavelength
k0_list = 2*pi/lbda_list    #'k0' : wave vector in vacuum, k0 = ω/c = 2pi/lambda

############################################################################
# Analytical calculation for the maximal reflection
R_th = numpy.tanh(Dn/n_med*pi*h/p)**2
lbda_B = p * n_med      # peak wavelenght
lbda_B1, lbda_B2 = p*no, p*ne   #peak width

############################################################################
# Calculation with Berreman4x4
data = Berreman4x4.DataList([s.evaluate(Kx,k0) for k0 in k0_list])

#Examples for 'name'...
# Naming convention (Fujiwara, p. 220):
# 't_ps' : transmitted 'p' component for an 's' incident wave
# 't_ss' : transmitted 's' component for an 's' incident wave
# 'r_LR' : Reflection of LCP channel from a RCP light
T_pp = data.get('T_pp')
T_ps = data.get('T_ps')
T_ss = data.get('T_ss')
T_sp = data.get('T_sp')

# Transmission coefficients for incident unpolarized light:
T_pn = 0.5 * (T_pp + T_ps)
T_sn = 0.5 * (T_sp + T_ss)
T_nn = T_sn + T_pn

# Transmission coefficients for 's' and 'p' polarized light, with 
# unpolarized measurement.
T_ns = T_ps + T_ss
T_np = T_pp + T_sp

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

###########################################################################
# Jones matrices for the circular wave basis

# Right-circular wave is reflected in the stop-band.
# R_LR, T_LR close to zero.

# First R, T is reflection and transmission
# Second R and L is the incident light (Right handed)
# Third is the filter channel before sensor

R_RR = data.get('R_RR')
T_RR = data.get('T_RR')

# Left-circular wave is transmitted in the full spectrum.
# T_RL, R_RL, R_LL close to zero, T_LL close to 1.
T_LL = data.get('T_LL')
R_LL = data.get('R_LL')

# Cross polarisation and Parallel polarisation
R_ss = data.get('R_ss')
R_pp = data.get('R_pp')
R_sp = data.get('R_sp')
R_ps = data.get('R_ps')

############################################################################
# Plotting
fig = pyplot.figure()
ax = fig.add_subplot("111")

# Analytical results
# Draw rectangle for λ ∈ [p·no, p·ne], and T ∈ [0, R_th]  
#rectangle = pyplot.Rectangle((lbda_B1,0), lbda_B2-lbda_B1, R_th, color='cyan')
#ax.add_patch(rectangle)


ax.plot(lbda_list, R_LL, '--', label='R_LL')
ax.plot(lbda_list, R_RR, label='R_RR')
#ax.plot(lbda_list, T_RR, label='T_RR')

#ax.plot(lbda_list, R_ss, label='R_ss')
#ax.plot(lbda_list, R_pp, label='R_pp')
#ax.plot(lbda_list, R_sp, label='R_sp')
#ax.plot(lbda_list, R_ps, label='R_ps')
#ax.plot(lbda_list, T_ns, label='T_ns')
#ax.plot(lbda_list, T_np, label='T_np')

ax.legend(loc='center right', bbox_to_anchor=(1.00, 0.50))

ax.set_title("Right-handed Cholesteric Liquid Crystal, aligned along \n" + 
             "the $x$ direction, with {:.1f} helix pitches.".format(N/2.))
ax.set_xlabel(r"Wavelength $\lambda_0$ (m)")
ax.set_ylabel(r"Power transmission $T$ and reflexion $R$")
fmt = ax.xaxis.get_major_formatter()
fmt.set_powerlimits((-3,3))

stack = s.drawStructure()
pyplot.show()


