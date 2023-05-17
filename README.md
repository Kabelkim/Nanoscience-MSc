![image](https://github.com/Kabelkim/Nanoscience-MSc/assets/65853425/383d9278-3008-4f4a-ad05-85883782259c)
# Adsorption energy calculated with DFT
Welcome to this Github page, describing the algorithms and storing the Python code used to generate data in Joakim Lajer's master project. 

## Description

The algorithms were used as part of the master thesis "Investigation of adsorption energies in phase-separated alloys." They utilize GPAW and ASE liberies in python, and are run as jobs on a high-performance cluster at the University of copenhagen. 


### DFT parameters

```
# DFT parameters
xc = <functional>
ecut = <eV>
kpts = <(x,x,x)>
```

### Building atomic system

```
atoms = <crystal-class>(<atom>,<size>,<vacuum>,<lattice-parameter>)
```


### Phase seperating the alloys
```
for index in [atom.index for atom in atoms if atom.tag == <x>]:
    atoms[index].symbol = '<guest-atom>'
```

### Attaching adsorbate

```
adsorbate = Atoms(<adsorbate-atom>,(<[x,x,x]>,<[x,x,x]>))
add_adsorbate(atoms,adsorbate,<hight>,position=[<x-coordinate>,<y-coordinate>])
```

### Performing DFT calculation

```
calc = GPAW(mode=PW({ecut}),
            kpts={kpts},
            xc='{xc}',
            txt='{<output-file>}')

atoms.set_calculator(calc)
atoms.get_potential_energy()
```

### Cluster parameters

```
partition = <partion>
nodes = <x>
ntasks = <x>
ntasks_per_core = <x>
mem_per_cpu = <mb>
```

### Formatting cluster scripts

```
#SBATCH --job-name={<filename>}
#SBATCH --partition={partition}
#SBATCH --error={<error-file>}
#SBATCH --output={<output-file>}
#SBATCH --nodes={nodes}
#SBATCH --ntasks={ntasks}
#SBATCH --ntasks-per-core={ntasks_per_core}
#SBATCH --mem-per-cpu={mem_per_cpu}
```

### Dependencies
For the dependencies, look at section **Appendices B Anaconda enviroment list**.


### Executing

The python files are directly executed on the HPC database, where all the submission files are created and can be executed directly.

## Authors

Contributors' names and contact info:

Joakim Lajer (gpw395@alumni.ku.dk)

## Version History

* 0.1
    * Initial Release (lite version)

## License

This project is licensed under the GNU General Public License v3.0, January 2004 - see the [LICENSE](https://github.com/Kabelkim/phase-splitter/blob/main/LICENSE) file for details.
