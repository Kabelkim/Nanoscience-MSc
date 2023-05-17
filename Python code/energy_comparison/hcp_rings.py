import glob, os, re, sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#Reference energies
h2o = -12.249268
h2 = -6.627349

#HCP
pure_pt_hcp = -698.829625+0.5*h2-(-691.110676)-h2o

#FCC
pure_pt_hcp = -703.920177+0.5*h2-(-696.162471)-h2o

#Load the energies from txt 
isExist = os.path.exists('results')
if not isExist:

   # Create a new directory because it does not exist
   os.makedirs('results')

dirs1 = '/home/theoretical_catalysis/kabelkim/Desktop/masterproject/HCP_vs_FCC/vec_eff_res/FCC/txt'
dirs2 = '/home/theoretical_catalysis/kabelkim/Desktop/masterproject/HCP_vs_FCC/atom_pos_re_fcc/txt'
dirs3 = '/home/theoretical_catalysis/kabelkim/Desktop/masterproject/HCP_vs_FCC/lagkage/txt'

df_ads = pd.DataFrame(columns = [])
df_slab = pd.DataFrame(columns = [])
e_ads = []
e_slab = []
pos_ads = []
pos_slab = []

n = "ring5"
layer = "5"
for root, folders, names in os.walk(dirs1):
    for name in names:
        if name.startswith(n):
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


e1 = (e_a[0]+(0.5*h2)-e_s[0]-h2o)-pure_pt_hcp


df_ads = pd.DataFrame(columns = [])
df_slab = pd.DataFrame(columns = [])
e_ads = []
e_slab = []
pos_ads = []
pos_slab = []

n = "con5"

for root, folders, names in os.walk(dirs1):
    for name in names:
        if name.startswith(n):
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



e2 = []
for i in range(len(e_s)):
    e2.append((e_a[i]+(0.5*h2)-e_s[i]-h2o)-pure_pt_hcp)
e2 = np.sum(e2)

df_ads = pd.DataFrame(columns = [])
df_slab = pd.DataFrame(columns = [])
e_ads = []
e_slab = []
pos_ads = []
pos_slab = []

for i in [1,21]:
    for root, folders, names in os.walk(dirs2):
        for name in names:
                if name.startswith('Zone' + layer+ '_' + (str(i))):
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

e6 = []
for i in range(len(e_s)):
    e6.append((e_a[i]+(0.5*h2)-e_s[i]-h2o)-pure_pt_hcp)
e6 = np.sum(e6)


df_ads = pd.DataFrame(columns = [])
df_slab = pd.DataFrame(columns = [])
e_ads = []
e_slab = []
pos_ads = []
pos_slab = []

for i in [1,2,3,4,9,13,17,21,16,11,6]:
    for root, folders, names in os.walk(dirs2):
        for name in names:
                if name.startswith('Zone' + layer+ '_' + (str(i))):
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

e3 = []
for i in range(len(e_s)):
    e3.append((e_a[i]+(0.5*h2)-e_s[i]-h2o)-pure_pt_hcp)
e3 = np.sum(e3)

df_ads = pd.DataFrame(columns = [])
df_slab = pd.DataFrame(columns = [])
e_ads = []
e_slab = []
pos_ads = []
pos_slab = []


for root, folders, names in os.walk(dirs2):
    for name in names:
            if name.startswith('Zone' + layer+ '_'):
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

e4 = []
for i in range(len(e_s)):
    e4.append((e_a[i]+(0.5*h2)-e_s[i]-h2o)-pure_pt_hcp)
e4 = np.sum(e3)

df_ads = pd.DataFrame(columns = [])
df_slab = pd.DataFrame(columns = [])
e_ads = []
e_slab = []
pos_ads = []
pos_slab = []

for root, folders, names in os.walk(dirs3):
    for name in names:
        if name.startswith("fcc"):
            if name.split("_")[-2] == layer:
                if name.endswith('slab.txt'):
                    with open(dirs3+'/'+name, 'r') as fp:
                        pos_slab.append(name.split("_")[-2])
                        lines = fp.readlines()
                        for line in open(dirs3+'/'+name):
                            if line.find('Free energy:') != -1:
                                e_slab.append(float(line.split()[-1]))
                if name.endswith('ads.txt'):
                    with open(dirs3+'/'+name, 'r') as fp:
                        pos_ads.append(name.split("_")[-2])
                        lines = fp.readlines()
                        for line in open(dirs3+'/'+name):
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

e5 = (e_a[0]+(0.5*h2)-e_s[0]-h2o)-pure_pt_hcp

e = []
e.append(e1)
e.append(e3)
e.append(e2)
e.append(e6)
e.append(e5)
e.append(e4)


clist = ["Green", "Blue", "Orange", "Violet", "Red", "Brown"]
x = np.arange(int(len(e)))

fig = plt.figure(figsize=(6,8))

for i in range(int(len(e))):
    plt.bar(x[i],e[i], width=1,color=clist[i])        
plt.ylabel(r'$\Delta E_{OH} - \Delta E^{Pt}_{OH}$ [eV]')
plt.xticks(x, ["Ring", "Ring atoms", "Corner","Corner atoms", "Layer","Layer atoms"])
plt.tight_layout()
plt.savefig("results/fcc_"+str(n)+"_mid"+".png")
plt.show()



