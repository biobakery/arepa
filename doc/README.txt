======================================================
ARepA: Automated Repository Acquisition 
======================================================

..  This document follows reStructuredText syntax and conventions.
	You can compile this file to a PDF or HTML document. 

-------------------------------------------------------
User Manual, Version 0.9.3 
-------------------------------------------------------

Authors 
 Yo Sup Moon, Dr. Daniela Boernigen, Dr. Levi Waldron, Eric Franzosa, and Dr. Curtis Huttenhower

Maintainer
 Yo Sup Moon <moon.yosup@gmail.com> 

License 
 MIT License 

URL
 http://huttenhower.sph.harvard.edu/arepa 

Google Group
 arepa-users: https://groups.google.com/forum/?fromgroups#!forum/arepa-users

Citation 
 Yo Sup Moon, Daniela Boernigen, Levi Waldron, and Curtis Huttenhower. "ARepA: Automated Repository Acquisition" 
 (working title)


Chapter 0 Getting Started 
============================================

0.0 Overview 
--------------------------------------------

ARepA was designed to be a simple command-line interface 
combining programmatic automation with an integrated data management tool 
that consolidates eclectic data from heterogeneous sources into a 
consistent, easily manipulable format. It was written with the Python programming 
language under the SCons software construction tool for dependency-tracking and 
automation.

The current implementation of ARepA fetches data cross *seven* different data repositories: (1) Bacteriome, (2) BioGRID, (3) GEO, (4) IntAct, (5) MPIDB, (6) RegulonDB, and (7) STRING.
The data from each of these repositories are managed in separate directories. Each sub-directory in ARepA conforms to its "hierarchical modularity": (described in detail later)
sub-directories maintain the same essential structure. Essentially, this amounts to having a "driver file" that launches automated processes (pipeline) and directories containing relevant information to launch them.   

Here is a table describing the nature of each repository. 

+-----------------+---------------------+---------------+------------------+-------------------------+
| Database        | data type           | # Species     | # Interactions   | Ref                     |
+=================+=====================+===============+==================+=========================+
| Bacteriome      | physical assoc.     | 1             | 3,888            | {PMID:17942431}         |
+-----------------+---------------------+---------------+------------------+-------------------------+
| BioGRID         | physical assoc.     | 32            | 349,696          | {PMID:21071413}         |
+-----------------+---------------------+---------------+------------------+-------------------------+
| IntAct          | physical assoc.     | 278           | 239,940          | {PMID:22121220}         |
+-----------------+---------------------+---------------+------------------+-------------------------+
| MPIDB           | physical assoc.     | 250           | 24,295           | {PMID:18556668}         |
+-----------------+---------------------+---------------+------------------+-------------------------+ 
| RegulonDB       | regulatory assoc.   | 1             | 4,096            | {PMID:21051347}         |
+-----------------+---------------------+---------------+------------------+-------------------------+
| STRING          | functional assoc.   | 1,133         | 1,640,707        | {PMID:21045058}         |
+-----------------+---------------------+---------------+------------------+-------------------------+
| GEO             | gene expression     | 1,967         |                  | {PMID:21097893}         |
+-----------------+---------------------+---------------+------------------+-------------------------+

Section 0.1 Supported Operating Systems 
--------------------------------------------
ARepA was fully tested on and is supported by the following platform(s) 

* Linux 
* Mac OS X

The following platform(s) is(are) NOT supported:

* Windows 

The following platform(s) has(have) NOT been tested:

* Windows Cygwin 

NB: It is highly recommended that ARepA is run on a Linux cluster rather than on a local machine when 
intending to use it for performing large batch jobs. Certain processes (such as missing value imputation and functional network construction for GEO) can be extremely CPU-intensive and is not suitable for laptop set-ups. 
That being said, certain other processes, such as running custom pipelines to analyze the data once it has been downloaded, are both suitable and convenient to run on a local Unix-like environment. 

Section 0.2 Software Prerequisites 
--------------------------------------------

Before downloading ARepA, you should have the following software on your machine:

* Required 
	Python (ver >= 2.7.1) 
	SCons (ver >= 2.1.0)  
	R (ver >= 2.13.1) with Bioconductor package, permission to download new libraries
	Java SE 6 (ver >= 1.6.0): Java is needed for gene identifier conversion service
	Subversion Source Control Management (ver >= 1.7.8): for automated acquisition of BridgeDB

* Recommended 
	Sleipnir Library for Computational Functional Genomics (Optional, but necessary for some normalization 	steps)


