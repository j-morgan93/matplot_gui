# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 09:51:00 2017

@author: jmorga14
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize
from scipy.interpolate import interp1d

sfile = "C:/Users/jmorga14/AnacondaProjects/matplot_gui-reading/simulated.out"
efile = "C:/Users/jmorga14/AnacondaProjects/matplot_gui-reading/experimental.out"
simfile =np.genfromtxt(sfile, comments='#', skip_header=3, names=True, unpack=True, autostrip=True)
expfile = np.genfromtxt(efile, comments='#', skip_header=3, names=True, unpack=True, autostrip=True)
# should replace "names" with the temperature values
sf = np.zeros(shape=(len(simfile),len(simfile.dtype.names)),dtype=float)
ef = expfile[expfile.dtype.names[1]] / max(expfile[expfile.dtype.names[1]])
names = list(simfile.dtype.names)
maxsim = np.zeros(shape=(len(simfile.dtype.names),1),dtype=float)

for i in range(1,len(simfile.dtype.names[1:])+1):
    maxsim[i] = max(simfile[simfile.dtype.names[i]])
    sf[:,i] = simfile[simfile.dtype.names[i]] / maxsim[i]
    names[i] = str(i)
    
def obj(i):  
    d = sum(abs(ef-sf[:,i])*pow(ef, 3))
    return d

deltas = np.zeros(shape=(len(simfile.dtype.names[1:]),1),dtype=float)

for i in range(len(deltas)):
    deltas[i] =obj(i+1)

deltas = np.asarray(deltas).squeeze()
xp  = np.linspace(1,len(simfile.dtype.names[1:]),num=len(simfile.dtype.names[1:]))
real_obj = interp1d(xp, deltas, kind='cubic')

def realguy(i):
    print(i)
    print(real_obj(i))
    print(2700+i*10)
    return real_obj(i)

x0=4

sol = minimize(realguy,x0,method='Nelder-Mead',options={'disp': True, 'maxiter':100}, tol=1e-6)

xnew = np.linspace(1,19,num=100)

plt.plot(xp,deltas,'o',xnew,real_obj(xnew),'--')
plt.legend(['tabulated','interpolated'],loc='best')
plt.show()