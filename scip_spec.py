# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 09:51:00 2017

@author: jmorga14
"""

import numpy as np
from scipy.optimize import minimize

sfile = "C:/Users/jmorga14/AnacondaProjects/matplot_gui-reading/simulated.out"
efile = "C:/Users/jmorga14/AnacondaProjects/matplot_gui-reading/experimental.out"
simfile =np.genfromtxt(sfile, comments='#', skip_header=3, names=True, unpack=True, autostrip=True)
expfile = np.genfromtxt(efile,comments='(',skip_header=1,names=True,unpack=True,autostrip=True, dtype=float)
   
sf = np.zeros(shape=(len(simfile),len(simfile.dtype.names)),dtype=float)
# ef = np.zeros(shape=(len(simfile),len(simfile.dtype.names)),dtype=float))
ef = expfile[expfile.dtype.names[1]]

for i in range(len(simfile.dtype.names)):
    sf[:,i] = simfile[simfile.dtype.names[i]]

def obj(i):
    print("PICKLED IS ",i)

    i = int(i+i/2)
    print("CHANGED IS ",i)

    pf= sf[:,i]
    return sum(abs(ef-pf)*pow(ef,2))

x0=10
sol = minimize(obj,x0,method='Nelder-Mead',options={'disp': True,'maxiter':100}, tol=1e-3)