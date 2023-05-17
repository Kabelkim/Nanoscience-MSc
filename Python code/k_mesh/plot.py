import glob, os, re, sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib
from matplotlib import style
from scipy import stats

dirs1 = './txt'
df = pd.DataFrame(columns = [])
e = []
a_a = []
num = []
for file in sorted(os.listdir(dirs1)):
    with open(dirs1+'/'+file, 'r') as fp:
        lines = fp.readlines()
        for line in open(dirs1+'/'+file):
            if line.find('Free energy:') != -1:
                e.append(float(line.split()[-1]))
        if file.split("_")[3] == 'ads.txt':
                        a_a.append(file.split("_")[2])
                        num.append(file.split("_")[1])
ef = []
for i in np.arange(len(e),step=2):
    ef.append(e[i]-e[i+1])


df['a'] = a_a
df['ef']  = ef
df['num'] = num

a_r = ['Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn']
df.sort_values(by=['num'])
df1 = df.loc[:9]
df2 = df.loc[10:19]
df3 = df.loc[20:29]
df4 = df.loc[30:39]
               
df1.sort_values(by="a", key=lambda column: column.map(lambda e: a_r.index(e)), inplace=True)
df2.sort_values(by="a", key=lambda column: column.map(lambda e: a_r.index(e)), inplace=True)
df3.sort_values(by="a", key=lambda column: column.map(lambda e: a_r.index(e)), inplace=True)
df4.sort_values(by="a", key=lambda column: column.map(lambda e: a_r.index(e)), inplace=True)

e1 = df1['ef'].tolist()
e2 = df2['ef'].tolist()
e3 = df3['ef'].tolist()
e4 = df4['ef'].tolist()
a = df1['a'].tolist()

val = [3,4,5,6,7,8,9,10,11,12]

#Plot
fig = plt.figure(figsize=(16,8))
plt.style.use("seaborn-muted")
ax1 = fig.add_subplot(111)
for xc in range(len(e1)):
    ax1.axvline(x=xc, c="k", alpha=0.1, ls="--")
 
ax1.scatter(a,e1, alpha=0.8, c='b', label='k-points (2x2x1)')
#ax1.plot(a,e1,ls="solid", alpha=0.3,lw=2,c='b')

ax1.scatter(a,e2, alpha=0.8, c='g', label='k-points (3x3x1)')
#ax1.plot(a,e2,ls="solid", alpha=0.3,lw=2,c='g')

ax1.scatter(a,e3, alpha=0.8, c='r', label='k-points (4x4x1)')
#ax1.plot(a,e3,ls="solid", alpha=0.3,lw=2,c='r')

ax1.scatter(a,e4, alpha=0.8, c='k', label='k-points (8x8x1)')
#ax1.plot(a,e4,ls="solid", alpha=0.3,lw=2,c='k')

#ax1.set_xticks(a_s)
#ax1.set_xticklabels(a_s)
"""
ax2 = ax1.twiny()
ax2.scatter(a,e1, alpha=0)
ax2.set_xticks(a)
ax2.set_xticklabels(val)
"""
ax1.set_ylabel(r'$E_a - E_s$ [eV]')
ax1.set_xlabel("Guest elements")
#ax2.set_xlabel("Valence electrons")
ax1.legend(loc="upper right")
#ax1.set_title("K-Point dependence (Pt-based SAA)")

plt.tight_layout()
plt.savefig("figure_5.png")
plt.show()

