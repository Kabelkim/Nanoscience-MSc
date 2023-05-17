import glob, os, re, sys
import matplotlib.pyplot as plt
import numpy as np

#Load the energies from txt 
isExist = os.path.exists('results')
if not isExist:

   # Create a new directory because it does not exist
   os.makedirs('results')

#Sorting files
path = '/home/theoretical_catalysis/kabelkim/Desktop/masterproject/HCP_vs_FCC/Old stuff/many_layers_fcc/4_layers/'
path2 = '/home/theoretical_catalysis/kabelkim/Desktop/masterproject/HCP_vs_FCC/Old stuff/fcc/3vs5/555_fixedlayers/txt'
path3 = '/home/theoretical_catalysis/kabelkim/Desktop/masterproject/HCP_vs_FCC/Old stuff/many_layers_fcc/6_layers/'
path4 = '/home/theoretical_catalysis/kabelkim/Desktop/masterproject/HCP_vs_FCC/Old stuff/many_layers_fcc/7_layers/'

slab = sorted(glob.glob(path+"*/*slab.txt"))
ads = sorted(glob.glob(path+"*/*ads.txt"))

slab2 = sorted(glob.glob(path2+"*/*slab.txt"))
ads2 = sorted(glob.glob(path2+"*/*ads.txt"))

slab3 = sorted(glob.glob(path3+"*/*slab.txt"))
ads3 = sorted(glob.glob(path3+"*/*ads.txt"))

slab4 = sorted(glob.glob(path4+"*/*slab.txt"))
ads4 = sorted(glob.glob(path4+"*/*ads.txt"))

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

elements2 = []
slab_e_zone22 = []
ads_e_zone22 = []
slab_e_zone32 = []
ads_e_zone32 = []

#Zone2
zone2_slab2 = "pt_slab"
zone2_ads2 = "pt_ads"

for i in slab2:
    if zone2_slab2 in i:
        elements2.append(i.split("_")[-3])
        with open(i, 'r') as fp:
            lines = fp.readlines()
            for line in open(i):
                if line.find('Free energy:') != -1:
                    slab_e_zone22.append(line)
slab_e_zone22 = ([s.replace('Free energy:   ', '') for s in slab_e_zone22])
slab_e_zone22 = ([s.replace('\n', '') for s in slab_e_zone22])
slab_e_zone22 = [float(x) for x in slab_e_zone22]

for i in ads2:
    if zone2_ads2 in i:
        with open(i, 'r') as fp:
            lines = fp.readlines()
            for line in open(i):
                if line.find('Free energy:') != -1:
                    ads_e_zone22.append(line)
ads_e_zone22 = ([s.replace('Free energy:   ', '') for s in ads_e_zone22])
ads_e_zone22 = ([s.replace('\n', '') for s in ads_e_zone22])
ads_e_zone22 = [float(x) for x in ads_e_zone22]

#Zone3
zone32 = "l_pt"

for i in slab2:
    if zone32 in i:
        with open(i, 'r') as fp:
            lines = fp.readlines()
            for line in open(i):
                if line.find('Free energy:') != -1:
                    slab_e_zone32.append(line)
slab_e_zone32 = ([s.replace('Free energy:   ', '') for s in slab_e_zone32])
slab_e_zone32 = ([s.replace('\n', '') for s in slab_e_zone32])
slab_e_zone32 = [float(x) for x in slab_e_zone32]

for i in ads2:
    if zone32 in i:
        with open(i, 'r') as fp:
            lines = fp.readlines()
            for line in open(i):
                if line.find('Free energy:') != -1:
                    ads_e_zone32.append(line)
ads_e_zone32 = ([s.replace('Free energy:   ', '') for s in ads_e_zone32])
ads_e_zone32 = ([s.replace('\n', '') for s in ads_e_zone32])
ads_e_zone32 = [float(x) for x in ads_e_zone32]

#Calculate Adsorption energies
E_zone22 = []
E_zone32 = []

