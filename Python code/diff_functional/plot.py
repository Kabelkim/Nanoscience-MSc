import glob, os, re, sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib
from matplotlib import style
from scipy import stats



def load_data(atom,y1=-8.5,y2=-1.5):
    if atom == 'O':
        pos = 3
        c = 'red'
    if atom == 'N':
        pos = 3.5
        c = 'blue'
    if atom == 'C':
        pos = 4
        c = 'black'
    if atom == 'H':
        pos = 5
        c = 'grey'
    dirs1 = './txt'
    elements = ['Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn','Y','Zr','Nb','Mo','Ru','Rh','Pd','Ag','Cd','Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg']
    df1 = pd.DataFrame(columns=[])
    df2 = pd.DataFrame(columns=[])
    a_a = []
    a_s = []
    e_s = []
    e_a = []

    for file in os.listdir(dirs1):
        if file.split("_")[0] == atom:
            if file.split("_")[2] == 'ads.txt':
                with open(dirs1+'/'+file, 'r') as fp:
                    a_a.append(file.split("_")[1])
                    lines = fp.readlines()
                    for line in open(dirs1+'/'+file):
                        if line.find('Free energy:') != -1:
                            e_a.append(float(line.split()[-1]))
            if file.split("_")[2] == 'slab.txt':
                with open(dirs1+'/'+file, 'r') as fp:
                    a_s.append(file.split("_")[1])
                    lines = fp.readlines()
                    for line in open(dirs1+'/'+file):
                        if line.find('Free energy:') != -1:
                            e_s.append(float(line.split()[-1]))
    df1['a'] = a_s
    df1['e'] = e_s

    df2['a'] = a_a
    df2['e'] = e_a

    df1.sort_values(by="a", key=lambda column: column.map(lambda e: elements.index(e)), inplace=True)
    df2.sort_values(by="a", key=lambda column: column.map(lambda e: elements.index(e)), inplace=True)

    e_s = df1['e'].tolist()
    e_a = df2['e'].tolist()
    a = df1['a'].tolist()

    e = []
    for i in range(len(e_s)):
        e.append(e_a[i]-e_s[i])
        
    d3_e = e[:4]
    d3_e.extend(e[5:8])
    ad3 = a[:4]
    ad3.extend(a[5:8])
    d4_e = e[10:17]
    ad4 = a[10:17]
    d5_e = e[19:22]
    d5_e.extend(e[23:26])
    ad5 = a[19:22]
    ad5.extend(a[23:26])
    d5_e.insert(0,None)
    ad4.insert(0,None)
    x_axis = np.arange(0,7)
    ad3.insert(0,None)
    #Plot
    fig = plt.figure(figsize=(6,8))
    ax1 = fig.add_subplot(111)
    if atom == 'H':
        ax1.yaxis.set_label_position("right")
        ax1.yaxis.tick_right()
        ax1.set_ylim(-4.5,-0.5)
    else:
        ax1.yaxis.tick_left()
        ax1.set_ylim(y1,y2)
    
    ax1.grid(alpha=0.4, ls="--")
    ax1.plot(x_axis,d3_e, color = c)
    ax1.scatter(x_axis,d3_e, color = c)
    ax1.set_xticklabels([2,3,4,5,6,8,9,10])
    #ax1.axvline(pos, color ='k', lw = 1, alpha = 0.6, ls='--')
    ax2 = ax1.twiny()
    ax2.scatter(x_axis,d3_e,alpha=0)
    ax2.set_xticklabels(ad3)
    ax1.set_ylabel("Adsorption Energy (eV)")
    ax2.set_xlabel("Dopant")
    plt.savefig(atom+"_1_plot.png")

    #Plot 2
    fig = plt.figure(figsize=(6,8))
    ax1 = fig.add_subplot(111)
    if atom == 'H':
        ax1.yaxis.set_label_position("right")
        ax1.yaxis.tick_right()
        ax1.set_ylim(-4.5,-0.5)
    else:
        ax1.yaxis.tick_left()
        ax1.set_ylim(y1,y2)
    
    ax1.grid(alpha=0.4, ls="--")
    ax1.plot(x_axis,d4_e, color = c)
    ax1.scatter(x_axis,d4_e, color = c)
    ax1.plot(x_axis,d5_e, color = c)
    ax1.scatter(x_axis,d5_e, color = c)
    ax1.set_xticklabels(ad4)
    ax1.axvline(pos, color = c, lw = 1, alpha = 0.6, ls='dashdot')
    ax2 = fig.add_axes((0.28,0.11,0.585,0.0))
    ax2.yaxis.set_visible(False) # hide the yaxis
    ax2.yaxis.set_visible(False) # hide the yaxis

    ax2.set_xticklabels(ad5)
    ax2.tick_params(axis='both', which='major', pad=15)
    ax3 = ax1.twiny()
    ax3.scatter(x_axis,d4_e,alpha=0)
    ax3.set_xticklabels([2,3,4,5,6,8,9,10])
    ax1.set_ylabel("Adsorption Energy (eV)")
    ax1.set_xlabel("Dopant", labelpad=15)
    plt.savefig(atom+"_2_plot.png")
    return
dope = ['O','N','C','H']
for i in dope:
    load_data(atom=i,y1=-18.5,y2=-9.5)

