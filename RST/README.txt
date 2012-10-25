======================================================
ARepA: Automated Repository Acquisition 
======================================================

---------------------------------------------------------
User Manual, Version 0.9.1 
---------------------------------------------------------

Authors 
 Yo S. Moon, Dr. Levi Waldron, 
 Dr. Daniela Boernigen, Dr. Curtis Huttenhower

Maintainer
 Yo S. Moon <jmoon@hsph.harvard.edu> 

Lincese
 MIT Open License

URL
 http://huttenhower.org/arepa 

Citation 
 Yo S. Moon, Levi Waldron, Daniela Boernigen, and Curtis Huttenhower. "ARepA: Automated Repository Acqusition", Nucleic Acids Research 

Chapter 0 Getting Started 
============================================

Section 0.1 Supported Operating Systems 
--------------------------------------------
ARepA was fully tested on and is supported by the following platform(s) 

* Linux 
* Mac OS X

The following platform is NOT supported:

* Windows 

The following platform(s) have NOT been tested:

* Windows Cygwin 

It is highly recommended that ARepA is run on a Linux cluster rather than on a local machine.
Certain processes (such as missing value imputation and functional network construction for 
GEO) can be extremely CPU-intensive and is not suitable for laptop set-ups. 

Section 0.2 Software Prerequisites 
--------------------------------------------

Before downloading ARepA, you should have the following software on your machine:

* Python (ver >= 2.7.1) 
* SCons (ver >= 2.1.0)  
* Sleipnir Library for Computational Functional Genomics [1]
* R (ver >= 2.13.1) with Bioconductor package, permission to download new libraries
* Java SE 6 (ver >= 1.6.0)
* Mercurial Source Control Management (Recommended) 


Section 0.3 Downloading ARepa 
------------------------------------------------

You can retrieve a copy of ARepA via mercurial (Recommended): ::

$ hg clone https://bitbucket.org/chuttenh/arepa

or by downloading a tarball from the huttenhower website ::

$ wget http://huttenhower.org/arepa/arepa_stable.tar.gz


Section 0.4 Setting up the Path 
--------------------------------------------

Once you have cloned arepa into a local directory, you must set up the correct UNIX paths
so that the necessary files in ARepA are recognized by your system. 
 
While in the root level in arepa, set the path by typing ::

$ export PATH=`pwd`/src:$PATH
$ export PYTHONPATH=`pwd`/src:$PYTHONPATH 

This command adds the main source directory to both the UNIX path for the bash shell and the environmental path forPython. 

Section 0.5 Compiling Necessary Components  
---------------------------------------------

It is *crucial* that you compile the GeneMapper module *prior* to running the build in its entirety. 
Compilation of GeneMapepr can be done by running the SConstruct file in the GeneMapper directory. Starting at the root directory, type ::

$ cd GeneMapper
$ scons 

This initiates a check-out of the batchmapper API and compiles a functional version of GeneMapper via a Java build.
After this is complete, ARepA will automatically generate general mapping files for its built-in gene conversion feature. 

Congratulations! Now you are ready to run ARepA. Before you run it, though, it is important to understand how ARepA handles user input. 

Chapter 1 Running ARepA 
============================================
ARepA was designed to be a simple command-line interface 
combining programmatic automation with an integrated data management tool 
that consolidates eclectic data from heterogeneous sources into a 
consistent, easily manipulable format. It was written with the Python programming 
language under the SCons software construction tool for dependency-tracking and 
automation. [Figure 1 of Paper] 

1.1 Input  
--------------------------------------------

The one essential input for ARepA is the taxonomic identifier of the organism of interest. This information is relayed onto ARepA in the **etc/taxa** text file. 
For instance, if you want to fetch human network and expression data across a multitude of data repositories, you would specify "Homo sapiens" in the input (etc/taxa). 
For example, typing ::

$ cd etc
$ less taxa 

will yield the default set of organisms

* Escherichia coli
* Vibrio cholerae
* Bacillus subtilis.

You can comment out any line with a hash "#". For example, the following file ::
* Escherichia coli
* #Vibrio cholerae
* #Bacillus subtillis 

will only fetch E. coli data, and nothing else.

Now, Tte entirety of the ARepA pipeline can be run with the execution of a simple command in terminlal. In the root directory of arepa, type ::

$ scons -k

The "-k" flag ensures that in the event of an incomplete or "bad" build, ARepA is instructed to carry on without halting. The output files, when built, 
will be saved in the **data** directory of the respective modules. For instance, with the above taxa file, E. coli expression data will saved in GEO/data.  

1.2 Output 
--------------------------------------------

ARepA by default fetches data from 7 different public repositories, which are listed below. For each repository, ARepA acquires the dataset names matching the taxonomic 
identifier specified by the input file. 

* Gene Expression/Gene co-expression - Data (text, pcl format), Metadata (python pickle), Documented R library containing both   
	* Gene Expression Omnibus 
* Interaction Networks - Data (text, dat format), Metadata (python pickle) 
	* Bacteriome 
	* RegulonDB
	* IntAct
	* MPIDB 
	* BioGrid
	* STRING 

1.3 Handy Features 
--------------------------------------------

Chpater 2 Modules 
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

Chapter 3 Structure 
============================================

.. image:: figure1.png
  :height: 300
  :width: 400
  :scale: 50
  :alt: Entity Diagram of ARepA  


1. SConstruct (SConscript) - the main driver script of the module. This initiates all processes downstream of the file.
2. data - this is where the downloaded (and parsed) is kept. 
3. src - contains all the source scripts. 
4. tmp - contains all intermediate files necessary to carry out the build for each module. 
5. etc - contains all configuration information for the module, including programmatic and manual overrides. 
6. doc - contains documentation for the module. 

Chapter 4 Advanced Topics 
============================================ 

Section 4.1 Testing ARepA 
--------------------------------------------

ARepA has a built-in unit testing script, located in the main **src** directory. 
While in the root directory, type ::

$ python src/test.py 

The default behavior of the testing script assumes that the entire build of ARepA is completed *prior* to running the script. If this is not the case, one can pass the optional argument "scons" to the test script and scons will be called in each submodule before the targets are checked. This method is error-prone and time-intensive and is not recommended. ::

$ python test.py scons 

Section 4.2 Advanced Configuration 
--------------------------------------------
Mapping status can be checked in every module by either checking the pickle metadata. 


Section 4.3 Running Modules Separately 
---------------------------------------------

After the taxonomic information has been downloaded
and processed by the parent node in arepa ("arepa/tmp/taxids" have been built),
one can launch any internal module separately by going into a desired directory and launching "scons". For instance, if one wants to run GEO, one would type (assuming starting from the root directory) ::

$ cd GEO
$ scons 

Section 4.3 Adding Custom Modules
---------------------------------------------

This is where things get fun. ARepA was designed so that adding new repositories is 
easy (well, as easy as the learning curve of SCons).  


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


Acknowledgements 
============================================ 

The authors would like to extend a special thanks to Larissa Miropolsky, who was involved in the development of the proof-of-concept of ARepA.  

References
=============================================
* Sleipnir
* Bioconductor Package 
* Batchmapper 
