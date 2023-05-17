#!/bin/python3

import sys
import os
import numpy as np
from time import sleep

# DFT parameters
xc = 'RPBE'
ecut = 400

# k-points to run over in turn to hopefully converge faster
kpts = (2,2,1)

# Cluster parameters
partition = 'katla_long'
nodes = 1
ntasks = 8
ntasks_per_core = 2
mem_per_cpu = 3000

os.system("mkdir sl")
os.system("mkdir py")
os.system("mkdir txt")
os.system("mkdir err")
os.system("mkdir log")

elements = ['V','Nb']
for i in range(1,4):
	for guest1 in elements:
		filename = str(i)+ '_' + guest1
		with open('py/' + filename + '.py', 'w') as f:
			f.write("from gpaw import GPAW, PW\n"\
			"from ase.io import Trajectory\n"\
			"from ase import Atoms\n"\
			"from ase.build import fcc111, add_adsorbate\n"\
			"from ase.constraints import FixAtoms, FixedLine\n"\
			"from ase.optimize import QuasiNewton\n"\
			"import numpy as np\n"\
			"\n"\
			"atoms = fcc111('Ta', size=(5,5,5), vacuum=7.5, a=3.31)\n"\
			"\n"\
			"for index in [atom.index for atom in atoms if atom.tag == {i}]:\n"\
			"	atoms[index].symbol = '{guest1}'\n"\
			"\n"\
			"atoms[112].symbol = 'Ta'\n"\
			"\n"\
			"calc = GPAW(mode=PW({ecut}),\n"\
			"		kpts={kpts},\n"\
			"		xc='{xc}',\n"\
			"		txt='{slab_txt}')\n"\
			"\n"\
			"atoms.set_calculator(calc)\n"\
			"atoms.get_potential_energy()\n"\
			"\n"\
			"OH = Atoms('OH',([0,0,0],[-0.063,0.866,0.311]))\n"\
			"add_adsorbate(atoms,OH,2.02,position=[8.5, 5])\n"\
			"calc = GPAW(mode=PW({ecut}),\n"\
			"		kpts={kpts},\n"\
			"		xc='{xc}',\n"\
			"		txt='{ads_txt}')\n"\
			"\n"\
			"atoms.set_calculator(calc)\n"\
			"atoms.get_potential_energy()\n"\
			"\n"\
			.format(i=i,
				guest1=guest1,
				ecut=ecut,
				kpts=kpts,
				xc=xc,
				slab_txt='../txt/'+ filename +'_slab.txt',
				ads_txt='../txt/'+ filename +'_ads.txt',))
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
			# Submit to slurm if 'submit' flag is given
			try:
			    	if sys.argv[1] == 'submit':
				        #sleep(1)
				        os.system("(cd sl/ && sbatch {})".format(filename + '.sl'))
			except IndexError:
				pass

