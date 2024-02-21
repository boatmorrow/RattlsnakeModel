## Installing PYSGFLOW in a virtual environment in VSCODE
These notes are for installing [PYSGFLOW](https://github.com/pygsflow/pygsflow) using a project specific .conda environement managed by VSCODE.  The changes for a general environment are small, and basically include creating your own named environement using conda, and updating that environment rather than the .conda local environment.

#### General Scientific Software Building Notes:
As you get into building and using open source scientific software, you'll have a bunch to learn, but basically there's three ways to make/install it.  

1. Use a package manager
2. Build from source
3. Find pre-made installers/binaries 

So, there's no package manager I know of for windows, but usually there are installers for many softwares for windows.  

For linux, you've already got one depending on your flavor.

For OSX, unless you feel strongly about Brew, in which case you already know enough about this.  Other wise [install Macports](https://www.macports.org/install.php).

### Install conda and VSCODE
You need at least [miniconda](https://docs.conda.io/projects/miniconda/en/latest/) (my favorite).  [VSCODE](https://code.visualstudio.com/) is downloadable for free on all OS's as far as I can tell.

### Create a project folder
This folder will contain your .conda env and should also house all your other files for the project.  Everything we do for the .conda env can be easily modified for a real user environment, which might be the better move as some point.

### Now Build the ENV
Here we'll build the env using a file named flopy_forge.yml, created by me 1/22/24.  First we should modify our .condarc to make sure conda-forge is the default channel.  This should probably give you better results for most scientific software packages anyways.

* Open (create if necessary) the file ~/.condarc , where ~ is your home directory.
* Add the following lines:

        channels:
          - conda-forge
          - defaults

* Create new conda environment using vscode.
    - command shift P on mac (something similiar on windows...) -> Python: Create Environment
    - now there a new conda envrionment with no name and path /path/to/project/folder/.conda

* Add the packages 
    - open a terminal in vscode.  The commands listed here are for a "nix" type terminal.  I'm pretty sure the conda commands should be the same for a windows machine, using the correct paths (i.e. C:\path\to\your\folder).
        - make sure the (.conda) environment is the active one in your terminal, should be, but make sure.

      conda env update -p /path/to/project/folder/.conda --file flopy_forge.yml

    - this should add all the needed packages except gsflow, which we'll add next.

### Now Install pyGSFLOW
pyGSFLOW is a python library for interacting with GSFLOW.  It utilizes Flopy, the library for interacting to MODFLOW.  We'll install the development version of pyGSFLOW, so we will need to clone the gsflow repository.  So, you need to have git installed.  [Installation Instructions for most OS's.](https://github.com/git-guides/install-git).

#### Clone the repo
* Make or cd to a directory where we'll download the repository to.
    - So, I have a directory ~/soft where I download all open source scientific software.  That makes it easy for me to find software I have added, and centralizes things.  I'd suggest something along these lines.  
    - If you already have something like this, change to that directory:

            cd /path/to/software/directory
        or
            dir C:\path\to\software\directory
   Y
    - If you don't have one make it:

            mkdir -p /path/to/software/directory
            cd /path/to/software/directory
        or
            
            dir C:\path\to\software\directory
        - the -p flag probably doesn't work on windows, so we'll have to figure that one out on the fly.
* Clone the pysflow git repository:
    - Make sure you are in your software directory.

            git clone https://github.com/pygsflow/pygsflow
    
    - You should now have a directory pygsflow in your software directory.

#### Install pysgsflow:
 - Make sure your desired conda environment is active!
 - Change into the pysgflow directory:

        cd pygsflow

    or 

        dir pygsflow

 - Install the dev version using pip:
            
            pip install .

* Check to make sure everything installed correctly:
    - change back your project folder:

            cd /path/to/project/folder
    
    - check for pygsflow:

            conda list | grep pygsflow
        
        - this command is nix specific, not sure how to do this in windows, but I think you use Select-String instead of grep. You can also* Check to make sure everything installed correctly:
    - change back your project folder:

            cd /path/to/project/folder
    
    - check for pygsflow:

            conda list | grep pygsflow
        
        - this command is nix specific, not sure how to do this in windows, but I think you use Select-String instead of grep. You can also just use "conda list", and look for pygsflow in the output.

### Install pymake (most useful for *nix machines)
This is a python program for downloading and compile most USGS subsurface codes.

  - Pymake requires a fortran compiler.  I use [gcc/gfortran](https://gcc.gnu.org/), which is available on all package managers. I think pymake only works easily for \*nix computers.  Windows users usually have to download pre-made binaries.

    - for mac osx
    
        sudo port install gcc13

- With our new .conda environment active:

       conda install mfpymake

This should add the pymake library to our python environment, and give use some command line utilities for downloading and compiling software for our machine.

#### Install MODFLOW 2005. 
MODFLOW 2005 is the first code we'll get started with.  This is the USGS written groundwater simulation software, written in FORTRAN.  This is the software that our python libraries are useful in helping develop and run input files, and for vizualizing the output.  

* Make a new directory in your software folder called MODFLOW or something like it.  Here we will download and install the different versions of MODFLOW that we need.  

      cd MODFLOW

* now use pymake to dowload and install MODFLOW 2005.  This requires an internet connection:

        make-program mf2005 -fc=gfortran --fflags='-O3'

- This utility program will download the source code for the internet and compile it using your system compiler, so it requires an internet connection. After it completes you will have an exectuable named mf2005, which is the modflow 2005 program.  This program is what will be needed to run modflow simulations. the exectuable needs to be in the system PATH.  In other words, it either needs to be in a location the sytem knows to search (e.g. /usr/local/bin) or needs to be copied into any directory you trying to run model in, or you can add the current location to your PATH. The utility can download and build almost any USGS subsurface software.  Its pretty rad.  

- We are now ready to begin simulating and analyzing groundwater flow problems. 

### Getting started with FLOPY
I have written a tutorial which uses Flopy and MODFLOW 2005 to simulate the results of Toth 1962.  You can get the entire repository by navigating to a directory where you like the repostiroy to reside, and then clone with git using:

    git clone https://github.com/boatmorrow/FlopyTothDemo

### Installing GSFLOW
As of Jan 2024, pymake doesn't have the ability to make gsflow.  Not sure what's going on here, but there two options for installing GSFLOW right now.  For windows and linux users there are precompiled binaries.  For OSX, we'll have to make from source.  Either way you need to download the software for [GSFLOW](https://www.usgs.gov/software/gsflow-coupled-groundwater-and-surface-water-flow-model)

* For windows/linux users download the latest version for your OS.  Put the binary in your software folder under the name GSFLOW.  It needs to be in the PATH like MF2005.

* For mac users, you need to have cmake.  Chances are you already have it, try:

       which make

If it returns a folder you're good.  If not:

      sudo port install cmake

* Download the linux distribution and upack in the software/GSLOW directory

      cd software/GSFLOW/gsflow_linux_2.3.0/src
      make all

A bunch of output and some minutes later, fingers crossed, you should have gsflow installed in software/GSFLOW/gsflow_linux_2.3.0/bin/
