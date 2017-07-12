# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 14:50:09 2017

@author: jmorga14
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 09:51:00 2017

@author: jmorga14
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize
from scipy.interpolate import interp2d
from scipy.interpolate import Rbf
from scipy.interpolate import griddata

sfile = "C:/Users/jmorga14/AnacondaProjects/matplot_gui-reading/temp_nrho.out"
efile = "C:/Users/jmorga14/AnacondaProjects/matplot_gui-reading/exp_temp_nrho.out"
simfile =np.genfromtxt(sfile, comments='#', skip_header=3, names=True, unpack=True, autostrip=True)
expfile = np.genfromtxt(efile, comments='#', skip_header=3, names=True, unpack=True, autostrip=True)
# should replace "names" with the temperature values
sf = np.zeros(shape=(int(len(simfile.dtype.names[1:]) / 5), 5, len(simfile),), dtype=float)
ef = expfile[expfile.dtype.names[1]] / max(expfile[expfile.dtype.names[1]])
names = list(simfile.dtype.names)
maxsim = np.zeros(shape=(int(len(simfile.dtype.names[1:]) / 5), 5), dtype=float)

count = 0
for i in range(int(len(simfile.dtype.names[1:]) / 5)):
    for j in range(5):
        maxsim[i, j] = max(simfile[simfile.dtype.names[i*5+j]])
        sf[i, j, :] = simfile[simfile.dtype.names[i*5+j]] / maxsim[i, j]
        count += 1
    
def obj(i, j):  
    d = sum(abs(ef-sf[i, j, :])*pow(ef, 2))
    return d

deltas = np.zeros(shape=(20, 5), dtype=float)
points = np.zeros(shape=(100, 2), dtype=float)
nrho = np.linspace(1, 5, 5)
temp = np.linspace(1, 20, 20)
count = 0

for i in range(int(len(simfile.dtype.names[1:]) / 5)):
    for j in range(5):
        for k in range(2):
            if k == 0:
                points[count, k] = temp[i]
            if k == 1:
                points[count, k] = nrho[j]
            deltas[i,j] = obj(i, j)
        count += 1

grid_x, grid_y = np.mgrid[1:5:.05, 2400:3350:1]

deltas = np.asarray(deltas).squeeze()

data_interp = interp2d(temp , nrho, deltas.T, kind='linear')

def realguy(x):
    i = x[0]
    j = x[1]
    print("I :", i)
    print(" J:", j)
    print(data_interp(i, j))
    return data_interp(i, j)

x0 = [6,4]

sol = minimize(realguy,x0,method='Nelder-Mead',options={'disp': True, 'maxiter':100}, tol=1e-6)
