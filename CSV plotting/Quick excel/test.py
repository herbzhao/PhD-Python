import pandas as pd
import os
import matplotlib.pyplot as plt
pd.set_option('display.mpl_style', 'default') # Make the graphs a bit prettier
plt.rcParams['figure.figsize'] = (8, 5)


folder_path = r'D:\GDrive\Research\BIP\Humidity sensor project\profilometer spot\20180221 - profilometry'
list_of_csv = os.listdir(folder_path)
# print(list_of_csv)

df = pd.read_csv("{}\{}".format(folder_path, list_of_csv[10]), skip_blank_lines=False, header=22, usecols=['Lateral(mm)','Total Profile(nm)'],)
print(list(df))

fig = plt.figure()
ax = fig.add_subplot("111")
ax.plot()
plt.show()
