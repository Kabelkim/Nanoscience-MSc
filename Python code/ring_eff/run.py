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
partition = 'katla_day'
nodes = 1
ntasks = 8
ntasks_per_core = 2
mem_per_cpu = 2500

os.system("mkdir sl")
os.system("mkdir py")
os.system("mkdir txt")
os.system("mkdir err")
os.system("mkdir log")


element = np.array(['Sc','Ti','V','Fe','Co','Ni','Cu','Zn','Ru','Rh','Pd','Ag','Ta','W','Re','Au'])

#Ring2 atoms
for i in [82,83,87]:
	for guest1 in element:
		filename = 'ring2_pos_'+str(i)+'_' + guest1.lower()
		with open('py/' + filename + '.py', 'w') as f:
			f.write("from gpaw import GPAW, PW\n"\
			"from ase.io import Trajectory\n"\
			"from ase import Atoms\n"\
			"from ase.build import hcp0001, add_adsorbate\n"\
			"from ase.constraints import FixAtoms, FixedLine\n"\
			"from ase.optimize import QuasiNewton\n"\
			"import numpy as np\n"\
		        "\n"\
			"atoms = hcp0001('Pt', size=(5,5,5), vacuum=7.5, a=3.993/2**0.5)\n"\
		        "\n"\
			"atoms[{i}].symbol = '{guest1}'\n"\
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
			"\n"\
			"calc = GPAW(mode=PW({ecut}),\n"\
			"               kpts={kpts},\n"\
			"               xc='{xc}',\n"\
			"               txt='{ads_txt}')\n"\
			"\n"\
			"atoms.set_calculator(calc)\n"\
			"atoms.get_potential_energy()\n"\
			"\n"\
			.format(guest1=guest1,
				i=i,
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
###############################################################################################################################################################################################################
#Ring2

for guest1 in element:
	filename = 'ring2_' + guest1.lower()
	with open('py/' + filename + '.py', 'w') as f:
		f.write("from gpaw import GPAW, PW\n"\
		"from ase.io import Trajectory\n"\
		"from ase import Atoms\n"\
		"from ase.build import hcp0001, add_adsorbate\n"\
		"from ase.constraints import FixAtoms, FixedLine\n"\
		"from ase.optimize import QuasiNewton\n"\
		"import numpy as np\n"\
	        "\n"\
		"atoms = hcp0001('Pt', size=(5,5,5), vacuum=7.5, a=3.993/2**0.5)\n"\
	        "\n"\
		"atoms[82].symbol = '{guest1}'\n"\
		"atoms[83].symbol = '{guest1}'\n"\
		"atoms[87].symbol = '{guest1}'\n"\
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
		"\n"\
		"calc = GPAW(mode=PW({ecut}),\n"\
		"               kpts={kpts},\n"\
		"               xc='{xc}',\n"\
		"               txt='{ads_txt}')\n"\
		"\n"\
		"atoms.set_calculator(calc)\n"\
		"atoms.get_potential_energy()\n"\
		"\n"\
		.format(guest1=guest1,
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

###############################################################################################################################################################################################################
#Ring3 atoms
for i in [57,58,61,62,66,67,63]:
	for guest1 in element:
		filename = 'ring3_pos_'+str(i)+'_' + guest1.lower()
		with open('py/' + filename + '.py', 'w') as f:
			f.write("from gpaw import GPAW, PW\n"\
			"from ase.io import Trajectory\n"\
			"from ase import Atoms\n"\
			"from ase.build import hcp0001, add_adsorbate\n"\
			"from ase.constraints import FixAtoms, FixedLine\n"\
			"from ase.optimize import QuasiNewton\n"\
			"import numpy as np\n"\
		        "\n"\
			"atoms = hcp0001('Pt', size=(5,5,5), vacuum=7.5, a=3.993/2**0.5)\n"\
		        "\n"\
			"atoms[{i}].symbol = '{guest1}'\n"\
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
			"\n"\
			"calc = GPAW(mode=PW({ecut}),\n"\
			"               kpts={kpts},\n"\
			"               xc='{xc}',\n"\
			"               txt='{ads_txt}')\n"\
			"\n"\
			"atoms.set_calculator(calc)\n"\
			"atoms.get_potential_energy()\n"\
			"\n"\
			.format(guest1=guest1,
				i=i,
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

###############################################################################################################################################################################################################
#Ring3

for guest1 in element:
	filename = 'ring3_' + guest1.lower()
	with open('py/' + filename + '.py', 'w') as f:
		f.write("from gpaw import GPAW, PW\n"\
		"from ase.io import Trajectory\n"\
		"from ase import Atoms\n"\
		"from ase.build import hcp0001, add_adsorbate\n"\
		"from ase.constraints import FixAtoms, FixedLine\n"\
		"from ase.optimize import QuasiNewton\n"\
		"import numpy as np\n"\
	        "\n"\
		"atoms = hcp0001('Pt', size=(5,5,5), vacuum=7.5, a=3.993/2**0.5)\n"\
	        "\n"\
		"atoms[57].symbol = '{guest1}'\n"\
		"atoms[58].symbol = '{guest1}'\n"\
		"atoms[61].symbol = '{guest1}'\n"\
		"atoms[63].symbol = '{guest1}'\n"\
		"atoms[66].symbol = '{guest1}'\n"\
		"atoms[67].symbol = '{guest1}'\n"\
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
		"\n"\
		"calc = GPAW(mode=PW({ecut}),\n"\
		"               kpts={kpts},\n"\
		"               xc='{xc}',\n"\
		"               txt='{ads_txt}')\n"\
		"\n"\
		"atoms.set_calculator(calc)\n"\
		"atoms.get_potential_energy()\n"\
		"\n"\
		.format(guest1=guest1,
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
###############################################################################################################################################################################################################
#Ring3 with mid

for guest1 in element:
	filename = 'ring3_mid_' + guest1.lower()
	with open('py/' + filename + '.py', 'w') as f:
		f.write("from gpaw import GPAW, PW\n"\
		"from ase.io import Trajectory\n"\
		"from ase import Atoms\n"\
		"from ase.build import hcp0001, add_adsorbate\n"\
		"from ase.constraints import FixAtoms, FixedLine\n"\
		"from ase.optimize import QuasiNewton\n"\
		"import numpy as np\n"\
	        "\n"\
		"atoms = hcp0001('Pt', size=(5,5,5), vacuum=7.5, a=3.993/2**0.5)\n"\
	        "\n"\
		"atoms[57].symbol = '{guest1}'\n"\
		"atoms[58].symbol = '{guest1}'\n"\
		"atoms[61].symbol = '{guest1}'\n"\
		"atoms[62].symbol = '{guest1}'\n"\
		"atoms[63].symbol = '{guest1}'\n"\
		"atoms[66].symbol = '{guest1}'\n"\
		"atoms[67].symbol = '{guest1}'\n"\
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
		"\n"\
		"calc = GPAW(mode=PW({ecut}),\n"\
		"               kpts={kpts},\n"\
		"               xc='{xc}',\n"\
		"               txt='{ads_txt}')\n"\
		"\n"\
		"atoms.set_calculator(calc)\n"\
		"atoms.get_potential_energy()\n"\
		"\n"\
		.format(guest1=guest1,
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

###############################################################################################################################################################################################################
#layer2 atoms
for i in range(75,100):
	for guest1 in element:
		filename = 'layer_2_pos_'+str(i)+'_' + guest1.lower()
		with open('py/' + filename + '.py', 'w') as f:
			f.write("from gpaw import GPAW, PW\n"\
			"from ase.io import Trajectory\n"\
			"from ase import Atoms\n"\
			"from ase.build import hcp0001, add_adsorbate\n"\
			"from ase.constraints import FixAtoms, FixedLine\n"\
			"from ase.optimize import QuasiNewton\n"\
			"import numpy as np\n"\
		        "\n"\
			"atoms = hcp0001('Pt', size=(5,5,5), vacuum=7.5, a=3.993/2**0.5)\n"\
		        "\n"\
			"atoms[{i}].symbol = '{guest1}'\n"\
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
			"\n"\
			"calc = GPAW(mode=PW({ecut}),\n"\
			"               kpts={kpts},\n"\
			"               xc='{xc}',\n"\
			"               txt='{ads_txt}')\n"\
			"\n"\
			"atoms.set_calculator(calc)\n"\
			"atoms.get_potential_energy()\n"\
			"\n"\
			.format(guest1=guest1,
				i=i,
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

###############################################################################################################################################################################################################
#layer2

for guest1 in element:
	filename = 'layer_2_' + guest1.lower()
	with open('py/' + filename + '.py', 'w') as f:
		f.write("from gpaw import GPAW, PW\n"\
		"from ase.io import Trajectory\n"\
		"from ase import Atoms\n"\
		"from ase.build import hcp0001, add_adsorbate\n"\
		"from ase.constraints import FixAtoms, FixedLine\n"\
		"from ase.optimize import QuasiNewton\n"\
		"import numpy as np\n"\
	        "\n"\
		"atoms = hcp0001('Pt', size=(5,5,5), vacuum=7.5, a=3.993/2**0.5)\n"\
	        "\n"\
		"for index in [atom.index for atom in atoms if atom.tag == 2]:\n"\
		"	atoms[index].symbol = '{guest1}'\n"\
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
		"\n"\
		"calc = GPAW(mode=PW({ecut}),\n"\
		"               kpts={kpts},\n"\
		"               xc='{xc}',\n"\
		"               txt='{ads_txt}')\n"\
		"\n"\
		"atoms.set_calculator(calc)\n"\
		"atoms.get_potential_energy()\n"\
		"\n"\
		.format(guest1=guest1,
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

###############################################################################################################################################################################################################
#layer3 atoms
for i in range(50,75):
	for guest1 in element:
		filename = 'layer_3_pos'+str(i)+'_' + guest1.lower()
		with open('py/' + filename + '.py', 'w') as f:
			f.write("from gpaw import GPAW, PW\n"\
			"from ase.io import Trajectory\n"\
			"from ase import Atoms\n"\
			"from ase.build import hcp0001, add_adsorbate\n"\
			"from ase.constraints import FixAtoms, FixedLine\n"\
			"from ase.optimize import QuasiNewton\n"\
			"import numpy as np\n"\
		        "\n"\
			"atoms = hcp0001('Pt', size=(5,5,5), vacuum=7.5, a=3.993/2**0.5)\n"\
		        "\n"\
			"atoms[{i}].symbol = '{guest1}'\n"\
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
			"\n"\
			"calc = GPAW(mode=PW({ecut}),\n"\
			"               kpts={kpts},\n"\
			"               xc='{xc}',\n"\
			"               txt='{ads_txt}')\n"\
			"\n"\
			"atoms.set_calculator(calc)\n"\
			"atoms.get_potential_energy()\n"\
			"\n"\
			.format(guest1=guest1,
				i=i,
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

###############################################################################################################################################################################################################
#layer3

for guest1 in element:
	filename = 'layer_3_' + guest1.lower()
	with open('py/' + filename + '.py', 'w') as f:
		f.write("from gpaw import GPAW, PW\n"\
		"from ase.io import Trajectory\n"\
		"from ase import Atoms\n"\
		"from ase.build import hcp0001, add_adsorbate\n"\
		"from ase.constraints import FixAtoms, FixedLine\n"\
		"from ase.optimize import QuasiNewton\n"\
		"import numpy as np\n"\
	        "\n"\
		"atoms = hcp0001('Pt', size=(5,5,5), vacuum=7.5, a=3.993/2**0.5)\n"\
	        "\n"\
		"for index in [atom.index for atom in atoms if atom.tag == 3]:\n"\
		"	atoms[index].symbol = '{guest1}'\n"\
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
		"\n"\
		"calc = GPAW(mode=PW({ecut}),\n"\
		"               kpts={kpts},\n"\
		"               xc='{xc}',\n"\
		"               txt='{ads_txt}')\n"\
		"\n"\
		"atoms.set_calculator(calc)\n"\
		"atoms.get_potential_energy()\n"\
		"\n"\
		.format(guest1=guest1,
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


