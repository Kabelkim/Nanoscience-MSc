import glob, os, re, sys
import matplotlib.pyplot as plt
import numpy as np

#Load the energies from txt 
isExist = os.path.exists('results')
if not isExist:

   # Create a new directory because it does not exist
   os.makedirs('results')

#Sorting files
path = '/home/theoretical_catalysis/kabelkim/Desktop/masterproject/HCP vs FCC/fcc/3vs5/555_fixedlayers/'

slab = sorted(glob.glob(path+"*/*slab.txt"))
ads = sorted(glob.glob(path+"*/*ads.txt"))

elements = []
slab_e_zone2 = []
ads_e_zone2 = []
slab_e_zone3 = []
ads_e_zone3 = []

#Reference energies
h2o = -12.249268
h2 = -6.627349

#Zone2
zone2_slab = "pt_slab"
zone2_ads = "pt_ads"

for i in slab:
    if zone2_slab in i:
        elements.append(i.split("_")[-3])
        with open(i, 'r') as fp:
            lines = fp.readlines()
            for line in open(i):
                if line.find('Free energy:') != -1:
                    slab_e_zone2.append(line)
slab_e_zone2 = ([s.replace('Free energy:   ', '') for s in slab_e_zone2])
slab_e_zone2 = ([s.replace('\n', '') for s in slab_e_zone2])
slab_e_zone2 = [float(x) for x in slab_e_zone2]

for i in ads:
    if zone2_ads in i:
        with open(i, 'r') as fp:
            lines = fp.readlines()
            for line in open(i):
                if line.find('Free energy:') != -1:
                    ads_e_zone2.append(line)
ads_e_zone2 = ([s.replace('Free energy:   ', '') for s in ads_e_zone2])
ads_e_zone2 = ([s.replace('\n', '') for s in ads_e_zone2])
ads_e_zone2 = [float(x) for x in ads_e_zone2]

#Zone3
zone3 = "l_pt"

for i in slab:
    if zone3 in i:
        with open(i, 'r') as fp:
            lines = fp.readlines()
            for line in open(i):
                if line.find('Free energy:') != -1:
                    slab_e_zone3.append(line)
slab_e_zone3 = ([s.replace('Free energy:   ', '') for s in slab_e_zone3])
slab_e_zone3 = ([s.replace('\n', '') for s in slab_e_zone3])
slab_e_zone3 = [float(x) for x in slab_e_zone3]

for i in ads:
    if zone3 in i:
        with open(i, 'r') as fp:
            lines = fp.readlines()
            for line in open(i):
                if line.find('Free energy:') != -1:
                    ads_e_zone3.append(line)
ads_e_zone3 = ([s.replace('Free energy:   ', '') for s in ads_e_zone3])
ads_e_zone3 = ([s.replace('\n', '') for s in ads_e_zone3])
ads_e_zone3 = [float(x) for x in ads_e_zone3]

#Calculate Adsorption energies
E_zone2 = []
E_zone3 = []

for i in range(len(slab_e_zone2)):
    E_zone2.append(ads_e_zone2[i]+(0.5*h2)-slab_e_zone2[i]-h2o)
E_zone2 = [x - E_zone2[5] for x in E_zone2]

for i in range(len(slab_e_zone3)):
    E_zone3.append(ads_e_zone3[i]+(0.5*h2)-slab_e_zone3[i]-h2o)
E_zone3 = [x - E_zone3[5] for x in E_zone3]

elements = [str.title(x) for x in elements]

#Make order correct
e_zone2 = []
for i in range(1):
    e_zone2.append(None)
    e_zone2.append(E_zone2[1])
    e_zone2.append(E_zone2[7])
    e_zone2.append(E_zone2[-1])
    e_zone2.append(E_zone2[-3])
    e_zone2.append(E_zone2[4])
    e_zone2.append(E_zone2[3])
    e_zone2.append(E_zone2[5])
    e_zone2.append(E_zone2[0])
    e_zone2.append(E_zone2[2])

e_zone3 = []
for i in range(1):
    e_zone3.append(None)
    e_zone3.append(E_zone3[1])
    e_zone3.append(E_zone3[7])
    e_zone3.append(E_zone3[-1])
    e_zone3.append(E_zone3[-3])
    e_zone3.append(E_zone3[4])
    e_zone3.append(E_zone3[3])
    e_zone3.append(E_zone3[5])
    e_zone3.append(E_zone3[0])
    e_zone3.append(E_zone3[2])

ele = []
for i in range(1):
    ele.append("Lu")
    ele.append(elements[1])
    ele.append(elements[7])
    ele.append(elements[-1])
    ele.append(elements[-3])
    ele.append(elements[4])
    ele.append(elements[3])
    ele.append(elements[5])
    ele.append(elements[0])
    ele.append(elements[2])

val_e = np.arange(20,30)

#Plot
fig = plt.figure(figsize=(16,8))
ax1 = fig.add_subplot(111)
plt.style.use("seaborn-muted")
for xc in ele:
    ax1.axvline(x=xc, c="k", alpha=0.2, ls="--")
ax1.axhline(e_zone2[-3], c="k", alpha=0.9, ls="--", label="Pure host")    
ax1.scatter(ele,e_zone2, label=("Zone 2"), alpha=0.5)
ax1.scatter(ele,e_zone3, label=("Zone 3"), alpha=0.5)
ax1.plot(ele,e_zone2, alpha=0.9)
ax1.plot(ele,e_zone3, alpha=0.9)
ax1.set_ylabel(r'$\Delta E_{OH} - \Delta E^{Pt(0001)}_{OH}$ [eV]')
ax1.set_xlabel("Guest elements")
ax1.set_ylim(-0.4,0.5)
ax1.legend(loc='upper right',fancybox=True,framealpha=1)
ax2 = ax1.twiny()
ax2.set_xticks(val_e)
ax2.scatter(val_e,e_zone2, label=("Zone 2"), alpha=0.5)
ax2.set_xlabel("Valence electron total")
plt.savefig("results/Zone3bvs3c_335.png")
plt.show()
