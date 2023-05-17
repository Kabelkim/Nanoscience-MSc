import os, sys, shutil, random
import numpy as np
from pathlib import Path

err = []
for names in sorted(Path('./err').iterdir(), key=os.path.getmtime):
    with open(names, 'r') as fp:
        lines = fp.readlines()
        if len(lines) != 0:
            a = (str(names).split("/")[-1])
            err.append(a.split(".")[0])

os.mkdir("crash")
os.mkdir("crash/err")
os.mkdir("crash/log")
os.mkdir("crash/txt")
os.mkdir("crash/py")
os.mkdir("crash/sl")


for names in err:
    shutil.copyfile('./sl/'+names+'.sl', 'crash/sl/'+names+'.sl')
    with open('./py/'+names+'.py', 'r') as fp:
        lines = fp.readlines()
        new_py = []
        new_py.extend(lines[:-19])
        new_py.extend(lines[-11:])
        a = np.reshape(new_py,(int(len(new_py)),))
        res = []
        for sub in a:
            res.append(sub.replace("\n", ""))
        np.savetxt('crash/py/'+names+'.py',res,fmt='%s')

    
