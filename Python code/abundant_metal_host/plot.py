import glob, os, re, sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib
from matplotlib import style
from scipy import stats


host = str(os.getcwdb()).split('/')[-1].split("'")[0].capitalize()

h2o = -12.249268
h2 = -6.627349

dirs1 = './txt'
elements = ['Ag','Au','Cu','Pt']


dirs1 = './txt'
df1 = pd.DataFrame(columns=[])
df2 = pd.DataFrame(columns=[])
a = []
e_s = []
e_a = []

for file in sorted(os.listdir(dirs1)):
    if file.split("_")[2] == 'ads.txt':
        with open(dirs1+'/'+file, 'r') as fp:
            a.append(file.split("_")[1])
            lines = fp.readlines()
            for line in open(dirs1+'/'+file):
                if line.find('Free energy:') != -1:
                    e_a.append(float(line.split()[-1]))
    if file.split("_")[2] == 'slab.txt':
        with open(dirs1+'/'+file, 'r') as fp:
            lines = fp.readlines()
            for line in open(dirs1+'/'+file):
                if line.find('Free energy:') != -1:
                    e_s.append(float(line.split()[-1]))
e = []
for i in range(len(e_a)):
    e.append(e_a[i] - e_s[i])
E = []
for i in e:
    E.append(i-e[a.index(host)])

a = np.array_split(a, 3)
e = np.array_split(E, 3)
c = ['r','g','b']
#Plot
fig = plt.figure(figsize=(8,6))
plt.style.use("seaborn-muted")
ax1 = fig.add_subplot(111)
ax1.axhline(0, c = 'k', label = "Pure host", alpha = 0.5)
ax1.grid(alpha=0.4, ls="--")
for i in range(3):
    ax1.plot(a[i],e[i],color = c[i], label="Layer " + str(i+1))
    ax1.scatter(a[i],e[i], color = c[i])
ax1.set_title("Host: " + str(host))
ax1.set_ylabel(r'Adsorption Energy (eV) $(E_{ads} - E_{slab}) - E_{host}$')
ax1.set_xlabel("Adsorbate")
ax1.set_ylim(-0.6,1.1)
plt.tight_layout()
ax1.legend()
plt.savefig(str(host)+".png")

