import os, sys, shutil, random
import numpy as np
from pathlib import Path

runs = []
for names in sorted(Path('./py').iterdir(), key=os.path.getmtime):
    runs.append(str(names).split("/")[1].replace(".py",""))

dft = []
for names in sorted(Path('./txt').iterdir(), key=os.path.getmtime):
    if (str(names).split("/")[1].split(".")[0]).endswith("ads"):
        dft.append((str(names).split("/")[1].split(".")[0]).replace("_ads",""))


new = list(set(runs) - set(dft))

os.mkdir("failed")
os.mkdir("failed/err")
os.mkdir("failed/log")
os.mkdir("failed/txt")
os.mkdir("failed/py")
os.mkdir("failed/sl")

for names in new:
    shutil.copyfile('./sl/'+names+'.sl', 'failed/sl/'+names+'.sl')
    shutil.copyfile('./py/'+names+'.py', 'failed/py/'+names+'.py')

