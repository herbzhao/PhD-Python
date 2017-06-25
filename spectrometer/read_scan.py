import csv
import re

import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio

from scipy import signal
import peakutils


class read_spectrometer():
    def __init__(self):

        #regex for sample description classification. example file name: sample1-H20-T20-Nikon10x-001
        self.temperature_re = re.compile('T\d+.?\d*')
        self.humidity_re = re.compile('H\d+.?\d*-')
        self.spot_number_re = re.compile('sample\d+-')

        #plotting settings
        self.fig = plt.figure(figsize=(12,4), dpi=200)
        self.intensity_lim = (0,1.1) # range of normalised intensity
        self.humidity_lim = (0,100) # range of RH
        self.plot_colour = ['r','g','b','y','k'] # colour scheme for multiple samples

        
    def initialise_methods(self):
        ' initialise class methods '
        self.convert_matlab_scan()
        self.format_result()
        self.remove_background(background_scan_number = 0)
        self.format_description()
        self.find_peaks(find_peak_method = 'scipy')
        self.format_peak_data()

        
    def convert_matlab_scan(self):
        'this converts matlab data into np.ndarray '
        self.mat_scan_contents = sio.loadmat(self.folder +'\\'+ 'scan.mat')['scan']
        self.scan_result = {}
        # catagorise scan result into spectrum, description and wavelength
        for i in ['spec', 'desc', 'wl']:
            self.scan_result[i] = self.mat_scan_contents[i]
        # total scan numbers
        self.total_scan_number = len(self.scan_result['wl'])
    
    def read_result(self, feature, scan_number): 
        '''Return all datapoints with certain features of certain scan

        #print(all_datapoints)
        # read value at certain datapoint
        #data_point = 100
        #print(all_datapoints[data_point])'''

        all_datapoints = self.scan_result[feature][scan_number][0]

        return all_datapoints

    def format_result(self):
        'convert all the information about one sample into a 2d array '
        self.formatted_scan_results = {}
        self.description = {}
        for scan_number in range(self.total_scan_number):
            wavelength_data = self.read_result(feature = 'wl', scan_number = scan_number)
            intensity_data = self.read_result(feature = 'spec', scan_number = scan_number)
            description = self.read_result(feature = 'desc', scan_number = scan_number)
            # form a 2d array with wavelength and spec data
            self.formatted_scan_results[scan_number] = np.vstack((
                np.transpose(wavelength_data), 
                np.transpose(intensity_data)))
            self.description[scan_number] = description
        
    def remove_background(self, background_scan_number = 0):
        'substract background on non-sample area'
        self.background_substracted_scan_results = {}
        # the sample_number of background spectrometer you want to remove
        background_intensity = self.formatted_scan_results[background_scan_number][1] # [1] is the spec
        for scan_number in range(self.total_scan_number):
            self.background_substracted_scan_results[scan_number] = np.vstack(
                (self.formatted_scan_results[scan_number][0],
                self.formatted_scan_results[scan_number][1] - background_intensity)) 
   
    def format_description(self):
        'Use regex to format the description. Exporting sample number, temperature, and humidity'
        self.temperature = {}
        self.humidity = {}
        self.sample_numbers = {}
        for scan_number in range(self.total_scan_number):
            description = self.description[scan_number][0] # convert list to string
            temperature = self.temperature_re.findall(description)
            humidity = self.humidity_re.findall(description)
            sample_number = self.spot_number_re.findall(description)

            try:
                temperature = temperature[0].replace('T','').replace('-','')
            except IndexError: 
                temperature = '' # if the data is empty, set it to ''
            try:
                humidity = humidity[0].replace('H','').replace('-','')
            except IndexError:
                humidity = '' # if the data is empty, set it to ''
            try:
                # for desc with same sample_number, add them to a list
                sample_number = sample_number[0].replace('sample','').replace('-','')
                if sample_number not in self.sample_numbers:
                    self.sample_numbers[sample_number] = []
                self.sample_numbers[sample_number].append(scan_number)
            except IndexError:
                pass

            self.temperature[scan_number] = temperature
            self.humidity[scan_number] = humidity

        # override the self.sample_numbers
        #self.sample_numbers[0] = range(1,20)
        #self.sample_numbers[1] = (18,29)
        #print(self.formatted_scan_results[3])

    def find_peaks(self, find_peak_method):
        'find peak using scipy'
        self.peak_wavelength = {}
        self.peak_intensity = {}
        if find_peak_method == 'scipy':
            for scan_number in range(self.total_scan_number):
                # for each scan, find peaks
                peak_data_points = signal.find_peaks_cwt(
                    self.formatted_scan_results[scan_number][1], np.arange(50,150))
                for peak_data_point in peak_data_points:
                    'filter out the peak thats not in our interested wavelength'
                    # convert datapoint into wavelength
                    peak_wavelength = float(self.formatted_scan_results[scan_number][0][peak_data_point])
                    if peak_wavelength > self.wavelength_lim[0] and peak_wavelength < self.wavelength_lim[1]:
                        self.peak_wavelength[scan_number] = peak_wavelength
                        self.peak_intensity[scan_number] = self.formatted_scan_results[scan_number][1][peak_data_point]
                        break

        elif find_peak_method == 'peakutils':
            for scan_number in range(self.total_scan_number):
                # for each scan, find peaks
                peak_data_points = peakutils.indexes(self.formatted_scan_results[scan_number][1], thres=0.5/max(self.formatted_scan_results[scan_number][1]), min_dist=100)
                #peak_data_points = peakutils.interpolate((range(0, len(self.formatted_scan_results[scan_number][1]))), self.formatted_scan_results[scan_number][1])
                for peak_data_point in peak_data_points:
                    'filter out the peak thats not in our interested wavelength'
                    # convert datapoint into wavelength
                    peak_wavelength = float(self.formatted_scan_results[scan_number][0][peak_data_point])
                    if peak_wavelength > self.wavelength_lim[0] and peak_wavelength < self.wavelength_lim[1]:
                        self.peak_wavelength[scan_number] = peak_wavelength
                        self.peak_intensity[scan_number] = self.formatted_scan_results[scan_number][1][peak_data_point]


    def format_peak_data(self):
        self.peak_data = {}
        for sample_number in self.sample_numbers.keys():
            self.peak_data[sample_number] = {}
            for i in ['humidity', 'temperature', 'peak_wavelength', 'peak_intensity']:
                self.peak_data[sample_number][i] = []
            for scan_number in self.sample_numbers[sample_number]:
                self.peak_data[sample_number]['humidity'].append(float(self.humidity[scan_number]))
                self.peak_data[sample_number]['temperature'].append(float(self.temperature[scan_number]))
                self.peak_data[sample_number]['peak_wavelength'].append(self.peak_wavelength[scan_number])
                self.peak_data[sample_number]['peak_intensity'].append(self.peak_intensity[scan_number])


    def plot_spectrum(self, scan_number):
        'plot spectra with given sample number, optionally show peaks'
        ax = plt.subplot(211)
        scan_number = scan_number -1 # convert scan number to python numbering system (start from 0)
        if scan_number > self.total_scan_number:
            scan_number = self.total_scan_number - 1
        ax.plot(
            self.formatted_scan_results[scan_number][0], #wavelength
            self.formatted_scan_results[scan_number][1], #intensity
            label='sample: {}\n{}'.format(scan_number + 1, self.description[scan_number]))
        if self.background_substraction is True:
            ax.plot(
                self.background_substracted_scan_results[scan_number][0], #wavelength
                self.background_substracted_scan_results[scan_number][1], #intensity
                label='bg_removed_sample: {}\n{}'.format(
                    scan_number + 1, self.description[scan_number]))        
        
        if self.show_peaks is True:
            ax.plot(
                (self.peak_wavelength[scan_number],self.peak_wavelength[scan_number]),
                self.intensity_lim,
                label = 'scipy peaks')

        # set range etc
        ax.set_xlim(self.wavelength_lim)
        ax.set_ylim(self.intensity_lim)
        lines, labels = ax.get_legend_handles_labels()
        ax.legend(
            lines, labels,
            scatterpoints=1, fancybox=True, shadow=True, ncol=1,
            fontsize=12, loc=1, bbox_to_anchor=(1.1,1))

    def plot_humidity_vs_peaks(self):
        'plot wavelength change with humidity'
        ax2 = plt.subplot(212)
        for sample_number in self.sample_numbers:
            ax2.scatter(
                self.peak_data[sample_number]['humidity'],
                self.peak_data[sample_number]['peak_wavelength'],
                c = self.plot_colour[int(sample_number)],
                label = 'spot{}'.format(sample_number))

        # set range etc
        ax2.set_xlim(self.humidity_lim)
        ax2.set_ylim(self.wavelength_lim)
        ax2.legend(
            scatterpoints=1, fancybox=True, shadow=True, ncol=1,
            fontsize=12, loc=1, bbox_to_anchor=(1.1,1))


    def export_data(self, filename):
        'Export data to a csv sheet'
        with open(filename, 'w', newline="") as csvfile:
            csv_writer = csv.writer(csvfile, dialect = 'excel')
            csv_writer.writerow(['scan number','sample description','temperature','humidity','wavelength','intensity'])
            for scan_number in range(self.total_scan_number):
                csv_writer.writerow(
                    ['{}'.format(scan_number + 1) ,
                    '{}'.format(self.description[scan_number]),
                    '{}'.format(self.temperature[scan_number]),
                    '{}'.format(self.humidity[scan_number]),
                    '{}'.format(self.peak_wavelength[scan_number]),
                    '{}'.format(self.peak_intensity[scan_number])])

if __name__ == "__main__":
# visualisation
    spectrometer_result = read_spectrometer()
    # initialise some parameters
    spectrometer_result.folder = r"D:\GDrive\Research\BIP\Humidity sensor project\data\20170421"
    spectrometer_result.background_substraction = False # secondary background substraction
    spectrometer_result.show_peaks = True # draw a line at peak positions
    spectrometer_result.wavelength_lim = (400,700) # range of wavelength to plot
    
    spectrometer_result.initialise_methods()
    # plot individual scan
    spectrometer_result.plot_spectrum(1)
    # plot peak wavelength change with relative humidity
    spectrometer_result.plot_humidity_vs_peaks()
    # export data to scan.csv
    spectrometer_result.export_data(spectrometer_result.folder + '\\' + 'scan.csv')
    # show matplotlib figure
    plt.show()
