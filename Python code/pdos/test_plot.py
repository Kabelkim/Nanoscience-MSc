import numpy as np
import matplotlib.pyplot as plt
import sys, os
from scipy.signal import find_peaks

dirs = '/home/theoretical_catalysis/kabelkim/Desktop/masterproject/HCP_vs_FCC/pdos_real/' + 'fcc' + '/' + '2' + '_layers/pdos'
pt_e = np.loadtxt(dirs+'/Zone2_pt_e.txt')
pt_dos = np.loadtxt(dirs+'/Zone2_pt_dos.txt')
pt_dos = pt_dos/np.max(pt_dos)

w_e = np.loadtxt(dirs+'/Zone2_w_e.txt')
w_dos = np.loadtxt(dirs+'/Zone2_w_dos.txt')
w_dos = w_dos/np.max(w_dos)

au_e = np.loadtxt(dirs+'/Zone2_au_e.txt')
au_dos = np.loadtxt(dirs+'/Zone2_au_dos.txt')
au_dos = au_dos/np.max(au_dos)


plt.plot(w_e, pt_dos-w_dos-1)
plt.plot(au_e, pt_dos-au_dos-1)
plt.xlim(-15,0)
plt.show()
