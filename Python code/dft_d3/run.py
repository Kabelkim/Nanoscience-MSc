#!/bin/python3

import sys
import os
import numpy as np
from time import sleep

# DFT parameters
xc = 'PBE'
ecut = 400

# k-points to run over in turn to hopefully converge faster
kpts = (3,3,1)

# Cluster parameters
partition = 'katla_short'
nodes = 1
ntasks = 8
ntasks_per_core = 2
mem_per_cpu = 1000

os.system("mkdir sl")
os.system("mkdir py")
os.system("mkdir txt")
os.system("mkdir err")
os.system("mkdir log")
os.system("mkdir pdos")
os.system("mkdir plot")


elements = ['Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn','Y','Zr','Nb','Mo','Ru','Rh','Pd','Ag','Cd','Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg']
adsorbates = ['O','N','C','H']

for ads in adsorbates:
	for guest1 in elements:
		filename = ads + '_' + guest1 
		with open('py/' + filename + '.py', 'w') as f:
			f.write("from gpaw import GPAW, PW\n"\
			"from ase.calculators.dftd3 import DFTD3\n"\
			"from ase import Atoms\n"\
			"from ase.build import fcc111, add_adsorbate\n"\
			"from ase.optimize import QuasiNewton\n"\
			"import numpy as np\n"\
			"import matplotlib.pyplot as plt\n"\
	                "from ase.dft.dos import DOS\n"\
			"\n"\
			"atoms = fcc111('Au', size=(3,3,3), vacuum=7.5, a=4.08)\n"\
			"\n"\
			"atoms[22].symbol = '{guest1}'\n"\
			"\n"\
			"dft = GPAW(mode=PW({ecut}),\n"\
			"		kpts={kpts},\n"\
			"		xc='{xc}',\n"\
			"		txt='{slab_txt}')\n"\
			"d3 = DFTD3(dft=dft)\n"\
			"atoms.calc = d3\n"\
			"\n"\
			"atoms.set_calculator(dft)\n"\
			"atoms.get_potential_energy()\n"\
			"\n"\
			"add_adsorbate(atoms,'{ads}',2.02,position=[4.2, 2.5])\n"\
			"dft = GPAW(mode=PW({ecut}),\n"\
			"		kpts={kpts},\n"\
			"		xc='{xc}',\n"\
			"		txt='{ads_txt}')\n"\
			"\n"\
			"d3 = DFTD3(dft=dft)\n"\
			"atoms.calc = d3\n"\
			"atoms.set_calculator(dft)\n"\
			"atoms.get_potential_energy()\n"\
			"\n"\
                	"dos = DOS(dft,npts=2001, width=0.2)\n"\
                	"d = dos.get_dos()\n"\
                	"e = dos.get_energies()\n"\
                	"e_f = dft.get_fermi_level()\n"\
                	"E = e-e_f\n"\
                	"np.savetxt('{dos_txt}', d)\n"\
                	"np.savetxt('{e_txt}', E)\n"\
                	"plt.plot(d,E)\n"\
               		"plt.xlabel('energy [eV]')\n"\
                	"plt.ylabel('DOS')\n"\
                	"#plt.xlim(-10,4)\n"\
	                "#plt.ylim(-5,70)\n"\
			"plt.savefig('{plot_png}')\n"\
	                "\n"\
			.format(ads=ads,
				guest1=guest1,
				ecut=ecut,
				kpts=kpts,
				xc=xc,
				slab_txt='../txt/'+ filename +'_slab.txt',
				ads_txt='../txt/'+ filename +'_ads.txt',
				dos_txt='../pdos/'+ filename + '_dos.txt',
                        	e_txt='../pdos/'+ filename + '_e.txt',
                        	plot_png='../plot/'+ filename + '.png',))
			# Make slurm script
			with open('sl/' + filename + '.sl', 'w') as f:
				f.write("#!/bin/bash\n"\
			"\n"\
			"#SBATCH --job-name={filename}\n"\
			"#SBATCH --partition={partition}\n"\
			"#SBATCH --error={error}\n"\
			"#SBATCH --output={output}\n"\
			"#SBATCH --nodes={nodes}\n"\
			"#SBATCH --ntasks={ntasks}\n"\
			"#SBATCH --ntasks-per-core={ntasks_per_core}\n"\
			"#SBATCH --mem-per-cpu={mem_per_cpu}\n"\
			"module purge\n"\
			". '/groups/kemi/kabelkim/miniconda3/etc/profile.d/conda.sh'\n"\
			"conda activate gpaw2\n"\
			"export OMP_NUM_THREADS=1\n"\
			"export OMPI_MCA_pml='^ucx'\n"\
			"export OMPI_MCA_osc='^ucx'\n"\
			"mpirun gpaw python ../py/{filename}.py"\
			.format(filename=filename,
				partition=partition,
				error='../err/' + filename + '.err',
				output='../log/' + filename + '.log',
				nodes=nodes,
				ntasks=ntasks,
				ntasks_per_core=ntasks_per_core,
				mem_per_cpu=mem_per_cpu))

