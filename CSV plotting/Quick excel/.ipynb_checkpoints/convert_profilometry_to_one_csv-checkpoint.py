#%%
import pandas as pd
import os
import matplotlib.pyplot as plt


#%%
folder_path = r'D:\GDrive\Research\BIP\Humidity sensor project\profilometer spot\20180221 - profilometry'
list_of_csv = os.listdir(folder_path)
output_file_name = 'combined_profilometry.csv'

#%%
''' Go through all the files '''
df_list = []
for file in list_of_csv:
    if '.csv' in file:
        if not output_file_name in file:
            df_temp = pd.read_csv(r"{}\{}".format(folder_path, file), skip_blank_lines=False, header=22, usecols=['Lateral(mm)','Total Profile(nm)'])
            # change the y axis  name to the sample name
            df_temp.rename(columns={"Total Profile(nm)": file}, inplace=True)
            df_list.append(df_temp)

# combine all the df into a big one
combined_df = pd.concat(df_list, axis=1)
#print(list(combined_df))

# create multiple figures
#combined_df.to_csv(r'{}\{}'.format(folder_path, len(list(combined_df)/2)))

#for i in range(len(list(combined_df)/2)): 
#    axes[i].set_title()


#

#
# use the number to call different columns with iloc
print(combined_df.iloc[:, [0,1]])

#%%
number_of_csvs = int((len(list(combined_df))/2))

fig, axes = plt.subplots(number_of_csvs,1, sharex=False, figsize=(5,130))

# plot it all out
for i in range(number_of_csvs):
    axes[i].set_title(list(combined_df)[2*i-1])
    axes[i].plot(combined_df.iloc[:, [2*i-2]], combined_df.iloc[:, [2*i-1]])
    axes[i].set_xlabel(r"Lateral (mm)")
    axes[i].set_ylabel(r"Vertical (nm)")


plt.show()



#%%
import pandas as pd
import numpy as np
import scipy as sp
import plotly
plotly.offline.init_notebook_mode()
import plotly.offline as py
import plotly.figure_factory as ff
from plotly.graph_objs import *

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/school_earnings.csv")
table = ff.create_table(df)

data = [Bar(x=df.School,
            y=df.Gap)]
py.iplot(data, filename='jupyter/basic_bar')