for i in range(len(slab_e_zone22)):
    E_zone22.append(ads_e_zone22[i]+(0.5*h2)-slab_e_zone22[i]-h2o)
E_zone22 = [x - E_zone22[5] for x in E_zone22]

for i in range(len(slab_e_zone32)):
    E_zone32.append(ads_e_zone32[i]+(0.5*h2)-slab_e_zone32[i]-h2o)
E_zone32 = [x - E_zone32[5] for x in E_zone32]

#Make order correct
e_zone22 = []
for i in range(1):
    e_zone22.append(None)
    e_zone22.append(E_zone22[1])
    e_zone22.append(E_zone22[7])
    e_zone22.append(E_zone22[-1])
    e_zone22.append(E_zone22[-3])
    e_zone22.append(E_zone22[4])
    e_zone22.append(E_zone22[3])
    e_zone22.append(E_zone22[5])
    e_zone22.append(E_zone22[0])
    e_zone22.append(E_zone22[2])

e_zone32 = []
for i in range(1):
    e_zone32.append(None)
    e_zone32.append(E_zone32[1])
    e_zone32.append(E_zone32[7])
    e_zone32.append(E_zone32[-1])
    e_zone32.append(E_zone32[-3])
    e_zone32.append(E_zone32[4])
    e_zone32.append(E_zone32[3])
    e_zone32.append(E_zone32[5])
    e_zone32.append(E_zone32[0])
    e_zone32.append(E_zone32[2])

elements3 = []
slab_e_zone23 = []
ads_e_zone23 = []
slab_e_zone33 = []
ads_e_zone33 = []

#Zone2
zone2_slab3 = "pt_slab"
zone2_ads3 = "pt_ads"

for i in slab3:
    if zone2_slab3 in i:
        elements3.append(i.split("_")[-3])
        with open(i, 'r') as fp:
            lines = fp.readlines()
            for line in open(i):
                if line.find('Free energy:') != -1:
                    slab_e_zone23.append(line)
slab_e_zone23 = ([s.replace('Free energy:   ', '') for s in slab_e_zone23])
slab_e_zone23 = ([s.replace('\n', '') for s in slab_e_zone23])
slab_e_zone23 = [float(x) for x in slab_e_zone23]

for i in ads3:
    if zone2_ads3 in i:
        with open(i, 'r') as fp:
            lines = fp.readlines()
            for line in open(i):
                if line.find('Free energy:') != -1:
                    ads_e_zone23.append(line)
ads_e_zone23 = ([s.replace('Free energy:   ', '') for s in ads_e_zone23])
ads_e_zone23 = ([s.replace('\n', '') for s in ads_e_zone23])
ads_e_zone23 = [float(x) for x in ads_e_zone23]

#Zone3
zone33 = "l_pt"

for i in slab3:
    if zone33 in i:
        with open(i, 'r') as fp:
            lines = fp.readlines()
            for line in open(i):
                if line.find('Free energy:') != -1:
                    slab_e_zone33.append(line)
slab_e_zone33 = ([s.replace('Free energy:   ', '') for s in slab_e_zone33])
slab_e_zone33 = ([s.replace('\n', '') for s in slab_e_zone33])
slab_e_zone33 = [float(x) for x in slab_e_zone33]

for i in ads3:
    if zone33 in i:
        with open(i, 'r') as fp:
            lines = fp.readlines()
            for line in open(i):
                if line.find('Free energy:') != -1:
                    ads_e_zone33.append(line)
ads_e_zone33 = ([s.replace('Free energy:   ', '') for s in ads_e_zone33])
ads_e_zone33 = ([s.replace('\n', '') for s in ads_e_zone33])
ads_e_zone33 = [float(x) for x in ads_e_zone33]

#Calculate Adsorption energies
E_zone23 = []
E_zone33 = []

for i in range(len(slab_e_zone23)):
    E_zone23.append(ads_e_zone23[i]+(0.5*h2)-slab_e_zone23[i]-h2o)
