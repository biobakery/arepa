======================================================
ARepA: Automated Repository Acquisition 
======================================================

---------------------------------------------------------
User Manual, Version x.x
---------------------------------------------------------

Authors 
 Yo S. Moon, Dr. Levi Waldron, 
 Dr. Daniela Boernigen, Dr. Curtis Huttenhower

Maintainer
 Yo S. Moon <jmoon@hsph.harvard.edu> 

Lincese
 x.x

URL
 http://huttenhower.org/arepa 

Chapter 0 Installation 
============================================

Section 1.1 Supported Operating Systems 
--------------------------------------------
The following platform(s) are supported:

* Linux 
* Mac OS X

The following platform(s) have NOT been tested:

* Windows Cygwin 

Section 1.2 Prerequisites 
--------------------------------------------

* Python > 2.7 
* SCons 
* R > x.x with Bioconductor
* Mercurial Source Control Management (Recommended) 

You can retrieve a copy of ARepA via mercurial: ::

$ hg clone https://bitbucket.org/chuttenh/arepa

Section 1.3 Setting up the Path 
--------------------------------------------

Once you have cloned arepa into a local directory, you must set up the correct UNIX paths. 
While in the root level in arepa, set the path by typing ::

$ export PATH= `pwd`/src:$PATH
$ export PYTHONPATH=`pwd`/src:$PYTHONPATH 

Section 1.4 Running the Build 
---------------------------------------------

It is *crucial* that you compile the GeneMapper module *prior* to running the build in its entirety. 
Compilation of GeneMapepr can be done by running the SConstruct file in the GeneMapper directory. ::

$ cd GeneMapper
$ scons 

The entirety of the ARepA pipeline can be run with the execution of a simple command in terminal ::

$ scons 

Chapter 2 Overview
============================================

.. image:: figure1.pdf
  :height: 300
  :width: 400
  :scale: 50
  :alt: Entity Diagram of ARepA  

Chapter 3 Structure 
============================================

Chpater 4 Modules 
============================================

Chapter 5 Advanced Topics 
============================================ 

Section 5.1 Testing ARepA 
--------------------------------------------

ARepA has a built-in unit testing script, located in the main **src** directory. 
While in the root directory, type ::

$ python src/test.py 

The default behavior of the testing script assumes that the entire build of ARepA is completed *prior* to running the script. If this is not the case, one can pass the optional argument "scons" to the test script and scons will be called in each submodule before the targets are checked. This method is error-prone and time-intensive and is not recommended. ::

$ python test.py scons 
 


Chapter 6 Frequently Asked Questions 
============================================

Chapter 7 Acknowledgements 
============================================ 




