import csv
import re

import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio

import pandas as pd


class read_spectrometer():
    ''' convert matlab.mat to csv for output spec'''
    def __init__(self):
        #regex for sample description classification. example file name: sample1-H20-T20-Nikon10x-001
        self.temperature_re = re.compile('T\d+.?\d*-')
        self.humidity_re = re.compile('H\d+.?\d*-')
        self.spot_number_re = re.compile('sample\d+-')
        # default humidity output is false
        self.output_humidity = False


    def save_matlab_spectra_to_csv(self):
        'this converts matlab data into np.ndarray '
        self.mat_scan_contents = sio.loadmat(self.folder +'\\'+ self.scan_filename)['scan']
        self.scan_result = {}
        
        table = {}
        table['wavelength'] = [i[0] for i in self.mat_scan_contents[0]['wl'][0]]


        for i in range(len(self.mat_scan_contents)):
            table[self.mat_scan_contents[i]['desc'][0][0]] = [i[0] for i in self.mat_scan_contents[i]['spec'][0]]
        
        # use panda to save the table into csv
        self.df = pd.DataFrame(table)
        head = ['wavelength'] + [i[0][0] for i in self.mat_scan_contents['desc']]
        self.df = self.df[head]
        self.df.to_csv(self.folder +'\\'+ self.output_filename + '.csv',  sep=',')
        print('saved to ' + self.folder +'\\'+ self.output_filename + '.csv')


    def save_matlab_peaks_to_csv(self):
        'save peak wavelength, peak width and name to another csv'
        self.mat_scan_contents = sio.loadmat(self.folder +'\\'+ self.scan_filename)['scan']
        table = {}
        table['desc'] = []
        table['desc'] = [i[0][0] for i in self.mat_scan_contents['desc']]
        
        if self.output_humidity is True:
            table['humidity'] = []
            for description in table['desc']:
                try:
                    humidity = self.humidity_re.search(description).group().replace('H','').replace('-','')
                except:
                    humidity = None
                table['humidity'].append(humidity)

        if self.output_temperature is True:
            table['temperature'] = []
            for description in table['desc']:
                try:
                    temperature = self.temperature_re.search(description).group().replace('T','').replace('-','')
                except:
                    temperature = None
                table['temperature'].append(temperature)
            

        for category in ['desc', 'peak_wavelength_matlab', 'peak_intensity_matlab', 'peak_width_matlab']:
            table[category] = []
            if category == 'desc':
                table[category] = [i[0][0] for i in self.mat_scan_contents[category]]
            else:
                table[category] = [i[0][0][0] for i in self.mat_scan_contents[category]]

        # use panda to save the table into csv
        self.df = pd.DataFrame(table)
        self.df.to_csv(self.folder +'\\'+ self.output_filename + '_peaks' + '.csv',  sep=',')
        print('saved to ' + self.folder +'\\'+ self.output_filename + '_peaks' + '.csv' )
        


peak_smoothing = True

if peak_smoothing == True:
    scan = read_spectrometer()
    scan.folder = r'V:\Group Publications & Reports\Papers & Manuscripts\Song - bottlebrush photonic balls\Final data for publication\Microscopy\2018_02_19 Bottlebrush films\20180219'

    # original spectra
    scan.scan_filename = 'scan_backup.mat'
    scan.output_filename = 'output_unsmoothed_spectra'
    scan.save_matlab_spectra_to_csv()

    # smoothed spectra for peak extraction
    scan.scan_filename = 'scan.mat'
    scan.output_filename = 'output_smoothed_spectra'
    scan.save_matlab_spectra_to_csv()
    # output humidity 
    scan.output_humidity = True
    scan.output_temperature = True
    scan.save_matlab_peaks_to_csv()



elif peak_smoothing == False:
    # for case without peak smoothing
    scan = read_spectrometer()
    scan.folder = r'C:\Users\herbz\Dropbox\BIP-dropbox\data\20180214\Green'

    # original spectra
    scan.scan_filename = 'scan.mat'
    scan.output_filename = 'output_unsmoothed_spectra'
    scan.save_matlab_spectra_to_csv()