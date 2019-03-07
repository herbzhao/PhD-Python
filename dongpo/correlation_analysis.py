from __future__ import division
import pylab as pl
from matplotlib.ticker import MaxNLocator
from scipy.optimize import fmin_l_bfgs_b

from cylinderEnsemble import cylinderEnsemble
#from mmaClass import mmaClass  #This library is not publicly available
from termcolor import colored, cprint
from scipy.stats import norm

import os


def gaussPeak(ce,k0,phi0,sigmaK,sigmaPhi):
    tmp = ce.lphi-phi0
    tmp[tmp>pl.pi] = (tmp[tmp>pl.pi] - 2*pl.pi)
    tmp[tmp<-pl.pi] = (tmp[tmp<-pl.pi] + 2*pl.pi)
    Ktrans,Phitrans = pl.meshgrid(ce.lk-k0,tmp)

    return 1/(sigmaK*sigmaPhi*pl.sqrt(2*pl.pi))*pl.exp(-0.5 * ((Ktrans/sigmaK)**2+(Phitrans/sigmaPhi)**2))

def main(folder_name, file_name):
    klim = (1,200)
    bbox = (-10,10)
    Nphi = 101
    Nk = 101
    k0 = 2*pl.pi/(0.270)
    ce = cylinderEnsemble(klim,Nk,Nphi,bbox)
    ce.setUniformIntegrationPoints() #to have an isotropic SF

    sigmaK =   0.01
    sigmaPhi = 0.05/180*pl.pi

    
    f = open(folder_name + "\\"+ file_name)
    bac = []
    for line in f:
        bac += [ [float(elm) for elm in line.split()] + [0.05] ]
    lCyl = pl.array(bac)

    ce.updateCylinders(lCyl) #change for different radii
    ce.visualise(sameColour=True,show=False)
    Sref = sum([gaussPeak(ce,k0,(phi0+45)/180*pl.pi,sigmaK,sigmaPhi) for phi0 in [0,90,180,270]])
    Sref /= Sref.max()

    ce.polarPlot(clim=(0.001,0.003),show=False,colorbar=True) #,smooth=0.5)
    #ce.polarPlotS(Sref,clim=(1,1))
    pl.savefig(folder_name+"\\" + file_name +'.eps', bbox_inches='tight')
    pl.show()




if __name__ == "__main__":
    folder_name = r"D:\Dropbox\000 - Inverse opal balls\Correlation analysis\data"
    file_names = (os.listdir(folder_name))
    txt_file_names = [name.replace('.txt','') for name in file_names if '.txt' in name]
    for file_name in txt_file_names:
        main(folder_name, file_name)