E_zone23 = [x - E_zone23[5] for x in E_zone23]

for i in range(len(slab_e_zone33)):
    E_zone33.append(ads_e_zone33[i]+(0.5*h2)-slab_e_zone33[i]-h2o)
E_zone33 = [x - E_zone33[5] for x in E_zone33]

#Make order correct
e_zone23 = []
for i in range(1):
    e_zone23.append(None)
    e_zone23.append(E_zone23[1])
    e_zone23.append(E_zone23[7])
    e_zone23.append(E_zone23[-1])
    e_zone23.append(E_zone23[-3])
    e_zone23.append(E_zone23[4])
    e_zone23.append(E_zone23[3])
    e_zone23.append(E_zone23[5])
    e_zone23.append(E_zone23[0])
    e_zone23.append(E_zone23[2])

e_zone33 = []
for i in range(1):
    e_zone33.append(None)
    e_zone33.append(E_zone33[1])
    e_zone33.append(E_zone33[7])
    e_zone33.append(E_zone33[-1])
    e_zone33.append(E_zone33[-3])
    e_zone33.append(E_zone33[4])
    e_zone33.append(E_zone33[3])
    e_zone33.append(E_zone33[5])
    e_zone33.append(E_zone33[0])
    e_zone33.append(E_zone33[2])

elements4 = []
slab_e_zone24 = []
ads_e_zone24 = []
slab_e_zone34 = []
ads_e_zone34 = []

#Zone2
zone2_slab4 = "pt_slab"
zone2_ads4 = "pt_ads"

for i in slab4:
    if zone2_slab4 in i:
        elements4.append(i.split("_")[-3])
        with open(i, 'r') as fp:
            lines = fp.readlines()
            for line in open(i):
                if line.find('Free energy:') != -1:
                    slab_e_zone24.append(line)
slab_e_zone24 = ([s.replace('Free energy:   ', '') for s in slab_e_zone24])
slab_e_zone24 = ([s.replace('\n', '') for s in slab_e_zone24])
slab_e_zone24 = [float(x) for x in slab_e_zone24]

for i in ads4:
    if zone2_ads4 in i:
        with open(i, 'r') as fp:
            lines = fp.readlines()
            for line in open(i):
                if line.find('Free energy:') != -1:
                    ads_e_zone24.append(line)
ads_e_zone24 = ([s.replace('Free energy:   ', '') for s in ads_e_zone24])
ads_e_zone24 = ([s.replace('\n', '') for s in ads_e_zone24])
ads_e_zone24 = [float(x) for x in ads_e_zone24]

#Zone3
zone34 = "l_pt"

for i in slab4:
    if zone34 in i:
        with open(i, 'r') as fp:
            lines = fp.readlines()
            for line in open(i):
                if line.find('Free energy:') != -1:
                    slab_e_zone34.append(line)
slab_e_zone34 = ([s.replace('Free energy:   ', '') for s in slab_e_zone34])
slab_e_zone34 = ([s.replace('\n', '') for s in slab_e_zone34])
slab_e_zone34 = [float(x) for x in slab_e_zone34]

for i in ads4:
    if zone34 in i:
        with open(i, 'r') as fp:
            lines = fp.readlines()
            for line in open(i):
                if line.find('Free energy:') != -1:
                    ads_e_zone34.append(line)
ads_e_zone34 = ([s.replace('Free energy:   ', '') for s in ads_e_zone34])
ads_e_zone34 = ([s.replace('\n', '') for s in ads_e_zone34])
ads_e_zone34 = [float(x) for x in ads_e_zone34]

#Calculate Adsorption energies
E_zone24 = []
E_zone34 = []

for i in range(len(slab_e_zone24)):
    E_zone24.append(ads_e_zone24[i]+(0.5*h2)-slab_e_zone24[i]-h2o)
E_zone24 = [x - E_zone24[5] for x in E_zone24]

