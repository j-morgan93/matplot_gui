# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 09:51:00 2017

@author: Jonathan Morgan

Scipy Simplex Optimization for NEQAIR Spectral Fitting
need scip_spec.py script and 4 arguments from GUI
1. Experimental Data
2. MaxIterations
3. MaxFunctionaEvals
4. Tolerance of Fit

Experimental data must also be loaded into GUI and normalized
The function will return two items: the value of the evaluated
objective function and a figure of the spectra to be plotted
on the GUI stack1UI figure-space.
"""

import time
import sys, getopt, os, subprocess
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize

def printerino(datafile, maxi, maxf, tol, spec):
   print("bingo bango")
   print(datafile)
   print(maxi)
   print(maxf)
   print(tol)
   print(spec)

def genLOSFile(self, temp, specnum, specnrho):
   name = "LOS_specfit.dat"
   print("Writing LOS out to: ", name)
   f = open(name, 'w')
   f.write("#15.0\n#\n\n")
   f.write("n        x        ntot        Tt")
   sum_nrho = 0
   for i in range(0, specnum):
      ind = specnrho[i, 0].currentIndex()
      f.write("        "+specnrho[i, 0].itemText(ind))
      sum_nrho += float(specnrho[i, 1].text())
   for j in range(0, specnum):
      f.write("\n"+str(j)+"        "+str(j*0.5)+"        "+str(sum_nrho)+"        "+str(temp))
      for k in range(0, specnum):
         f.write("        "+str(float(specnrho[k, 1].text())))
   return name

def folderMake(self):
   cwd = os.getcwd()
   if os.path.isdir(cwd+"/spectralfit") is True:
     print("spectralfit directory already exists")
     path = (cwd+"/spectralfit")
   else:
     print("creating spectralfit directory")
     subprocess.run(["mkdir","spectralfit"])
     path = (cwd+"/spectralfit")
   return path

def moveNEQAIRFiles(self):
   subprocess.run(["cp","LOS_specfit.dat","spectralfit/LOS.dat"])
   subprocess.run(["rm","spectralfit/intensity_scanned.out"])
   print("copied LOS file")
   subprocess.run(["cp","neqair.inp","spectralfit"])
   subprocess.run(["rm","spectralfit/neqair.out"])
   print("copied neqair.inp file")

def submitFile(self):
   cwd = os.getcwd()   
   os.chdir(cwd+"/spectralfit")
   subprocess.check_call(["qsub","run_neqair.pbs"])
   os.chdir("..")

def isIntensity(self):
   cwd = os.getcwd()
   if os.path.exists(cwd+"/spectralfit/intensity_scanned.out"):
     print("intensity_scanned done")
     return True
   else:
     print("intensity_scanned not there")
     return False

def isNEQAIROut(self):
   cwd = os.getcwd()
   if os.path.exists(cwd+"/spectralfit/neqair.out"):
     print("neqair.out done")
     return True
   else:
     print("neqair.out not there")
     return False

"""
def main(argv):
   datafile = ''
   maxiter = ''
   maxfunc = ''
   tol = ''
   try:
      opts, args = getopt.getopt(argv,"hd:i:f:t:",["data=","maxi=","maxf=","tol="])
   except getopt.GetoptError:
      print("specfit.py -d <inputfile> -i <maxiterations> -f <maxfunceval> -t <tolerance>")
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print("specfit.py -d <inputfile> -i <maxiterations> -f <maxfunceval> -t <tolerance>")
         sys.exit()
      elif opt in ("-d", "--data"):
         datafile = arg
      elif opt in ("-i", "--maxi"):
         maxiter = arg
      elif opt in ("-f", "--maxf"):
         maxfunc = arg
      elif opt in ("-t", "--tol"):
         tol = arg
   print("Input file is ", datafile)
   print("MaxIterations are ", maxiter)
   print("MaxFunctionEvals are", maxfunc)
   print("Tolerance is", tol)

if __name__ == "__main__":
   main(sys.argv[1:])
"""
def simplexerino(self):
     # os.chdir(os.getcwd()+"/spectralfit")
     print("i'm alive!!")    
     while os.path.exists(os.getcwd()+"/spectralfit/intensity_scanned.out") is False:
       time.sleep(5)   
     print("done!")
     os.chdir(os.getcwd()+"/spectralfit")
     sfile = "intensity_scanned.out"
     efile = self.exp_datafile
     simfile =np.genfromtxt(sfile, comments='#', skip_header=4, names=True, unpack=True, autostrip=True)
     expfile = np.genfromtxt(efile, comments='#', skip_header=4, names=True, unpack=True, autostrip=True)
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

# deltas = np.zeros(shape=(len(simfile.dtype.names[1:]),1),dtype=float)

for i in range(len(deltas)):
    deltas[i] =obj(i+1)

def realguy(i):
    print(i)
    print(real_obj(i))
    print(2700+i*10)
    return real_obj(i)

# x0 = np.zeros(shape=(self.los['SpecNum'.value()+1,1),dtype=float)  # this has to be the array of temperatures and number densities

# sol = minimize(realguy,x0,method='Nelder-Mead',options={'disp': True, 'maxiter':maxiter, 'maxfev':maxfunc}, tol= tol)

# xnew = np.linspace(1,19,num=100)

# plt.plot(xp,deltas,'o',xnew,real_obj(xnew),'--')
# plt.xlabel("Case #")
# plt.ylabel('Delta')
# plt.legend(['tabulated','interpolated'],loc='best')
# plt.show()
"""
