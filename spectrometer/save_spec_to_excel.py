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
        self.temperature_re = re.compile('T\d+.?\d*')
        self.humidity_re = re.compile('H\d+.?\d*-')
        self.spot_number_re = re.compile('sample\d+-')
        
        
    def convert_matlab_scan(self):
        'this converts matlab data into np.ndarray '
        self.mat_scan_contents = sio.loadmat(self.folder +'\\'+ self.scan_filename)['scan']
        self.scan_result = {}
        # catagorise scan result into spectrum, description and wavelength
        for i in ['spec', 'desc', 'wl']:
            self.scan_result[i] = self.mat_scan_contents[i]
        # total scan numbers
        self.total_scan_number = len(self.scan_result['wl'])
        
        
        def convert_struct_to_column(table, header, scan_header, scan_number):
            'a short function to add column to dict' 
            table[header] = []
            for i in self.scan_result[scan_header][scan_number][0]:
                table[header].append(float(i))
        
        table = {}
        convert_struct_to_column(table, 'wavelength', 'wl', scan_number = 0)
        for i in range(self.total_scan_number):
            # the description about sample temperature and humidity
            description = str(self.scan_result['desc'][i][0]).replace("[","").replace("]","").replace("\'","")
            convert_struct_to_column(table, description, 'spec', scan_number = i)
            
        self.df = pd.DataFrame(table)
        
        # rearrange the header
        header = self.df.columns.tolist()
        header = header[-1:] + header[:-1]
        self.df = self.df[header]
        
        #writer = pd.ExcelWriter(self.folder +'\\'+ 'output_smoothed_peaks.xlsx')
        self.df.to_csv(self.folder +'\\'+ self.output_filename,  sep=',')



    def convert_matlab_scan_2(self):
        'this converts matlab data into np.ndarray '
        self.mat_scan_contents = sio.loadmat(self.folder +'\\'+ self.scan_filename)['scan']
        self.scan_result = {}
        # catagorise scan result into spectrum, description and wavelength
        for i in ['spec', 'desc', 'wl']:
            self.scan_result[i] = self.mat_scan_contents[i]
        # total scan numbers
        self.total_scan_number = len(self.scan_result['wl'])
        
        table = {}
        # all the spectra share the same wavelength axis
        table['wavelength'] = []
        # convert numpy array into a list 
        list(map(lambda wavelength: table['wavelength'].append(float(wavelength)), self.scan_result['wl'][0][0]))

        # assign spectra intensity to sample description into columns
        for sample_number in range(len(self.scan_result['desc'])):
            table[self.scan_result['desc'][sample_number][0][0]] = []
            list(map(lambda intensity: table[self.scan_result['desc'][sample_number][0][0]].append(float(intensity)), self.scan_result['spec'][sample_number][0]))
        
        self.df = pd.DataFrame(table)
        
        # reverse the header order
        header = self.df.columns.tolist()[::-1]
        self.df = self.df[header]
        self.df.to_csv(self.folder +'\\'+ self.output_filename,  sep=',')
    



scan = read_spectrometer()
scan.folder = r'D:\GDrive\Research\BIP\Humidity sensor project\data\20170810 - temper'
scan.scan_filename = 'smoothed_peaks.mat'
scan.output_filename = 'output_smoothed_peaks.csv'
scan.convert_matlab_scan_2()