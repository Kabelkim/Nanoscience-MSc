import glob, os, re, sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#Reference energies
h2o = -12.249268
h2 = -6.627349
pure_pt_hcp = -698.829625+0.5*h2-(-691.110676)-h2o

position='2_3_4'

#Load the energies from txt 
isExist = os.path.exists('results')
if not isExist:

   # Create a new directory because it does not exist
   os.makedirs('results')

dirs1 = '/home/theoretical_catalysis/kabelkim/Desktop/masterproject/HCP_vs_FCC/vec_eff_res/HCP/txt'
dirs2 = '/home/theoretical_catalysis/kabelkim/Desktop/masterproject/HCP_vs_FCC/hcp_re_atoms'

df_ads = pd.DataFrame(columns = [])
df_slab = pd.DataFrame(columns = [])
e_ads = []
e_slab = []
pos_ads = []
pos_slab = []

for root, folders, names in os.walk(dirs1):
    for name in names:
        if name.endswith('slab.txt'):
            with open(dirs1+'/'+name, 'r') as fp:
                pos_slab.append(name.split("_s")[0])
                lines = fp.readlines()
                for line in open(dirs1+'/'+name):
                    if line.find('Free energy:') != -1:
                        e_slab.append(float(line.split()[-1]))
        if name.endswith('ads.txt'):
            with open(dirs1+'/'+name, 'r') as fp:
                pos_ads.append(name.split("_a")[0])
                lines = fp.readlines()
                for line in open(dirs1+'/'+name):
                    if line.find('Free energy:') != -1:
                        e_ads.append(float(line.split()[-1]))


df_slab['e'] = e_slab
df_slab['pos'] = pos_slab

df_ads['e'] = e_ads
df_ads['pos'] = pos_ads

df_slab = df_slab.sort_values(by=['pos'])
df_ads = df_ads.sort_values(by=['pos'])

e_s = df_slab['e'].tolist()
e_a = df_ads['e'].tolist()
pos = df_ads['pos'].tolist()


e1 = ((df_ads.loc[df_ads['pos']==position]['e'].tolist()[0])+0.5*h2-(df_slab.loc[df_slab['pos']==position]['e'].tolist()[0])-h2o)-pure_pt_hcp


df_ads = pd.DataFrame(columns = [])
df_slab = pd.DataFrame(columns = [])
e_ads = []
e_slab = []
pos_ads = []
pos_slab = []

for i in position.split("_"):
    for root, folders, names in os.walk(dirs2):
        for name in names:
            if name.split("_")[1] == (str(i)):
                if name.endswith('slab.txt'):
                    with open(dirs2+'/'+name, 'r') as fp:
                        pos_slab.append(name.split("_")[1])
                        lines = fp.readlines()
                        for line in open(dirs2+'/'+name):
                            if line.find('Free energy:') != -1:
                                e_slab.append(float(line.split()[-1]))
                if name.endswith('ads.txt'):
                    with open(dirs2+'/'+name, 'r') as fp:
                        pos_ads.append(name.split("_")[1])
                        lines = fp.readlines()
                        for line in open(dirs2+'/'+name):
                            if line.find('Free energy:') != -1:
                                e_ads.append(float(line.split()[-1]))

df_slab['e'] = e_slab
df_slab['pos'] = pos_slab

df_ads['e'] = e_ads
df_ads['pos'] = pos_ads

df_slab = df_slab.sort_values(by=['pos'])
df_ads = df_ads.sort_values(by=['pos'])

e_s = df_slab['e'].tolist()
e_a = df_ads['e'].tolist()
pos = df_ads['pos'].tolist()

e2 = []
for i in range(len(e_s)):
    e2.append((e_a[i]+(0.5*h2)-e_s[i]-h2o)-pure_pt_hcp)

e2.append(np.sum(e2))
e2.append(e1)
print(e2)
clist = ["Green", "Blue", "Orange", "Violet", "Red"]
x = np.arange(int(len(e2)))

fig = plt.figure(figsize=(5,8))
for i in range(int(len(e2))):
    plt.bar(x[i],e2[i], width=1,color=clist[i])        
plt.ylabel(r'$\Delta E_{OH} - \Delta E^{Pt}_{OH}$ [eV]')
if int(len(e2)) == 4:
    plt.xticks(x, [str(position.split("_")[0]),str(position.split("_")[1]),str(position.split("_")[0] + "+" + position.split("_")[1] ),str(position)])
if int(len(e2)) == 5:
    plt.xticks(x, [str(position.split("_")[0]),str(position.split("_")[1]),str(position.split("_")[2]),str(position.split("_")[0] + "+" + position.split("_")[1] + "+" + position.split("_")[2]),str(position)])
plt.tight_layout()
plt.savefig("results/"+str(position)+".png")
plt.show()


