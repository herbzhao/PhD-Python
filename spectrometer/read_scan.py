import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio
from scipy import signal

import peakutils


class read_spectrometer():
    def __init__(self):
        self.fig = plt.figure(figsize=(12,4), dpi=200)
        self.scan_result = {}
        self.formatted_scan_results = {}
        self.sample_description = []
        self.background_substracted_scan_results = {}
        self.peak_wavelength = {}
        self.peak_intensity = {}
        
        #settings
        self.wavelength_xlim = (300,800)
        self.spec_ylim = (0,1.1)

        # run functions
        self.convert_matlab_scan()
        self.format_result()
        self.find_peaks()
        self.remove_background(background_sample_number = 0)


    def convert_matlab_scan(self):
        'this converts matlab data into np.ndarray '
        self.mat_scan_contents = sio.loadmat('scan.mat')['scan']
        self.scan_result = {}
        for i in ['spec', 'desc', 'wl']:
            self.scan_result[i] = self.mat_scan_contents[i]

        self.total_sample_number = len(self.scan_result['wl'])

    def read_result(self, feature, sample_number): 
        'For quick reading of results, returns full datapoints of wavelength, spec, etc'
        
        all_datapoints = self.scan_result[feature][sample_number][0]
        #print(all_datapoints)
        # read value at certain datapoint
        #data_point = 100
        #print(all_datapoints[data_point])
        return all_datapoints

    def format_result(self):
        'convert all the information about one sample into a 2d array '
        for sample_number in range(self.total_sample_number):
            wavelength_data = self.read_result(feature = 'wl', sample_number = sample_number)
            spectrometer_data = self.read_result(feature = 'spec', sample_number = sample_number)
            description = self.read_result(feature = 'desc', sample_number = sample_number)
            # form a 2d array with wavelength and spec data
            self.formatted_scan_results[sample_number] = np.vstack((
                np.transpose(wavelength_data), 
                np.transpose(spectrometer_data)))
            self.sample_description.append(description)

        #print(self.formatted_scan_results[3])

    def remove_background(self, background_sample_number = 0):
        'substract background on non-sample area'
        # the sample_number of background spectrometer you want to remove
        background_spectrum = self.formatted_scan_results[background_sample_number][1] # [1] is the spec
        for sample_number in range(self.total_sample_number):
            self.background_substracted_scan_results[sample_number] = np.vstack(
                (self.formatted_scan_results[sample_number][0],
                self.formatted_scan_results[sample_number][1] - background_spectrum)
            ) 

    def find_peaks(self):
        'find peak using scipy'
        for sample_number in range(self.total_sample_number):
            peak_data_point = signal.find_peaks_cwt(
                self.formatted_scan_results[sample_number][1], 
                np.arange(50,150))
            peak_wavelengths = self.formatted_scan_results[sample_number][0][peak_data_point]
            for peak_wavelength in peak_wavelengths:
                if peak_wavelength > 300 and peak_wavelength < 800:
                    self.peak_wavelength[sample_number] = peak_wavelength
                    self.peak_intensity[sample_number] = self.formatted_scan_results[sample_number][1][peak_data_point]


    def find_peaks_2(self):
        'find peak using peakutils'
        for sample_number in range(self.total_sample_number):
            peak_data_point = peakutils.indexes(
                self.formatted_scan_results[sample_number][1], 
                thres=0.1, min_dist=10)
            peak_wavelengths = self.formatted_scan_results[sample_number][0][peak_data_point]
            for peak_wavelength in peak_wavelengths:
                if peak_wavelength > 300 and peak_wavelength < 800:
                    self.peak_2[sample_number] = peak_wavelength

    def plot_spectrum(self, sample_number):
        'plot spectra with given sample number, show peaks'
        ax = plt.subplot(211)
        sample_number = sample_number -1 # convert sample number to start from 0
        ax.plot(
            self.formatted_scan_results[sample_number][0],
            self.formatted_scan_results[sample_number][1], 
            label='sample: {}\n{}'.format(sample_number + 1, self.sample_description[sample_number]))
        if self.background_substraction is True:
            ax.plot(
                self.background_substracted_scan_results[sample_number][0],
                self.background_substracted_scan_results[sample_number][1], 
                label='bg_removed_sample: {}\n{}'.format(
                    sample_number + 1, self.sample_description[sample_number]))        
        
        if self.show_peaks is True:
            ax.plot((self.peak_wavelength[sample_number],self.peak_wavelength[sample_number]),(0,1.1), label = 'scipy peaks')
            print(self.peak_wavelength[sample_number])
            print(self.peak_intensity[sample_number])


        # set range etc
        ax.set_xlim(self.wavelength_xlim)
        ax.set_ylim(self.spec_ylim)
        lines, labels = ax.get_legend_handles_labels()
        ax.legend(
            lines, labels,
            scatterpoints=1, fancybox=True, shadow=True, ncol=1,
            fontsize=12, loc=1, bbox_to_anchor=(1.1,1))

    def plot_peaks(self):
        ax2 = plt.subplot(221)
        for sample_number in range(self.total_sample_number):
            ax2.scatter(self.peak_wavelength[sample_number], self.peak_intensity[sample_number])
        

if __name__ == "__main__":
# visualisation
    spectrometer_result = read_spectrometer()
    spectrometer_result.background_substraction = True
    spectrometer_result.show_peaks = True
    spectrometer_result.plot_spectrum(30)
    #spectrometer_result.plot_peaks()
    plt.show()
