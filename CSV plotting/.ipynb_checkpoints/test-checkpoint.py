    def plotly_spectrum(self):
        
        # marker colour
        colour_scale = cl.scales['8']['div']['Spectral']*3 #repeat 3 times 
        dash_scale = [None]*8+['dot']*8+['dash']*8  #'dash', 'dot', and 'dashdot'
        #colour_scale = ['red','orange','yellow','green','cyan','blue','purple']*5
        item_number = 0
        
        # create traces -- data points
        self.traces = {}
        # prepare datasets for plotly
        sample_number = '1' # fix this bug
        for scan_number in self.plot_scan_numbers:
            scan_number = scan_number - 1 #the scan number starts with 1 while python starts with 0
            self.traces[scan_number] = go.Scatter(
                x = self.formatted_scan_results[scan_number][0], #wavelength
                y = self.formatted_scan_results[scan_number][1], #intensity
                name = '{}% RH'.format(int(self.peak_data[sample_number]['humidity'][scan_number])),
                mode = 'lines',
                #text='RH {}'.format(self.peak_data[sample_number]['humidity'][scan_number]), # hover text
                line = dict(
                    shape='spline',
                    dash = dash_scale[item_number],
                    color= colour_scale[item_number],
                    ),
                 marker = dict(
                    )
                )
            # iterate item + 1 for each plot
            item_number += 1
            
        # modify layout with dict()
        layout = dict(
            #title = '',
            xaxis= dict( 
                range = self.wavelength_lim, 
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
                title = 'Intensity (A.U.)',
                titlefont=dict(size=30, family = 'Times New Roman'),
                ticklen= 0,
                tickfont=dict(size=20, family = 'Times New Roman'),
                showline = True,
                zeroline = True,
                showgrid = True,
                gridwidth= 1,
                range = self.intensity_lim),
            showlegend = True,
            legend = dict(
                    font=dict(size=20, family = 'Times New Roman'),
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
        for i in self.plot_scan_numbers: # this scan number start from 1 rather than 0
            data.append(self.traces[i-1])
        # create figure with data and layout
        fig = dict(data=data, layout=layout)
        # set export static image
        
        # generate the plot
        a = py.iplot(fig,  filename='styled-scatter', image='svg', image_width = 800, image_height = 500)



        