for i in range(len(slab_e_zone34)):
    E_zone34.append(ads_e_zone34[i]+(0.5*h2)-slab_e_zone34[i]-h2o)
E_zone34 = [x - E_zone34[5] for x in E_zone34]

#Make order correct
e_zone24 = []
for i in range(1):
    e_zone24.append(None)
    e_zone24.append(E_zone24[1])
    e_zone24.append(E_zone24[7])
    e_zone24.append(E_zone24[-1])
    e_zone24.append(E_zone24[-3])
    e_zone24.append(E_zone24[4])
    e_zone24.append(E_zone24[3])
    e_zone24.append(E_zone24[5])
    e_zone24.append(E_zone24[0])
    e_zone24.append(E_zone24[2])

e_zone34 = []
for i in range(1):
    e_zone34.append(None)
    e_zone34.append(E_zone34[1])
    e_zone34.append(E_zone34[7])
    e_zone34.append(E_zone34[-1])
    e_zone34.append(E_zone34[-3])
    e_zone34.append(E_zone34[4])
    e_zone34.append(E_zone34[3])
    e_zone34.append(E_zone34[5])
    e_zone34.append(E_zone34[0])
    e_zone34.append(E_zone34[2])
    
#Plot
fig = plt.figure(figsize=(16,8))
ax1 = fig.add_subplot(111)
plt.style.use("seaborn-muted")
for xc in ele:
    ax1.axvline(x=xc, c="k", alpha=0.1, ls="--")
ax1.axhline(e_zone2[-3], c="k", alpha=0.9, ls="--", label="Pure host")    
ax1.scatter(ele,e_zone2, alpha=0.5, c='r')
ax1.scatter(ele,e_zone3, alpha=0.5,c='b')
ax1.plot(ele,e_zone2,ls="solid", alpha=0.3,c='r', label="Zone 2")
ax1.plot(ele,e_zone3,ls="solid", alpha=0.3,c='b', label="Zone 3")
ax1.scatter(ele,e_zone22,alpha=0.5,c='r')
ax1.scatter(ele,e_zone32, alpha=0.5, c='b')
ax1.plot(ele,e_zone22,ls="dotted", alpha=0.3,c='r')
ax1.plot(ele,e_zone32,ls="dotted", alpha=0.3,c='b')
ax1.scatter(ele,e_zone23,  alpha=0.5,c='r')
ax1.scatter(ele,e_zone33, alpha=0.5, c='b')
ax1.plot(ele,e_zone23,ls="dashed", alpha=0.3,c='r')
ax1.plot(ele,e_zone33,ls="dashed", alpha=0.3,c='b')
ax1.scatter(ele,e_zone24, alpha=0.5,c='r')
ax1.scatter(ele,e_zone34, alpha=0.5, c='b')
ax1.plot(ele,e_zone24,ls="dashdot", alpha=0.3,c='r')
ax1.plot(ele,e_zone34,ls="dashdot", alpha=0.3,c='b')
ax1.set_ylim(-0.3,0.4)
ax1.set_ylabel(r'$\Delta E_{OH} - \Delta E^{Pt(111)}_{OH}$ [eV]')
ax1.set_xlabel("Guest elements")

ax1.text(0.3,0.05, "5&7 Layers", c="b")
ax1.text(0.3,0.03, "4&6 Layers", c="b")

ax1.text(0.3,0.27, "5&7 Layers", c="r")
ax1.text(0.3,0.25, "4&6 Layers", c="r")


#ax1.set_ylim(-0.4,0.5)
ax1.legend(loc='upper right',fancybox=True,framealpha=1)
"""
ax2 = ax1.twiny()
ax2.set_xticks(val_e)
ax2.scatter(val_e,e_zone2, label=("Zone 2"), alpha=0.5)
ax2.set_xlabel("Valence electron total")
"""
plt.tight_layout()
plt.savefig("results/figure_9.png")
plt.show()
