import glob, os, re, sys
import numpy as np

# Cluster parameters
partition = 'katla_day'
nodes = 1
ntasks = 8
ntasks_per_core = 2
mem_per_cpu = 3000

dirs1 = '/home/theoretical_catalysis/kabelkim/Desktop/masterproject/HCP_vs_FCC/vector_effect/FCC/py'
for filename in sorted(os.listdir(dirs1)):
    with open('sl/' + filename.split(".")[0] + '.sl', 'w') as f:
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
        "mpirun gpaw python ../py/{filename}"\
        .format(filename=filename,
        partition=partition,
        error='../err/' + filename.split(".")[0] + '.err',
        output='../log/' + filename.split(".")[0] + '.log',
        nodes=nodes,
        ntasks=ntasks,
        ntasks_per_core=ntasks_per_core,
        mem_per_cpu=mem_per_cpu))    
