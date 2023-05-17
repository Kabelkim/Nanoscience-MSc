import glob, os, re, sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


elements = ['Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn','Y','Zr','Nb','Mo','Ru','Rh','Pd','Ag','Cd','Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg']
df_a = pd.DataFrame(columns = ['e_a','a_a'])
df_s = pd.DataFrame(columns = ['e_s','a_s'])
e_a = []
e_s = []
a_a = []
a_s = []
zone = []

#Reference energies
h2o = -12.249268
h2 = -6.627349

#Load the energies from txt 
isExist = os.path.exists('results')
if not isExist:

   # Create a new directory because it does not exist
   os.makedirs('results')

dirs = '/home/theoretical_catalysis/kabelkim/Desktop/masterproject/HCP_vs_FCC/Old stuff/many_atoms/HCP'
sub_folders = [name for name in os.listdir(dirs) if os.path.isdir(os.path.join(dirs, name))]
"""
for i in sub_folders:
   for j in range(2,5):
      if i.startswith('Zone'+str(j)):
         for files in os.listdir(dirs+'/Zone'+str(j)+'/txt/'):
            print(files)
"""
for i in range(10):
   for root, folders, names in os.walk(dirs):
      for name in names:
         if name.endswith('ads.txt'):
            if name.startswith('Zone'+str(i)):
               with open(dirs+'/Zone'+str(i)+'/txt/'+name, 'r') as fp:
                  a_a.append(str.title(name.split("_")[1]))
                  zone.append(str.title(name.split("_")[0]))
                  lines = fp.readlines()
                  for line in open(dirs+'/Zone'+str(i)+'/txt/'+name):
                     if line.find('Free energy:') != -1:
                        e_a.append(float(line.split()[-1]))
         if name.endswith("slab.txt"):
            if name.startswith('Zone'+str(i)):
               with open(dirs+'/Zone'+str(i)+'/txt/'+name, 'r') as fp:
                  a_s.append(str.title(name.split("_")[1]))
                  lines = fp.readlines()
                  for line in open(dirs+'/Zone'+str(i)+'/txt/'+name):
                     if line.find('Free energy:') != -1:
                        e_s.append(float(line.split()[-1]))
         
df_a['e_a'] = e_a
df_a['a_a'] = a_a
df_a1 = df_a.iloc[:int(len(e_a)/3),:]
df_a2 = df_a.iloc[int(len(e_a)/3):int(len(e_a)/3)*2,:]
df_a3 = df_a.iloc[int(len(e_a)/3)*2:,:]

l = len(a_s) // 3
first_a, second_a,third_a = a_s[:l], a_s[l:l*2], a_s[l*2:]

df_a1.sort_values(by="a_a", key=lambda column: column.map(lambda e: first_a.index(e)), inplace=True)
df_a2.sort_values(by="a_a", key=lambda column: column.map(lambda e: second_a.index(e)), inplace=True)
df_a3.sort_values(by="a_a", key=lambda column: column.map(lambda e: third_a.index(e)), inplace=True)



df_a1['e_s'] = e_s[:l]
df_a2['e_s'] = e_s[l:l*2]
df_a3['e_s'] = e_s[l*2:]
print(df_a1)
df_a1.sort_values(by="a_a", key=lambda column: column.map(lambda e: elements.index(e)), inplace=True)
df_a2.sort_values(by="a_a", key=lambda column: column.map(lambda e: elements.index(e)), inplace=True)
df_a3.sort_values(by="a_a", key=lambda column: column.map(lambda e: elements.index(e)), inplace=True)

ea1 = df_a1['e_a'].tolist()
ea2 = df_a2['e_a'].tolist()
ea3 = df_a3['e_a'].tolist()
                  
es1 = df_a1['e_s'].tolist()
es2 = df_a2['e_s'].tolist()
es3 = df_a3['e_s'].tolist()
                  
e_zone2 = []
e_zone3 = []
e_zone4 = []

for i in range(len(ea1)):
    e_zone2.append(ea1[i]+(0.5*h2)-es1[i]-h2o)
e_zone2 = [x - e_zone2[-3] for x in e_zone2]

for i in range(len(ea2)):
    e_zone3.append(ea2[i]+(0.5*h2)-es2[i]-h2o)
e_zone3 = [x - e_zone3[-3] for x in e_zone3]

for i in range(len(ea3)):
    e_zone4.append(ea3[i]+(0.5*h2)-es3[i]-h2o)
e_zone4 = [x - e_zone4[-3] for x in e_zone4]

val_e = []
for i in range(3):
   val_e.append(list(np.arange(20,30)))
val_e = sum(val_e,[])
elements = ['Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','Lu','Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg']

ez2 = e_zone2
ez3 = e_zone3
ez4 = e_zone4

#Matchfixing
e_zone2.insert(14, None)
e_zone2.insert(20, None)
e_zone3.insert(14, None)
e_zone3.insert(20, None)
e_zone4.insert(14, None)
e_zone4.insert(20, None)


#Plot
fig = plt.figure(figsize=(16,8))
ax1 = fig.add_subplot(111)
plt.style.use("seaborn-muted")
for xc in elements:
    ax1.axvline(x=xc, c="k", alpha=0.1, ls="--")
ax1.axhline(e_zone2[-3], c="k", alpha=0.9, ls="--", label="Pure host")    
ax1.scatter(elements,e_zone2, alpha=0.5, c='r')
ax1.scatter(elements,e_zone3, alpha=0.5,c='b')
ax1.scatter(elements,e_zone4, alpha=0.5,c='g')

ez2[14] = -0.1
ez2[20] = 0.35
ez3[14] = 0.1
ez3[20] = 0
ez4[14] = -0.023
ez4[20] = 0.05

ax1.plot(elements,ez2,ls="solid", alpha=0.3,c='r', label="Zone 2")
ax1.plot(elements,ez3,ls="solid", alpha=0.3,c='b', label="Zone 3")
ax1.plot(elements,ez4,ls="solid", alpha=0.3,c='g', label="Zone 4")

ax1.set_ylabel(r'$\Delta E_{OH} - \Delta E^{Pt(111)}_{OH}$ [eV]')
ax1.set_xlabel("Guest elements")
#ax1.set_ylim(-0.4,0.5)

ax1.legend(loc='upper right',fancybox=True,framealpha=1)

ax2 = ax1.twiny()
ax2.scatter(elements,e_zone2, alpha=0)
ax2.set(xticks=range(30), xticklabels=val_e)
ax2.set_xlabel("Valence electron total")
plt.tight_layout()
plt.savefig("results/figure_10.png")
plt.show()

