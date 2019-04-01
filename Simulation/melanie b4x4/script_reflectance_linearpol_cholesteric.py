import B4x4
from matplotlib import pyplot as plt

print('start')

theta_deg_in = 0
lbda_min_nm = 400
lbda_max_nm = 800
sim = B4x4.Factory(theta_deg_in, lbda_min_nm, lbda_max_nm)
res = sim.getReflTrans()
r_pp = [i[0][0][0] for i in res]  # reflected p component for a p incident wave, one per wl
r_ps = [i[0][0][1] for i in res]  # reflected p component for a s incident wave, one per wl
r_sp = [i[0][1][0] for i in res]  # reflected s component for a p incident wave, one per wl
r_ss = [i[0][1][1] for i in res]  # reflected s component for a s incident wave, one per wl
t_pp = [i[1][0][0] for i in res]  # transmitted p component for a p incident wave, one per wl
t_ps = [i[1][0][1] for i in res]  # transmitted p component for a s incident wave, one per wl
t_sp = [i[1][1][0] for i in res]  # transmitted s component for a p incident wave, one per wl
t_ss = [i[1][1][1] for i in res]  # transmitted s component for a s incident wave, one per wl

fig = plt.figure()
ax = fig.add_subplot("111")
lbda_list = range(lbda_min_nm, lbda_max_nm, 1)
ax.plot(lbda_list, r_pp, '-', label="p-pol to p-pol")
ax.plot(lbda_list, r_ps, '-', label="s-pol to p-pol")
ax.plot(lbda_list, r_sp, '--', label="p-pol to s-pol")
ax.plot(lbda_list, r_ss, '-', label="s-pol to s-pol")
plt.legend()
ax.set_xlabel(r"Wavelength $\lambda_0$ (nm)")
ax.set_ylabel(r"Reflectance $R$")
fmt = ax.xaxis.get_major_formatter()
fmt.set_powerlimits((-3, 3))
plt.show()

print('end')
