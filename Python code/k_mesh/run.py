#!/bin/python3

import sys
import os
import numpy as np
from time import sleep

# DFT parameters
xc = 'RPBE'
ecut = 400

# k-points to run over in turn to hopefully converge faster
#kpts = (4,4,1)

# Cluster parameters
partition = 'katla_day'
nodes = 1
ntasks = 8
ntasks_per_core = 2
mem_per_cpu = 3000	

os.system("mkdir sl")
os.system("mkdir py")
os.system("mkdir txt")
os.system("mkdir err")
os.system("mkdir log")

elements = ['Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn']
mesh = [(2,2,1),(3,3,1),(4,4,1),(8,8,1)]
for kpoints in mesh:
	for guest1 in elements:
		filename = 'hcp_'+ str(kpoints[0]) + '_' + guest1
		with open('py/' + filename + '.py', 'w') as f:
			f.write("from gpaw import GPAW, PW\n"\
			"from ase.io import Trajectory\n"\
			"from ase import Atoms\n"\
			"from ase.build import hcp0001, add_adsorbate\n"\
			"from ase.constraints import FixAtoms, FixedLine\n"\
			"from ase.optimize import QuasiNewton\n"\
			"import numpy as np\n"\
			"\n"\
			"atoms = hcp0001('Pt', size=(3,3,3), vacuum=7.5, a=3.993/2**0.5)\n"\
			"\n"\
			"atoms[22].symbol = '{guest1}'\n"\
			"\n"\
			"calc = GPAW(mode=PW({ecut}),\n"\
			"		kpts={kpoints},\n"\
			"		xc='{xc}',\n"\
			"		txt='{slab_txt}')\n"\
			"\n"\
			"atoms.set_calculator(calc)\n"\
			"atoms.get_potential_energy()\n"\
			"\n"\
			"add_adsorbate(atoms,'N',2.02,position=[4.25, 2.5])\n"\
			"calc = GPAW(mode=PW({ecut}),\n"\
			"		kpts={kpoints},\n"\
			"		xc='{xc}',\n"\
			"		txt='{ads_txt}')\n"\
			"\n"\
			"atoms.set_calculator(calc)\n"\
			"atoms.get_potential_energy()\n"\
			"\n"\
			.format(guest1=guest1,
				ecut=ecut,
				kpoints=kpoints,
				xc=xc,
				slab_txt='../txt/' + filename + '_slab.txt',
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
