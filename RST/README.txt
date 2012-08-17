======================================================
ARepA: Automated Repository Acquisition 
======================================================

---------------------------------------------------------
User Manual, Version 0.9.0a 
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

Citation 
 Yo S. Moon, Levi Waldron, Daniela Boernigen, and Curtis Huttenhower. "ARepA: Automated Repository Acqusition", Nucleic Acids Research, xxxxxxx (Submitted) 

Chapter 0 Installation 
============================================

Section 0.1 Supported Operating Systems 
--------------------------------------------
The following platform(s) are supported:

* Linux 
* Mac OS X

The following platform is NOT supported:

* Windows 

The following platform(s) have NOT been tested:

* Windows Cygwin 

Section 0.2 Prerequisites 
--------------------------------------------

* Python (ver >= 2.7.1) 
* SCons (ver >= 2.1.0)  
* Sleipnir Library for Computational Functional Genomics [1]
* R (ver >= 2.13.1) with Bioconductor package, permission to download new libraries 
* Mercurial Source Control Management (Recommended) 

You can retrieve a copy of ARepA via mercurial: ::

$ hg clone https://bitbucket.org/chuttenh/arepa

or by downloading a tarball from the huttenhower website ::

$ wget http://huttenhower.org/arepa/arepa_stable.tar.gz

Section 0.3 Setting up the Path 
--------------------------------------------

Once you have cloned arepa into a local directory, you must set up the correct UNIX paths. 
While in the root level in arepa, set the path by typing ::

$ export PATH=`pwd`/src:$PATH
$ export PYTHONPATH=`pwd`/src:$PYTHONPATH 

Section 0.4 Running the Build 
---------------------------------------------

It is *crucial* that you compile the GeneMapper module *prior* to running the build in its entirety. 
Compilation of GeneMapepr can be done by running the SConstruct file in the GeneMapper directory. ::

$ cd GeneMapper
$ scons 

The entirety of the ARepA pipeline can be run with the execution of a simple command in terminlal. In the root directory of arepa, type ::

$ scons 

Chapter 1 Overview
============================================
ARepA was designed to be a simple command-line interface 
combining programmatic automation with an integrated data management tool 
that consolidates eclectic data from heterogeneous sources into a 
consistent, easily manipulable format. It was written with the Python programming 
language under the SCons software construction tool for dependency-tracking and 
automation. 

1.1 Design 
--------------------------------------------

1.2 SCons
--------------------------------------------

1.3 Features 
--------------------------------------------


Chapter 2 Structure 
============================================

.. image:: figure1.pdf
  :height: 300
  :width: 400
  :scale: 50
  :alt: Entity Diagram of ARepA  


1. SConstruct (SConscript) 
2. data 
3. src 
4. tmp
5. etc 
6. doc 

Chpater 3 Modules 
============================================

There are two types of modules: **internal modules**, and 
**external modules**. Internal modules do actual downloading and processing 
of data/metadata from public repositoires; external modules serve 
global helper functions, such as gene identifier conversion, and R package 
generation. Currently there are 3 external modules:

1. RST - generate documentation from source
2. Package - export R package 
3. GeneMapper - converts gene identifiers into common format 

Now, we describe the internal modules, which can be subsequently 
divided into two broad categories: gene expression/co-expression, 
and interaction networks.  

Gene Expression/Gene co-expression 
--------------------------------------------
1. Gene Expression Omnibus 

Interaction Networks 
--------------------------------------------
1. Bacteriome 
2. RegulonDB
3. IntAct
4. MPIDB 
5. BioGrid
6. STRING 


Chapter 4 Advanced Topics 
============================================ 

Section 4.1 Testing ARepA 
--------------------------------------------

ARepA has a built-in unit testing script, located in the main **src** directory. 
While in the root directory, type ::

$ python src/test.py 

The default behavior of the testing script assumes that the entire build of ARepA is completed *prior* to running the script. If this is not the case, one can pass the optional argument "scons" to the test script and scons will be called in each submodule before the targets are checked. This method is error-prone and time-intensive and is not recommended. ::

$ python test.py scons 

Section 4.2 Running Modules Separately 
---------------------------------------------

After the taxonomic information has been downloaded
and processed by the parent node in arepa ("arepa/tmp/taxids" have been built),
one can launch any internal module separately by going into a desired directory and launching "scons". For instance, if one wants to run GEO, one would type (assuming starting from the root directory) ::

$ cd GEO
$ scons 


Chapter 5 Frequently Asked Questions 
============================================

NB: All questions should be directed to jmoon@hsph.harvard.edu.

1. I get the following error when I run ARepA

	ImportError: No module named arepa

*Solution*
 Make sure you add the **src** directory of ARepA's root level to both the bash path and the python path variables. 

2. I get the following error when I run ARepA

	ImportError: No module named sfle

*Solution*
 See above 

3. GeneMapping is not working!

*Solution*
 Make sure you *compile* GeneMapper prior to running ARepA. This can be done by launching an SCons call within the "GeneMapper" module. 

4. Where can I find configuration information for my pipelines?

*Solution*
 All configuration information is in the **etc** folder of every directory. See the chapter on specific modules for more details on configuration information for a particualr repository. 

5. How do I cite ARepA? 


Chapter 6 Acknowledgements 
============================================ 

The authors would like to thank Larissa Miropolsky. 

References
=============================================
