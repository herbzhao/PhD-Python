import B4x4
from matplotlib import pyplot as plt

print('start')

theta_deg_in_list = range(0, 91, 1)
lbda_min_nm = 500
lbda_max_nm = 500
r_pp = []
r_ps = []
r_sp = []
r_ss = []

fig = plt.figure()
ax = fig.add_subplot("111")

for theta_deg_in in theta_deg_in_list:
    sim = B4x4.Factory(theta_deg_in, lbda_min_nm, lbda_max_nm)
    res = sim.getReflTrans()
    r_pp.append(res[0][0][0][0])  # reflected p component for a p incident wave, one per wl
    r_ps.append(res[0][0][0][1])  # reflected p component for a s incident wave, one per wl
    r_sp.append(res[0][0][1][0]) # reflected s component for a p incident wave, one per wl
    r_ss.append(res[0][0][1][1]) # reflected s component for a s incident wave, one per wl
print("---")

ax.plot(theta_deg_in_list, r_pp, '-', label="p-pol to p-pol")
ax.plot(theta_deg_in_list, r_ps, '-', label="s-pol to p-pol")
ax.plot(theta_deg_in_list, r_sp, '--', label="p-pol to s-pol")
ax.plot(theta_deg_in_list, r_ss, '-', label="s-pol to s-pol")

plt.legend()
plt.show()

print('end')
