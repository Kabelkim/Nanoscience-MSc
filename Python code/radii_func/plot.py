import glob, os, re, sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib
from matplotlib import style
from scipy import stats

atom = 'Pt'
val = 10
an = -3

cl = ["red","blue","green"]
h2o = -12.249268
h2 = -6.627349  
elements = ['Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn','Y','Zr','Nb','Mo','Ru','Rh','Pd','Ag','Cd','Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg']
atomic_radii = [184, 176, 171, 166, 161, 156, 152, 149, 145, 142, 212, 206, 198, 190, 178, 173, 169, 165, 161, 208, 200, 193, 188, 185, 180, 177, 174, 171]
ar = []
for i in atomic_radii:
    temp = str(i)
    ar.append(int(temp))
    ar.append(int(temp))
    ar.append(int(temp))


df1 = pd.DataFrame(columns=[])
df2 = pd.DataFrame(columns=[])
a_a = []
a_s = []
e_s = []
e_a = []
l_s = []
l_a = []

for file in os.listdir('./txt'):
    if file.split("_")[3] == 'ads.txt':
        with open('./txt'+'/'+file, 'r') as fp:
            a_a.append(file.split("_")[2])
            l_a.append(file.split("_")[1])
            lines = fp.readlines()
            for line in open('./txt'+'/'+file):
                if line.find('Free energy:') != -1:
                    e_a.append(float(line.split()[-1]))
    if file.split("_")[3] == 'slab.txt':
        with open('./txt'+'/'+file, 'r') as fp:
            l_s.append(file.split("_")[1])
            a_s.append(file.split("_")[2])
            lines = fp.readlines()
            for line in open('./txt'+'/'+file):
                if line.find('Free energy:') != -1:
                    e_s.append(float(line.split()[-1]))
df1['a'] = a_s
df1['e'] = e_s
df1['l'] = l_s

df2['a'] = a_a
df2['e'] = e_a
df2['l'] = l_a
df2.sort_values(by='l')
df1.sort_values(by="a", key=lambda column: column.map(lambda e: elements.index(e)), inplace=True)
df2.sort_values(by="a", key=lambda column: column.map(lambda e: elements.index(e)), inplace=True)

#df1['r'] = ar
#df2['r'] = ar

e_s1 = df1.loc[df1['l'] == "1", 'e'].tolist()
e_a1 = df2.loc[df2['l'] == "1", 'e'].tolist()
a1 = df1.loc[df1['l'] == "1", 'a'].tolist()

host = e_a1[an]+0.5*h2-e_s1[an]-h2o

e1 = []
for i in range(len(e_s1)):
        e1.append((e_a1[i]+0.5*h2-e_s1[i]-h2o)-host)
        
e_s2 = df1.loc[df1['l'] == "2", 'e'].tolist()
e_a2 = df2.loc[df2['l'] == "2", 'e'].tolist()
a2 = df1.loc[df1['l'] == "2", 'a'].tolist()

e2 = []
for i in range(len(e_s2)):
    e2.append((e_a2[i]+0.5*h2-e_s2[i]-h2o)-host)

e_s3 = df1.loc[df1['l'] == "3", 'e'].tolist()
e_a3 = df2.loc[df2['l'] == "3", 'e'].tolist()
a3 = df1.loc[df1['l'] == "3", 'a'].tolist()

e3 = []
for i in range(len(e_s3)):
    e3.append((e_a3[i]+0.5*h2-e_s3[i]-h2o)-host)
"""
df3 = pd.DataFrame(columns=[])
df3['e'] = e1
df3['a'] = a1
df3['r'] = atomic_radii
df3 = df3.sort_values(by='r')
E1 = df3['e'].tolist()
A1 = df3['a'].tolist()
R1 = df3['r'].tolist()

df4 = pd.DataFrame(columns=[])
df4['e'] = e2
df4['a'] = a2
df4['r'] = atomic_radii
df4 = df4.sort_values(by='r')
E2 = df4['e'].tolist()
A2 = df4['a'].tolist()
R2 = df4['r'].tolist()

df5 = pd.DataFrame(columns=[])
df5['e'] = e3
df5['a'] = a3
df5['r'] = atomic_radii
df5 = df5.sort_values(by='r')
E3 = df5['e'].tolist()
A3 = df5['a'].tolist()
R3 = df5['r'].tolist()

df5 = pd.DataFrame(columns=[])
df5['e'] = e3
df5['a'] = a3
df5['r'] = atomic_radii
df5 = df5.sort_values(by='e')

E3 = df5['e'].tolist()
A3 = df5['a'].tolist()
R = df5['r'].tolist()

df4 = pd.DataFrame(columns=[])
df4['e'] = e2
df4['a'] = a2
df4.sort_values(by="a", key=lambda column: column.map(lambda e: A3.index(e)), inplace=True)
E2 = df4['e'].tolist()
A2 = df4['a'].tolist()




df3 = pd.DataFrame(columns=[])
df3['e'] = e1
df3['a'] = a1

df3.sort_values(by="a", key=lambda column: column.map(lambda e: A2.index(e)), inplace=True)
E1 = df3['e'].tolist()
A1 = df3['a'].tolist()
"""

#plot
val_l = [10+val, 11+val, 12+val, 13+val,14+val, 15+val,16+val,17+val,18+val,19+val,10+val,11+val,12+val,13+val,15+val,16+val,17+val,18+val,19+val,11+val,12+val,13+val,14+val,15+val,16+val,17+val,18+val,19+val]
fig = plt.figure(figsize=(16,8))
ax1 = fig.add_subplot(111)
plt.style.use("seaborn-muted")
ax1.grid(alpha=0.4, ls="--")
ax1.axhline(0, color = 'k', lw = 1, alpha = 0.6, label = "Pure host")


ax1.scatter(a1,e1, color = cl[0])
ax1.plot(a1,e1, color = cl[0], alpha = 0.3, label = "First layer")


ax1.scatter(a2,e2, color = cl[1])
ax1.plot(a2,e2, color = cl[1], alpha = 0.3, label = "Second layer")

ax1.scatter(a3,e3, color = cl[2])
ax1.plot(a3,e3, color = cl[2], alpha = 0.3, label = "Third layer")

ax2 = ax1.twiny()
ax2.scatter(a1,e1,alpha=0)
ax2.set_xticklabels(atomic_radii)
ax2.set_xlabel("Atomic radius (pm)")
ax1.set_xlabel("Guest elements")
ax1.legend(loc="upper right")
ax1.set_ylabel("Adsorption Energy (eV)")
plt.tight_layout()
plt.savefig("figure_26.png")
plt.show()

"""
load_data('Hf',4,-9)
load_data('Ta',5,-8)
load_data('W',6,-7)
load_data('Re',7,-6)
load_data('Os',8,-5)
load_data('Ir',9,-4)
load_data('Pt',10,-3)
load_data('Au',11,-2)
load_data('Hg',12,-1)

"""









