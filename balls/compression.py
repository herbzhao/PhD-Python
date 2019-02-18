# vol in ul
s_vol = 0.5
s_vol_um3 = s_vol * 10**9
# rad in um
s_rad = 500
s_area = s_rad**2 * np.pi
# height in um
s_height = s_vol_um3/s_area
# starting weight concentration
s_conc_wt = 8
# devide by density of CNC to get vol conc
s_conc_vol = s_conc_wt/1.6
print(s_conc_vol)