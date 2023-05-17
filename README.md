![image](https://github.com/Kabelkim/Nanoscience-MSc/assets/65853425/a6878964-df5c-4045-bc2a-ccf0023f3481)

# Adsorption energy calculated with DFT
This repository contains a description of Density Functional Theory (DFT) and the algorithms used in the master thesis "Investigation of adsorption energies in phase-separated alloys." (The Python files can be found in [CODE](https://github.com/Kabelkim/Nanoscience-MSc/tree/main/Python%20code)). They utilize GPAW and ASE libraries in Python and are run as jobs on a high-performance cluster at the University of Copenhagen. 

## What is DFT?
DFT is a quantum mechanical method used to study the electronic structure of atoms, molecules, and solids. It provides a powerful approach to investigating various properties such as energy, structure, and bonding in materials.

## GPAW
GPAW is an open-source software package that implements DFT calculations using real-space grids and projector-augmented wave method. It offers efficient and accurate simulations of materials by combining the advantages of both plane wave and localized basis set methods.

## Description
### DFT parameters
Understanding the DFT parameters used in GPAW is essential for obtaining reliable and meaningful results.
```
xc = <functional>
ecut = <eV>
kpts = <(x,x,x)>
```
- Exchange-Correlation Functionals (xc): Different functionals such as RPBE and DFT-D3 can be selected to describe the exchange-correlation energy in GPAW.

- Energy Cutoff (ecut): The energy cutoff determines the maximum kinetic energy of the plane waves used to represent the electronic wavefunctions. It is an important parameter to balance accuracy and computational cost.

- k-point sampling (kpts): GPAW utilizes k-point sampling to discretize the Brillouin zone and perform calculations on a finite set of k-points. The choice of k-point mesh affects the accuracy and computational efficiency of the calculations.

### Building atomic system
GPAW utilizes the Atomic Simulation Environment (ASE) library to build and manipulate atomic structures. 
```
atoms = <crystal-class>(<atom>,<size>,<vacuum>,<lattice-parameter>)
```
- Crystal class: The crystal class refers to the symmetry group of a crystal structure. It describes the arrangement of atoms in the crystal lattice and determines its overall symmetry. Examples of the crystal classes include HCP and FCC, which are implemented throughout the algorithms.

- Atom: The atom refers to the individual chemical element present in the crystal structure. It can be represented by its chemical symbol, such as H for hydrogen, O for oxygen, and so on.

- Size: The size of the crystal refers to its dimensions or extent in space. It can be specified in terms of length, width, and height.

- Vacuum: The vacuum, in the context of crystal structures, refers to the space between periodic replicas of the crystal lattice. It is often included to prevent interactions between periodic images and simulate an isolated system. The vacuum size can affect the accuracy of calculations and is typically chosen to be large enough to minimize interactions between periodic images.

- Lattice parameter: the lattice parameter refers to the length of the edges of the unit cell in a crystal structure. In the algorithms used, it is denoted by the symbol a, describing the unit cell length. 

### Phase separating the alloys
To manipulate atoms in ASE, including layer-phase separated alloys, you can follow these steps:
```
for index in [atom.index for atom in atoms if atom.tag == <x>]:
    atoms[index].symbol = '<guest-atom>'
```
Here the atoms in the indices in the layer are denoted in "atom.tag == <x>", where x represents the layer. Then guest atoms will be inserted in the positions in that layer, the code can be combined with a list containing different guest elements, thus producing many calculations. 

### Attaching adsorbate
To attach an adsorbate to the alloy surface, the following part can be implemented:
 
```
adsorbate = Atoms(<adsorbate-atom>,(<[x,x,x]>,<[x,x,x]>))
add_adsorbate(atoms,adsorbate,<hight>,position=[<x-coordinate>,<y-coordinate>])
```
This gives access to study the interactions and properties of the adsorbate on the surface.
    
### Performing DFT calculation
To perform a DFT calculation using GPAW, these steps are necessary:
```
calc = GPAW(mode=PW({ecut}),
            kpts={kpts},
            xc='{xc}',
            txt='{<output-file>}')

atoms.set_calculator(calc)
atoms.get_potential_energy()
```
The calc descriptor uses the input from earlier and combines them. Then the DFT is using these parameters and calculates the desired outcome, in this case, the potential energies. It is crucial to perform the DFT calculation before and after attaching the adsorbate to get information about the interactions. 

### Cluster parameters
To run DFT calculations using GPAW on a high-performance cluster, several key parameters needs to be considered. These parameters help allocate computational resources efficiently and optimize the execution of the DFT calculations. 
```
partition = <partion>
nodes = <x>
ntasks = <x>
ntasks_per_core = <x>
mem_per_cpu = <mb>
```
- partition: The partition refers to the specific subset of resources or compute nodes on the cluster dedicated to the job. Different partitions may have varying properties, such as the number of cores, memory capacity, or run time limits. 

- nodes: Nodes are individual computational units within a cluster. Each node typically contains multiple cores or processors that can run parallel tasks. 

- ntasks: The ntasks parameter determines the total number of tasks or processes that will be executed on the allocated nodes.
    
- ntasks_per_core: It specifies the number of tasks assigned to each core or processor within a node. It helps optimize the load balance across cores and can impact the performance of the calculations. 

- mem_per_cpu: Memory per cpu defines the amount of memory allocated per CPU or core. It is crucial to allocate sufficient memory to avoid memory-related errors during the DFT calculations. 
    
### Formatting cluster scripts
When submitting DFT calculations on a high-performance cluster, it is important to format the cluster scripts correctly. These scripts contain directives that define the desired configuration and execution parameters for the job.
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
This is formatted with the parameters listed earlier and helps the calculations run as smoothly as possible.
    
### Dependencies
For the dependencies, look at section **Appendices B Anaconda environment list** in the thesis.


### Executing

The Python files are directly executed on the HPC database, where all the submission files are created and can be executed directly.

## Authors

Contributors' names and contact info:

Joakim Lajer (gpw395@alumni.ku.dk)

## Version History

* 0.1
    * Initial Release (lite version)

## License

This project is licensed under the GNU General Public License v3.0, January 2004 - see the [LICENSE](https://github.com/Kabelkim/Nanoscience-MSc/blob/main/LICENSE) file for details.
