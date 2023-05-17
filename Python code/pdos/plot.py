import numpy as np
import matplotlib.pyplot as plt
import sys, os
from scipy.signal import find_peaks

isExist = os.path.exists('results')
if not isExist:

   # Create a new directory because it does not exist
   os.makedirs('results')
plt.style.use('fast')

cc = ['fcc','hcp']
ll = ['2','3','4']

for c_class in cc:
   for layer in ll:
      dirs = '/home/theoretical_catalysis/kabelkim/Desktop/masterproject/HCP_vs_FCC/pdos_real/' + c_class + '/' + layer + '_layers/pdos/Zone' + layer + '_'

      elements = ['au','pt'with open(dirs1+'/'+name, 'r') as fp:,'ir','os','re','w']
      count = 0

      peaks, _ = find_peaks(np.loadtxt(dirs + elements[1] + "_dos.txt"), height=100)
      off_sets = np.loadtxt(dirs+ elements[1] + "_e.txt")[peaks[-1]]

      plt.figure(figsize=(10, 6), dpi=300)
      for i in elements:
          count +=50
          d = np.loadtxt(dirs + i + "_dos.txt")
          e = np.loadtxt(dirs + i + "_e.txt")
          plt.plot(e-off_sets,d-count,label=str.title(i), lw=2)
          plt.xlim(-10,4)
          plt.ylim(-320,100)
      plt.ylabel('pDOS [arb.]')
      plt.xlabel(r'$E-E_f $ [eV]')
      plt.axvline(x=0,c="k", ls="--", alpha=0.5)
      plt.legend(loc='upper right')
      plt.yticks(range(0))
      plt.tight_layout()
      plt.savefig('results/'+c_class+'zone'+layer+'.png')

      #Residual plots

      pt = np.loadtxt(dirs + elements[1] + "_dos.txt")
                      
      plt.figure(figsize=(10, 6), dpi=300)
      for n in elements:
          d = np.loadtxt(dirs + n + "_dos.txt")
          e = np.loadtxt(dirs + n + "_e.txt")
          plt.plot(e-off_sets,pt-d,label=str.title(n), lw=2)
          plt.xlim(-10,4)
          plt.ylim(-150,150)
      plt.ylabel('pDOS [arb.]')
      plt.xlabel(r'$E-E_f $ [eV]')
      plt.axvline(x=0,c="k", ls="--", alpha=0.5)
      plt.legend(loc='upper right')
      plt.yticks(range(0))
      plt.tight_layout()
      plt.savefig('results/residuals_'+c_class+'zone'+layer+'.png')