Section 0.3 Downloading ARepa 
------------------------------------------------

You can download ARepA from the following url: http://huttenhower.sph.harvard.edu/arepa. 

Once you have downloaded arepa, you must set up the correct UNIX paths, which 
is described in the next section. 

Section 0.4 Setting up the Path 
--------------------------------------------

Once you have cloned arepa into a local directory, you must set up the correct UNIX paths
so that the necessary files in ARepA are recognized by your system. 
 
Make sure you are at the root level of arepa. Check by typing in your terminal ::

$ pwd 

Your local arepa directory should look something like this 

::

	BioGrid		doc			etc         GEO     	MPIDB	RegulonDB   src     tmp
	Bacteriome  GeneMapper  IntAct  	SConstruct  STRING


While in the root level in arepa, set the path by typing ::

$ export PATH=`pwd`/src:$PATH
$ export PYTHONPATH=`pwd`/src:$PYTHONPATH 

This command adds the main source directory to both the UNIX path for the bash shell and the environmental path for Python. These two lines should be added to your bashrc file to avoid repeating this exportation procedure every time you want to run arepa (with `pwd` replaced with the absolute path of arepa). For instance, the author's local version of arepa is in */Users/ysupmoon/hg/arepa*. To add to the bashrc one types ::

$ cd ~
$ echo 'export PATH=/Users/ysupmoon/hg/arepa/src:$PATH' |cat >> .bashrc 
$ echo 'export PYTHONPATH=/Users/ysupmoon/hg/arepa/src:$PYTHONPATH' |cat >> .bashrc 

This should append those two lines to the end of the .bashrc file.
We are almost there! We now move on to initializing the necessary components before we tell arepa to run. 
But first, we review some basic facts about arepa. 

Section 0.5 ARepA Basics 
--------------------------------------------- 

ARepA is built with *hierarchical modularity* in mind. This means that a computational process can be initiated 
from just about any node in the program tree. At every executable directory, you will see an "SConstruct" file.
This file can be launched with the command "scons". From the last section, we saw that your local directory structure 
of arepa might look like this 

	BioGrid		doc			etc         GEO     	MPIDB	RegulonDB   src     tmp
	Bacteriome  GeneMapper  IntAct  	SConstruct  STRING

Things to note: 

1. Folders with files pertaining to *this* particular level of arepa are in lowercase; for instance, 
**doc**, **etc**, **tmp**, and **src** are folders that describe this current node, the root node. 

2. Submodules start with uppercase characters; **BioGrid**, **Bacteriome**, **GeneMapper**, **IntAct**, **GEO**, **MPIDB**, **STRING**, and **RegulonDB** are all submodules that perform specific tasks. 

3. The "SConstruct" file is a file that launches all processes downstream from the main directory. 
Each module has an SConstruct file. The root directory has one, and so do each submodules. We can run arepa by typing 
"scons" in the root directory. Once it builds the necessary files for the current directory, arepa instructs its children to run. At this point, you can run each submodule separately. That is, you can pick specific repositories that you want data from. But we are not ready to run arepa yet! Follow the instructions on the next section. 

Section 0.6 Extracting Necessary Components  
---------------------------------------------

It is **recommended** that you extract and run the GeneMapper module **prior** to running the build in its entirety. 
ARepA will automatically do this for you when the necessity of using GeneMapper arises, but it is recommended that 
you do this first. This may save you some headaches. Extraction of GeneMapper can be done by running the SConstruct file in the GeneMapper directory. Let's first see what directories are present in the current implementation of arepa ::

$ ls 

What you see is the following

::

	Bacteriome  BioGrid  doc  etc  GeneMapper  GEO  IntAct  MPIDB  RegulonDB  SConstruct  src  STRING  tmp

Everything you see is a **directory** except for a specialized **file** named "SConstruct". 
Right now, we are interested in only initializing the directory "GeneMapper".
Starting at the root directory (you should already be there), type ::

$ cd GeneMapper
$ scons 

This initiates a check-out of the BridgeDB API and compiles a functional version of GeneMapper via a Java build (this is why we need Java!).
After this is complete, ARepA will automatically provide gene identifier conversion services (given that a mapping file for the specified organism exists; 
we will talk more about what this means later).  

Congratulations! Now you are ready to run ARepA. Before you run it, though, it is important to understand how ARepA handles user input. 


Chapter 1 Running ARepA (Simple)
============================================


Chapter 2 Running ARepA (Customized)
============================================

2.1 Input  
--------------------------------------------

