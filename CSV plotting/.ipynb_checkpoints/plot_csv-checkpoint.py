class plot_csv():
    
    def __init__(self):
        pass


    def prepare_data_frames(self):
        self.data_frames = {}
        for i in self.csv_list:
            df = pd.read_csv(i, skiprows = self.csv_skip_rows, )
            self.data_frames[i] = df
            
        



    def plotly_plot_data(self):
        #color_palatte = ['red','orange','yellow','green','cyan','blue','purple']
        # create traces -- data points
        self.traces = {}
        
        for i in self.csv_list: 
            self.traces[i] = go.Scatter(
                x = self.data_frames[i].humidity, #x value
                y = self.data_frames[i].wavelength_matlab, #y value
                name = '{}'.format(i),
                mode = 'lines',
                #mode = 'lines+markers',
                #text='RH {}'.format(self.peak_data[sample_number]['humidity'][scan_number]), # hover text
                line = dict(
                    #dash = 'dash', 
                    shape='spline',
                    color = '',
                    ),
                 marker = dict(
                    size = 3,
                    #color = 'rgba(255, 0, 0, .8)',
                    line = dict(
                        width = 0, 
                        # outter rim of the marker,
                        #color = 'black',
                        ),
                    )
                )
        
        
        
        # modify layout with dict()
        layout = dict(
            #title = '',
            xaxis= dict( 
                #range = self.wavelength_lim, 
                title= 'Wavelength (nm)',
                titlefont=dict(size=30, family = 'Times New Roman'),
                ticklen= 0,
                tickfont=dict(size=20, family = 'Times New Roman'),
                showline=True,
                zeroline= True,                
                gridwidth= 1,
                showgrid=True,
                ),
            yaxis = dict(
                #range = self.intensity_lim,
                title = 'Intensity (A.U.)',
                titlefont=dict(size=30, family = 'Times New Roman'),
                ticklen= 0,
                tickfont=dict(size=20, family = 'Times New Roman'),
                showline = True,
                zeroline = True,
                showgrid = True,
                gridwidth= 1,
                ),
            showlegend = True,
            legend = dict(
                font=dict(size=22, family = 'Times New Roman'),
                #yanchor='middle',
                #xanchor='middle'),
                x = 0.85, y = 1,
                # a box for legend
                bgcolor='white',
                #bordercolor='black',
                borderwidth=2,
                ), 
            # transparent graph
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
            )

        
        # create data -- a list contains all the traces
        data = []
        for i in self.traces:
            data.append(self.traces[i])
        # create figure with data and layout
        fig = dict(data=data, layout=layout)
        # set export static image
        
        # generate the plot and save as svg
        a = py.iplot(fig,  filename='styled-scatter', 
                     #image='svg',
                    )



if __name__ == "__main__":
    # visualisation
    csv_plots = plot_csv()
    # initialise some parameters
    csv_plots.folder = r"D:\GDrive\Research\BIP\Humidity sensor project\data\20170421"
    csv_plots.csv_list = ['2.csv']
    csv_plots.csv_skip_rows = range(4) # skip first 3 lines
    csv_plots.prepare_data_frames()
    csv_plots.plotly_plot_data()
    
    
    # export data to scan.csv
    # spectrometer_result.export_data(spectrometer_result.folder + '\\' + 'scan.csv')
    
    
    