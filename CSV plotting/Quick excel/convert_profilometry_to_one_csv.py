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

# specify layout REF:  https://plot.ly/python/reference/#layout
layout = dict(
                # title = 'Styled Scatter',
                # global font control
                font=dict(
                    family='Arial, sans-serif',
                    size=20,
                    color='black'
                ),

                xaxis = dict(
                    title = 'x_title',
                    # range
                    range=[0, 10],
                    #autorange=True,
                    # ticks
                    tickmode='linear',
                    dtick=5,
                    #tickmode='auto',
                    ticks="inside",
                    tickwidth=2,
                    tickfont=dict(
                    family='Arial, sans-serif',
                    size=14,
                    color='black'
                    ),
                    # mirror the axis and ticks on the top
                    mirror="ticks",
                    zeroline = False,
                    showline=True,
                    showgrid=False, 
                    linewidth=2,
                    zerolinewidth=5,
                    ),
                
                xaxis = dict(
                    title = 'x_title',
                    # range
                    range=[0, 10],
                    #autorange=True,
                    # ticks
                    tickmode='linear',
                    dtick=5,
                    #tickmode='auto',
                    ticks="inside",
                    tickwidth=2,
                    tickfont=dict(
                    family='Arial, sans-serif',
                    size=14,
                    color='black'
                    ),
                    # mirror the axis and ticks on the top
                    mirror="ticks",
                    zeroline = False,
                    showline=True,
                    showgrid=False, 
                    linewidth=2,
                    zerolinewidth=5,
                    ),

                # figure size
                height=600, 
                width=600,
                margin=go.Margin(
                    l=80,
                    r=50,
                    b=80,
                    t=80,
                    pad=0
                ),
                
                showlegend=False,
                legend = dict(
                    x=1,
                    y=1,
                    traceorder='normal',
                    font=dict(
                        family='Arial, sans-serif',
                        size=20,
                        #color='black'
                    ),
                    #
                    bgcolor='rgba(0,0,0,0)',
                    #bordercolor='black',
                    #borderwidth=0.5
                    ),
                )