ARepA requires the user to provide (1) the taxonomic identifier of the organism of interest and (2) the final gene identifier standard (gene name, uniprot, kegg orthologs, etc). 
This information is relayed onto ARepA in the **etc/taxa** and **etc/geneid** text files, respectively. 
For instance, if you want to fetch human network and expression data across a multitude of data repositories, you would specify "Homo sapiens" in the input (etc/taxa). 

1. Taxa 

	A new copy of ARepA is by default instructed to download a set of model organism data. 

	Typing ::

	$ cd etc
	$ less taxa 

	will yield the default set of organisms

	* Homo sapiens 
	* Escherichia coli
	* Mus musculus 
	* Saccharomyces cerevisiae
	* Pseudomonas aeruginosa

	Following the pythonic standard, you can comment out any line with a hash "#". For example, the following file ::

	* Homo sapiens 
	* #Escherichia coli
	* #Mus musculus 
	* #Saccharomyces cerevisiae
	* #Pseudomonas aeruginosa
	will only fetch E. coli data, and nothing else.

2. Gene ID 

	By default, 


Now, The entirety of the ARepA pipeline can be run with the execution of a simple command in terminal. In the root directory of arepa, type ::

$ scons -k

The "-k" flag ensures that in the event of an incomplete or "bad" build, ARepA is instructed to carry on without halting. A more thorough, albeit technical,
explaination can be found in the SCons user manual. 
The output files, when built, will be saved in the **data** directory of the respective modules.
For instance, with the above taxa file, E. coli expression data will saved in GEO/data, and regulatory association network data in RegulonDB/data, and so forth.   

2.2 Output 
--------------------------------------------

ARepA by default fetches data from 7 different public repositories, which are again listed below. For each repository, ARepA acquires the dataset names matching the taxonomic 
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

2.3 Advanced Input  
--------------------------------------------

Chapter 3 Modules 
============================================

There are two types of modules: **internal modules**, and 
**external modules**. Internal modules do actual downloading and processing 
of data/metadata from public repositories; external modules serve 
global helper functions, such as gene identifier conversion. 
Here is a list of external module(s): 

1. GeneMapper - converts gene identifiers into common format 

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

Chapter 4 Design Choice 
============================================

1. SConstruct - the main driver script of the module. This initiates all processes downstream of the file.
2. data - this is where the downloaded (and parsed) is kept. 
3. src - contains all the source scripts. 
4. tmp - contains all intermediate files necessary to carry out the build for each module. 
5. etc - contains all configuration information for the module, including programmatic and manual overrides. 
6. doc - contains documentation for the module. 

Chapter 5 Advanced Topics 
============================================ 

Section 5.1 Unit-Testing ARepA 
--------------------------------------------

ARepA has a built-in unit testing script, located in the main **src** directory. 
While in the root directory, type ::

$ python src/test.py 

The default behavior of the testing script assumes that the entire build of ARepA is completed *prior* to running the script. If this is not the case, one can pass the optional argument "scons" to the test script and scons will be called in each submodule before the targets are checked. This method is error-prone and time-intensive and is not recommended. ::

$ python test.py scons 

Section 5.2 Advanced Configuration 
--------------------------------------------
Mapping status can be checked in every module by either checking the pickle metadata. 


Section 5.3 Running Modules Separately 
---------------------------------------------

After the taxonomic information has been downloaded
and processed by the parent node in arepa ("arepa/tmp/taxids" have been built),
one can launch any internal module separately by going into a desired directory and launching "scons". For instance, if one wants to run GEO, one would type (assuming starting from the root directory) ::

$ cd GEO
$ scons 

Section 5.4 Adding Custom Modules
---------------------------------------------

This is where things get fun. ARepA was designed so that adding new repositories is 
easy (well, as easy as the learning curve of SCons).  


Chapter 6 Frequently Asked Questions 
============================================

NB: All questions should be directed to the arepa-users group group. 

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

5. My organisms/datasets are not being downloaded! 

6. How do I cite ARepA? 


Acknowledgements 
============================================ 

The authors would like to extend a special thanks to Larissa Miropolsky, who was involved in the development of the proof-of-concept of ARepA.  

References
=============================================
* Sleipnir
* Bioconductor Package 
* BridgeDB 


License  
==============================================

This software is licensed under the MIT license. 

Copyright (c) 2013 Yo Sup Moon, Dr. Daniela Boernigen, Dr. Levi Waldron, Dr. Eric Franzosa, and Dr. Curtis Huttenhower 

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
