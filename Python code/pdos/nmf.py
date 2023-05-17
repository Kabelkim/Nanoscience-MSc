import numpy as np
import sys, os
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA, NMF

data = []
for i in os.listdir("./fcc/2_layers/pdos/"):
    if i.split(".")[0].endswith("_dos"):
        a = np.loadtxt("./fcc/2_layers/pdos/"+str(i))
        a = (a - np.min(a)) / (np.max(a) - np.min(a))
        a = np.array(a).T
        a = a[1250:]
        data.append(a)
e = np.linspace(-58.7,5.6,len(data[0]))
e = e[1250:]

n_components = 6
pca = PCA(n_components=n_components)
df_pca = pca.fit_transform(data)
variance_exp_cumsum = pca.explained_variance_ratio_.round(2).cumsum()

fig, ax = plt.subplots(nrows=1, figsize=(12,9))
plt.plot(range(1, (n_components + 1)), variance_exp_cumsum, "o", color="firebrick")
ax.set_xlabel('number of components')
ax.set_ylabel('Variance Explained (%)')
plt.xlim(0, (n_components + 1))
plt.ylim((variance_exp_cumsum[0] - 0.01), (variance_exp_cumsum[-1] + 0.01))
plt.show()

nmf_com = 3

nmf = NMF(n_components=nmf_com, init="random", random_state=0, max_iter=20000)
W = nmf.fit_transform(data)
fig, ax = plt.subplots(nrows=1, figsize=(12, 9))
for i in range(np.shape(W)[1]):
    W[:, i] = (W[:, i] - np.min(W[:, i])) / (np.max(W[:, i]) - np.min(W[:, i]))
for j in range(nmf_com):
    plt.plot(W.T[j] - j, label="NMF Component Number " + str(int(j + 1)))
ax.set_xlabel('r[Å]')
ax.set_ylabel('G(r) [a.u]')
ax.set_yticklabels('')
plt.legend(loc="upper right")
plt.show()
