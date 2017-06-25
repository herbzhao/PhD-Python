# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 16:55:52 2016

@author: Bonan
"""

"""
Python script for plotting and simulate 1-D defect structure. e.g. get sepctrum 
along a line
"""
import tm4.simClasses as sim
from tm4.linearDefect import CrossSection
import matplotlib.pyplot as pl
import numpy as np
from time import clock
import time
import tm4.matTools as mt
import matplotlib.gridspec as gridspec
pl.rcParams['figure.figsize'] = (8,6)
pl.rcParams['savefig.dpi'] = 100
#%%
#define materials
CNC = sim.UniaxialMaterial(1.586,1.524) # this might not be right
air = sim.HomogeneousNondispersiveMaterial(1)
cellulose = sim.HomogeneousNondispersiveMaterial(1.55)
# Set the glass as a practical backend
glass = sim.HomogeneousNondispersiveMaterial(1.55)
front = sim.IsotropicHalfSpace(air)
airhalf= sim.IsotropicHalfSpace(air)
glasshalf = sim.IsotropicHalfSpace(glass)
s = sim.OptSystem()
s.setHalfSpaces(airhalf,glasshalf)
heli = sim.HeliCoidalStructure
h1 = heli(CNC, 150, 1000)
spacer = sim.HomogeneousStructure(CNC, 10)
airSpacer = sim.HomogeneousStructure(air,10)
glassSpacer = sim.HomogeneousStructure(glass,10)
s.setStructure([h1])
wlRange = np.linspace(350,850,50)
#%% Class def
class CrossSection2D(CrossSection):
    """A class represent a 2D CrossSection of the film"""
    # Define the subclass method of alignHelices       
    def alignHelices(self, pointIndex):
        """Align the helices"""
        end = 0
        for i, helix in enumerate(self.s.structures):
            if i > 0: helix.phyParas['aor'] = end
            #print(i,end)
            # Calculate the end angle, not the intrinstic anlge of rotation need to be added
            if i == 0:                
                end = - helix.phyParas['t'] / helix.phyParas['p'] * np.pi + helix.phyParas['aor']\
                    + pointIndex/len(self.t) * 2 * np.pi

#%% Plotting    
        
#%%
def f1(x):
    return 2500
    

    
def getSaveName():
    return "results\\" + time.strftime("%Y%m%d-%H%M%S")
    
    
if __name__ == '__main__':
    from report_Paras import figPath
    pitchesList1 = [[200,180],[200,180],[200,160],[180,200], [170,200], [160,200]]
    pitchesList2 = [[210,180],[210,170],[210,160],[180,210], [170,210], [160,210]]
    pitchesList3 = [[150,180],[180,150]]
    pitchesList4 = [[180,180]]
    nop = 20 #Number of points to sample along the defect
    for pitches in pitchesList4:
        wlRange = np.linspace(400,800,200)
        h1 = heli(CNC,pitches[0],1000) #The thickness doesn't matter here
        h2 = heli(CNC, pitches[1] ,1000)
        tmp = [h1,h2]
        #%% Set layer structure
        c = CrossSection2D(s, 5000,1000,2)
        c.setInterfaceFunction(f1,0)
        c.calcPixelConfig(nop)
        c.setLayerTemplate(tmp)
        c.setWlList(wlRange)
        #for i in range(4):c.
       #     res.append(c.getResultForPoint(i))
        #c.getResultForPoint(0)
        t = clock()
        # %%Calculation
        
        res = c.getSpectrum(wlRange,4)
        name = getSaveName() + '2Layer'
        #np.save(name, res)
        print(clock()-t)
        
        #res = np.load('results/20160505-1351142Layer.npy')
        # %% Plottign
        #%% Save plot of layer structure
        #%%Plotting the structure
        pl.rc('figure', figsize = (3.3,2.8))
        pl.rc('font', size = 8)
        pl.figure()
        x = c.p.T
        # Calculate the ys to be plot
        y = np.append(c.h, np.repeat([[c.d]], len(c.p), axis = 0), axis = 1)
        pl.plot(y, x,'x-')
        pl.plot(np.zeros(x.shape[0]), x, 'x-')
        pl.xlim(0, c.d+2000)
        pl.ylim((c.l, 0))
        pl.annotate('', (5000,500), (7000,500),
                    arrowprops=dict(facecolor='black', headwidth = 10, width = 1,headlength = 10))
        #pl.title('Pitch ='+ str([x.phyParas['p'] for x in c.tmp])
        #+ " incident from right")
        pl.xlabel('Height from bottom /nm')
        pl.ylabel('Distance /a.u.')
        pl.tight_layout(pad = 0.2)
        #pl.savefig(figPath+"LD2S.pdf")
        #%%Plotting Combined image £££££££
        fig = pl.figure()
        gs = gridspec.GridSpec(1, 2, width_ratios=[10,1])
        ax1 = pl.subplot(gs[0])
        ax2 = pl.subplot(gs[1])
        sPlot = ax1.imshow(res, cmap = 'viridis',aspect = 'auto', interpolation = 'none',
                  extent = [wlRange[0], wlRange[-1],  1000, 0])
        ax1.set_xlabel("Wavelength /nm")
        ax1.set_ylabel("Distance /a.u.")
        ax1.set_xticks(np.arange(400,801,100))
        pl.colorbar(sPlot, ax = ax1)
        resArray = np.array(res)
        spec = mt.specData(wlRange,resArray.T)
        RGB = spec.getRGBArray()
        ax2.imshow(RGB.reshape((nop,1,3)),aspect='auto', extent=[0,1,1000,0])
        ax2.set_title("RGB")
        ax2.set_xticks([])
        ax2.set_yticks([])
        pl.tight_layout(pad = 0.2)
        #pl.savefig(figPath+ "LD2SPEC.pdf")
        ####