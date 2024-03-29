
Installation
============

Get a copy of Neuroptimus
----------------------------------

Install `git` and type:


    git clone https://github.com/KaliLab/neuroptimus.git



Dependencies
-------------

The following python libraries are required:
  - python
  - numpy 
  - eFEL
  - matplotlib 

The following libraries are recommended:
  - neuron
  - scipy 
  - PyQt5
  - inspyred 
  - pyelectro
  - Pygmo
  - bluepyopt
  - ipyparallel
  - nest
  
You can get required or recommended libraries with the following command:

  
    pip install -r requirements_minimal.txt

or

    pip install -r requirements_full.txt

You can get individual package with `pip`:
    
    pip install neuron

    
Build documentation
-------------------

If you should require a local copy of the Neuroptimus documentation, you need a working install of
Sphinx, then run the command:


    sphinx-build ./doc <local build directory>

from the top-level neuroptimus directory where <local build directory>
should be replaced with a custom filepath.

Test Platforms
--------------

The package was tested on the following systems:

    1. Ubuntu 22.04.1 LTS
    2. Ubuntu 20.04.6 LTS 
    3. Fedora release 32 (Thirty Two) (neurofedora)

