======================================================
ARepA: Automated Repository Acquisition
======================================================

..  This document follows reStructuredText syntax and conventions.
	You can compile this file to a PDF or HTML document.
	For instructions on how to do so, visit the reStructeredText webpage
	(http://docutils.sourceforge.net/rst.html).

-------------------------------------------------------
User Manual, Version 0.9.7
-------------------------------------------------------

Authors
 Yo Sup Moon, Daniela Boernigen, Levi Waldron, Eric Franzosa, Xochitl Morgan, and Curtis Huttenhower

Google Group
 arepa-users: https://groups.google.com/forum/?fromgroups#!forum/arepa-users

License
 MIT License

URL
 http://huttenhower.sph.harvard.edu/arepa

Citation
 Daniela Boernigen*, Yo Sup Moon*, Levi Waldron, Eric Franzosa, Xochitl Morgan, and Curtis Huttenhower. "ARepA: Automated Repository Acquisition" (In Submission)
 (* contributed equally)

.. contents ::

Chapter 0 Getting Started
============================================

Section 0.0 Overview
--------------------------------------------

ARepA was designed to be a simple command-line interface that consolidates eclectic 'omics data from heterogeneous sources into a consistent, easily manipulable format.
Its standard features include data normalization (e.g. log transform), missing value imputation, quality control against malformed data, gene identifier standardization, and basic network inference for expression data. It was written with the Python and R programming languages, alongside the SCons software construction tool for dependency-tracking and automation.

The current implementation of ARepA fetches data cross seven different data repositories: (1) Bacteriome, (2) BioGRID, (3) GEO, (4) IntAct, (5) MPIDB, (6) RegulonDB, and (7) STRING. Here is a table describing what we can get out of each repository.

+-----------------+-----------------------+---------------+------------------+-------------------------------------+
| Database        | data type             | # Species     | # Interactions   | Reference                           |
+=================+=======================+===============+==================+=====================================+
| Bacteriome      | physical interaction  | 1             | 3,888            | Su, Peregrin-Alvarez et al. 2008    |
+-----------------+-----------------------+---------------+------------------+-------------------------------------+
| BioGRID         | physical interaction  | 32            | 349,696          | Stark, Breitkreutz et al. 2011      |
+-----------------+-----------------------+---------------+------------------+-------------------------------------+
| IntAct          | physical interaction  | 278           | 239,940          | Kerrien, Aranda et al. 2012         |
+-----------------+-----------------------+---------------+------------------+-------------------------------------+
| MPIDB           | physical interaction  | 250           | 24,295           | Goll, Rajagopala et al. 200 8       |
+-----------------+-----------------------+---------------+------------------+-------------------------------------+
| RegulonDB       | regulatory interaction| 1             | 4,096            | Gama-Castro, Salgado et al. 2011    |
+-----------------+-----------------------+---------------+------------------+-------------------------------------+
| STRING          | functional association| 1,133         | 1,640,707        | Szklarczyk, Franceschini et al. 2011|
+-----------------+-----------------------+---------------+------------------+-------------------------------------+
| GEO             | gene expression       | 1,967         |                  | Barrett, Troup et al. 2011          |
+-----------------+-----------------------+---------------+------------------+-------------------------------------+

Section 0.1 Supported Operating Systems
--------------------------------------------
ARepA was fully tested on and is supported by the following platform(s)

* Linux
* Mac OS X (>= 10.7.4)

The following platform(s) is(are) NOT supported:

* Windows (>= XP)

The following platform(s) has(have) NOT been tested:

* Cygwin

NB: It is highly recommended that ARepA is run on a Linux cluster rather than on a local machine when
intending to use it for performing large batch jobs. Certain processes (such as missing value imputation and functional network construction for GEO) can be extremely CPU-intensive and is not suitable for laptop set-ups. That being said, certain other processes, such as running custom pipelines to analyze the data once it has been downloaded, are both suitable and convenient to run on a local Unix-like environment.

Section 0.2 Software Prerequisites
--------------------------------------------

Before downloading ARepA, you should have the following software on your machine:

* Required
	* Python (ver >= 2.7)
	* SCons (ver >= 2.1)
	* R (ver >= 2.13) with GEOquery package (part of Bioconductor)
	* Java SE 6 (ver >= 1.6): Java is needed for gene identifier conversion service
	* Apache Ant (ver >= 1.8.0)
	* Subversion Source Control Management (ver >= 1.7): for automated acquisition of BridgeDB
	* curl
	* wget

* Recommended
	* Sleipnir Library for Computational Functional Genomics (Optional, but necessary for some normalization steps)

Section 0.3 Downloading ARepa
------------------------------------------------

You can download ARepA from the following url: http://huttenhower.sph.harvard.edu/arepa. Once you have downloaded ARepA, you must set up the correct python paths, which is described in the next section.

Section 0.4 Setting up the Path
--------------------------------------------

Once you have cloned arepa into a local directory, you must set up the correct python paths
so that the necessary files in ARepA are recognized by your python interpreter. Make sure you are at the root level of arepa. Check by typing in your terminal ::

$ ls

Your local arepa directory should look something like this

::

	Bacteriome
	BioGrid
	doc
	etc
	GeneMapper
	GEO
	IntAct
	MPIDB
	RegulonDB
	SConstruct
	src
	STRING
	tmp

While in the root level in arepa, set the path by typing ::

	$ export PYTHONPATH=`pwd`/src:$PYTHONPATH

This command adds the main source directory to the environmental variable PYTHONPATH. These two lines should be added to your bashrc file to avoid repeating this exportation procedure every time you want to run arepa.

Section 0.5 ARepA Basics
---------------------------------------------

ARepA is built with *hierarchical modularity* in mind. This means that a computational process can be initiated from just about any node in the program tree. At every executable directory, you will see an "SConstruct" file.This file can be launched with the command "scons".

Things to note:

1. Folders with files pertaining to *this* particular level of arepa are in lowercase; for instance, **doc**, **etc**, **tmp**, and **src** are folders that describe this current node, the root node.

2. Submodules start with uppercase characters; **BioGrid**, **Bacteriome**, **GeneMapper**, **IntAct**, **GEO**, **MPIDB**, **STRING**, and **RegulonDB** are all submodules that perform specific tasks.

3. The "SConstruct" file is a file that launches all processes downstream from the main directory. Each module has an SConstruct file. The root directory has one, and so do each submodules. We can run 		arepa by typing "scons" in the root directory. Once it builds the necessary files for the current directory, arepa instructs its children to run. At this point, you can run each submodule separately. That is, you can pick specific repositories that you want data from. But we are not ready to run arepa yet! Follow the 	instructions on the next section.


Chapter 1 Running ARepA
============================================

Section 1.0 Basics
--------------------------------------------

Typing **scons** in your terminal screen at the root level of arepa will initiate the pipeline process. There are two flags that users should be aware of.

1. The **-k** flag: when an error is encountered in the build process, skip to the next build whenever possible. Without this flag, a single error in the build tree will terminate the entire arepa process. Sometimes datasets contain errors that are beyond arepa's control. In this case, we would like arepa to be robust to these inconsistensies.

2. The **-j** flag: this allows for multiple threads to run at once, greatly increasing the speed of the build. Usually, the user should specify the number of threads to be the number of cores on the machine he/she is using.

For example, on a quad-core machine, one would type
::

	$ scons -kj4

For a complete list of options, run "scons --help" on the command line.

When all targets in its computation tree are built, scons will give the following message

::

	scons: done building targets.

Section 1.1 Input
--------------------------------------------

ARepA requires the user to provide (1) the taxonomic identifier of the organism of interest and (2) the final gene identifier standard (gene name, uniprot, kegg orthologs, etc).
This information is relayed onto ARepA in the **etc/taxa** and **etc/geneid** text files, respectively.
For instance, if you want to fetch human network and expression data across a multitude of data repositories, you would specify "Homo sapiens" in the input (etc/taxa).

Taxa
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A new copy of ARepA is by default instructed to download a set of model organism data.

Typing ::

$ cd etc
$ less taxa

will yield the default set of organisms
::

	Homo sapiens
	Escherichia coli
	Mus musculus
	Saccharomyces cerevisiae
	Pseudomonas aeruginosa

Following the pythonic standard, you can comment out any line with a hash "#". For example, the following file

::

	Homo sapiens
	#Escherichia coli
	#Mus musculus
	#Saccharomyces cerevisiae
	#Pseudomonas aeruginosa

will only fetch Homo sapiens data, and nothing else.

Gene ID
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, the gene identifier of choice is specified to be UniRef90/UniRef100 identifiers, given by the symbol "U":

Typing ::

$ cd etc
$ less geneid

will yield the default output geneid
::

	U


Here is a list of supported gene identifiers (can be extended by giving arepa custom gene mapping files provided by the user):

+-----------------+--------------------+
| Name            | ARepA Symbol       |
+=================+====================+
| UniRef      	  | U                  |
+-----------------+--------------------+
| Gene Symbol     | H                  |
+-----------------+--------------------+
| KEGG Ortholog   | Ck                 |
+-----------------+--------------------+
| UniProt         | S                  |
+-----------------+--------------------+
| KEGG Entry      | Kg                 |
+-----------------+--------------------+
| Affymetrix      | X                  |
+-----------------+--------------------+
| Entrez Gene     | L                  |
+-----------------+--------------------+	

It should be noted that the gene id mapping is based on BridgeDB (van Iersel et al. 2010, http://www.bridgedb.org/). A list of system codes supported by arepa for extension can be viewed in the file **arepa/GeneMapper/etc/batchlist.txt**.


Section 1.2 Output
--------------------------------------------

ARepA by default fetches data from seven different public repositories, which are again listed below. For each repository, ARepA acquires the dataset names matching the taxonomic
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

The output for each directory can be found in $REPOSITORY_NAME/data. Expression tables are saved in a *pcl* format (for a brief description, visit http://www.broadinstitute.org/cancer/software/gsea/wiki/index.php/Data_formats). The final pcl output will always be $DATASET_NAME.pcl. Interaction networks are saved in a *dat/dab* format (http://huttenhower.sph.harvard.edu/content/genomic-data-formats). The final dat/dab output will always be $DATASET_NAME.{dat|dab}. Metadata is saved as a python pickle (http://docs.python.org/2/library/pickle.html), a compressed, structured object. When loaded, metadata is given as a python dictionary, which is essentially a series of key,value pairs http://docs.python.org/2/tutorial/datastructures.html). Metadata is saved as $DATASET_NAME.pkl.

Section 1.3 Example Output
--------------------------------------------
Let's look at an example of arepa output. Take a look at the data directory of the Bacteriome repository.
::

	$ cd Bacteriome/data
	$ ls

	bacteriome_00raw.dab
	bacteriome_00raw.dat
	bacteriome_00raw_mapped00.dat
	bacteriome_00raw_mapped01.dat
	bacteriome_00raw.quant
	bacteriome.dat
	bacteriome.pkl
	status.txt

Bacteriome is an interaction repository, so we have dat/dab files as final output. We see that there are multiple dat files; however, only one is the final output. The final output is always given by $DATASET_NAME.dat, or in this case, "bacteriome.dat". Other files, such as "bacteriome_00raw.dat" are intermediate files, which can be also useful to the user. The metadata is given by "bacteriome.pkl".

Section 1.4 Metadata Usage
--------------------------------------------
There is a useful script in the main src directory of arepa that can aid in dealing with pickled metadata.

::

	$ cd src/
	$ unpickle.py -h

	usage: unpickle.py [-h] [-m str_split] [-c columns] [-s skip_rows]
                   [-l log.txt] [-r] [-k str_man_key] [-x]
                   [input] [output]

	pickle and unpickle files.

	positional arguments:
	  input           input pickle or text file
	  output          output pickle or text file

	optional arguments:
	  -h, --help      show this help message and exit
	  -m str_split    Split between key and value
	  -c columns      Number of columns to map
	  -s skip_rows    Number of header rows to skip at top of file
	  -l log.txt      Optional log file containing status metavariables
	  -r              Reverse flag
	  -k str_man_key  Flag to specify output for specific key in the pickle
	  -x              Give output in R package metadata format

As an example usage, one can quickly view the contents of the metadata by using the "unpickle.py" script.

::

	$ cd Bacteriome/data
	$ unpickle.py bacteriome.pkl

	title	Bacteriome
	url	http://www.compsysbio.org/bacteriome/dataset/combined_interactions.txt
	conditions	3888
	gloss	Bacterial Protein Interaction Database
	taxid	83333
	mapped	True
	type	protein interaction

One can also convert a tab delimited text file into a python pickle.
::

	$ unpickle.py -r tab_delimtied_file.txt > output.pkl

One can also quickly view a key,value pair contained in the pickle. For instance, if one wants to view the gene id mapping status of the dataset, perform ::

	$ unpickle.py -k mapped metadata_file

For the case of bacteriome ::
	$ unpickle.py -k mapped Bacteriome/data/bacteriome.pkl
	True

For full usage of the metadata, see the argument list above.


Chapter 2 Modules
============================================

Section 2.0 Internal vs External Modules
--------------------------------------------

The data from each of these repositories are managed in separate directories. Each sub-directory in ARepA conforms to a hierarchical modularity, in which all the sub-directories maintain the same essential structure. Essentially, this amounts to having a "driver file" that launches automated processes (pipeline) and directories containing relevant information to launch them.

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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Gene Expression Omnibus

Interaction Networks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Bacteriome
2. RegulonDB
3. IntAct
4. MPIDB
5. BioGRID
6. STRING

Hierarchical Modularity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each module contains the following:

1. SConstruct - the main driver script of the module. This initiates all processes downstream of the file.
2. data - this is where the downloaded (and parsed) is kept.
3. src - contains all the source scripts.
4. tmp - contains all intermediate files necessary to carry out the build for each module.
5. etc - contains all configuration information for the module, including programmatic and manual overrides.
6. doc - contains documentation for the module.

Section 2.1 Bacteriome
--------------------------------------------

* Optional Inputs
	* None

* Final Outputs
	* data/bacteriome.dat - network matrix
	* data/bacteriome.pkl - metadata

Section 2.2 RegulonDB
--------------------------------------------

* Optional Inputs
	* None

* Final Outputs
	* data/regulondb.dat - network matrix
	* data/regulondb.pkl - metadata

Section 2.3 IntAct
--------------------------------------------

* Optional Inputs
	* etc/include - list of dataset IDs to include (one per line)
	* etc/exclude - list of dataset IDs to exclude (one per line)
	* etc/manual_curation - manually curated metadata, tab-delimited, one row per sample, one column per metadatum
	* etc/manual_mapping - manually curated gene ID mapping, tab-delimited, one row per gene family equivalence class

* Final Outputs
	* data/dataset_name/dataset_name.dat - network matrix
	* data/dataset_name/dataset_name.pkl - metadata

Section 2.4 MPIDB
--------------------------------------------

* Optional Inputs
	* etc/include - list of dataset IDs to include (one per line)
	* etc/exclude - list of dataset IDs to exclude (one per line)
	* etc/manual_curation - manually curated metadata, tab-delimited, one row per sample, one column per metadatum
	* etc/manual_mapping - manually curated gene ID mapping, tab-delimited, one row per gene family equivalence class

* Final Outputs
	* data/dataset_name/dataset_name.dat - network matrix
	* data/dataset_name/dataset_name.pkl - metadata

Section 2.5 BioGRID
--------------------------------------------

* Optional Inputs
	* etc/include - list of dataset IDs to include (one per line)
	* etc/exclude - list of dataset IDs to exclude (one per line)
	* etc/manual_curation - manually curated metadata, tab-delimited, one row per sample, one column per metadatum
	* etc/manual_mapping - manually curated gene ID mapping, tab-delimited, one row per gene family equivalence class

* Final Outputs
	* data/dataset_name/dataset_name.dat - network matrix
	* data/dataset_name/dataset_name.pkl - metadata

Section 2.6 STRING
--------------------------------------------

* Optional Inputs
	* etc/include - list of dataset IDs to include (one per line)
	* etc/exclude - list of dataset IDs to exclude (one per line)
	* etc/manual_curation - manually curated metadata, tab-delimited, one row per sample, one column per metadatum
	* etc/manual_mapping - manually curated gene ID mapping, tab-delimited, one row per gene family equivalence class

* Final Outputs
	* data/dataset_name/dataset_name.dat - network matrix
	* data/dataset_name/dataset_name.pkl - metadata

Section 2.7 GEO
--------------------------------------------

* Optional Inputs
	* etc/include - list of dataset IDs to include (one per line)
	* etc/exclude - list of dataset IDs to exclude (one per line)
	* etc/batch - turn on/off batch mode; see include/exclude behavior in Advanced Topics for more details 
	* etc/manual_curation - manually curated metadata, tab-delimited, one row per sample, one column per metadatum
	* etc/manual_mapping - manually curated gene ID mapping, tab-delimited, one row per gene family equivalence class
	* etc/mapping - configure regexps for identifying gene ID mapping columns in platform files
	* etc/raw - one-line text file (True or False), turn on/off downloading and processing of raw CEL files for each dataset
	* etc/preprocess - one-line text file (Bioconductor function name), chooose a processing function for normalizing raw CEL files
	* etc/rpackage - one-line text file (True or False), turn on/off creation of expression sets and R packages per dataset
	* etc/sleipnir - one-line text file (True or False), turn on/off Sleipnir normalization functions (Normalizer, KNNImpute, Dat2Dab, etc.)

* Final Outputs
	* data/dataset_name/dataset_name.dat - network matrix
	* data/dataset_name/dataset_name.pkl - metadata

Chapter 3 Advanced Topics
============================================

Section 3.0 Customized Pipeline
---------------------------------------------

Each module in ARepA can be tweaked to the user's taste: for instance, one can
override automatically generated metadata by providing his own; additionally, one can
override automatically generated mapping files with a custom-curated one.

Curated Metadata
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add a tab-delimited text file in **repository/etc/manual_curation/** with the matching dataset name (e.g. IntAct/etc/manual_curation/IntAct_taxid_287.txt)

Curated Gene Mapping
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add a tab-delimited gene map file in **repository/etc/manual_mapping/** with the matching dataset name (.map).

Caveat: follow the system code - label key as defined by **GeneMapper/etc/batchlist.txt**
See GEO/etc/manual_mapping for an example.


Section 3.1 Running Modules Separately
---------------------------------------------

After the taxonomic information has been downloaded
and processed by the parent node in arepa (**arepa/tmp/taxids** have been built),
one can launch any internal module separately by going into a desired directory and launching **scons**.
For instance, if one wants to run GEO, first make sure that the taxids file was built correctly, then launch **scons** in the GEO directory.

::

	$ scons tmp/taxids
	scons: Reading SConscript files ...
	scons: done reading SConscript files.
	scons: Building targets ...
	funcPipe(["tmp/taxids"], ["src/taxdump2taxa.py", "tmp/taxdump.txt", "etc/taxa"])
	cat "arepa/tmp/taxdump.txt" | arepa/src/taxdump2taxa.py "arepa/etc/taxa" > "arepa/tmp/taxids"
	scons: done building targets.

	$ cd GEO
	$ scons

Section 3.2 Adding New Modules
---------------------------------------------

Advanced users who are familiar with scons can write their own modules that download and process data from a repository that is not included in vanilla ARepA.
There are TWO basic steps that must take place.

(1) Initiation script - starts the download of dataset names, filters out only the desired ones, which are passed onto scripts that handles *per dataset* functions.
(2) Per dataset parsing scripts - download raw data and metadata, run various vanilla and customized parsing functions.

Let us go through an example.

Step 1: The SConstruct file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Create a directory on the main level of arepa and initiate an **SConstruct** file. For the purpose of this example, we will call this module **my_repo**
::

	$ mkdir my_repo
	$ touch SConstruct

Following the arepa convention, create the directories **tmp**, **etc** and **src**, which will store raw downloaded files, configuration files, and source scripts respectively.

::

	$ mkdir tmp etc src

Now, the SConstruct file serves as a driver file that launches all processes within the module. For those users that are familiar with make, these are analogous to Makefiles.

Edit the SConstruct to perform the following actions: (1) Download a batch list of dataset names and parse them into a text file, where each line contains a dataset name (2) Pass dataset names to child directories. This will initiate a separate modular build for each dataset name.

Suppose that you have created two text files **dataset1.txt** and **dataset2.txt** and that
**c_fileInputExclude** and **c_fileInputInclude** are pointers to files that contain dataset names that the user wants to
exclude/include respectively (can be empty). A repository can have many different types of datasets (e.g. GEO has GDS and GSE datasets); the names of different datasets should be in separate files (this is why we have two text files in this example case).
::

	#SConstruct file
	import sfle
	# SflE stands for Scientific Flow Environment, a tool that contains various python/arepa wrappers for scons.
	# It is an extremely convenient and powerful tool. For documentation visit huttenhower.sph.harvard.edu/sfle.
	import arepa
	# arepa.py contains arepa-specific global utilities

	pE = DefaultEnvironment()
	
	# Download and parse names
	# ...

	c_strFileDataset1 = "tmp/dataset1.txt"
	c_strFileDataset2 = "tmp/dataset2.txt"

	afileTXTs = [c_strFileDataset1, c_strFileDataset2]

IMPORTANT: it is *crucial* that users build their files in the scons standard; i.e. in a tracked manner. Ad-hoc building of files outside of scons will not, in general, give correct builds.

You can pass the IDs to child directories in the following manner ::

	sfle.sconscript_children( pE, afileTXTs, sfle.scanner( c_fileInputExclude, c_fileInputInclude ), 1, arepa.c_strProgSConstruct )

The "1" here refers to the hierarchy level. Recall that ARepA was designed with hierarchical modularity as a design principle; one can initiate a downstream process at any point in the computational tree. Processes that are stemmed from level 1 should be labeled as level "2" and so on.

This instructs arepa to do the following: for each name in the provide dataset names, perform actions defined by source scripts in the **src** directory. In particular, do this in a modular way, such that each dataset can be launched independently later on.

Step 2: The SConscript_n.py Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
For each name in the dataset name list (modulo excluded names), arepa looks in the **src** folder and launches the **SConscript_n.py** scripts in numerical order. For instance **SConscript_1.py** will be launched before **SConscript_2.py**. The information in these scripts are loaded into the SCons environment; the users can think of these files as pseudo-SConstruct files in which all SCons python wrappers can be used.

Let's take a look at an example (IntAct/src/SConscript_1-id.py) ::
	
	#!/usr/bin/env python

	def test( iLevel, strID, hashArgs ):
		return ( iLevel == 1 )
	if locals( ).has_key( "testing" ):
		sys.exit( )

	pE = DefaultEnvironment( )

	c_strID					= arepa.cwd( )
	c_fileInputIntactC		= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirTmp, "intactc" )
	c_fileIDPKL				= sfle.d( pE, c_strID + ".pkl" )
	c_fileIDDAB				= sfle.d( pE, c_strID + ".dab" )
	c_fileIDRawDAT          = sfle.d( pE, c_strID + "_00raw.dat" )
	c_fileIDDAT				= sfle.d( pE, c_strID + ".dat")
	c_fileIDQUANT           = sfle.d( pE, c_strID + ".quant" )

	c_fileProgUnpickle      = sfle.d( pE, arepa.path_arepa( ), sfle.c_strDirSrc, "unpickle.py" )
	c_fileProgC2Metadata    = sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "c2metadata.py" )
	c_fileProgC2DAT         = sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "c2dat.py" )

	c_fileInputSConscriptGM         = sfle.d( pE, arepa.path_arepa(),sfle.c_strDirSrc,"SConscript_genemapping.py")
	c_fileInputSConscriptDAB        = sfle.d( pE, arepa.path_arepa(), sfle.c_strDirSrc, "SConscript_dat-dab.py" )

	c_fileStatus 	    			=  sfle.d(pE, "status.txt")
	c_strGeneFrom 				    = "S"

	afileIDDAT = sfle.pipe( pE, c_fileInputIntactC, c_fileProgC2DAT, c_fileIDRawDAT, [c_strID] )

	# ... rest of the code omitted ...

The first piece of code ::
	
	def test( iLevel, strID, hashArgs ):
		return ( iLevel == 1 )
	if locals( ).has_key( "testing" ):
		sys.exit( )

makes sure that the script is launched in the right arepa level. This can be modified to take any arbitrary conditional.
This is convenient when writing different scripts to handle different types of datasets. For instance, for GEO, two different scripts are used to handle GDS and GSE datasets. For instance, ::

	#GEO/src/SConscript_1-gse.py

	def test( iLevel, strID, hashArgs ):
		return ( iLevel == 1 ) and ( strID.find( "GSE" ) == 0 )
	if locals( ).has_key( "testing" ):
		sys.exit( )

ensures that this particular script launches only for GSE datasets.

Now, let's take a look at the rest of the code in the IntAct example. Most scons processes can be hidden away by using features available in sfle (included in arepa; visit huttenhower.sph.harvard.edu/sfle for documentation). For instance, **sfle.pipe()** seen in the above example performs a UNIX pipe that is tracked by scons, in a manner that is consistent with conventions in arepa. Customized pipelines can be built by the user providing their own python scripts. Of course, users can also utilize features that are already available in vanilla ARepA.

Section 3.3 ARepA-provided functions
---------------------------------------------

These are scripts that perform routinely performed tasks in arepa.

* arepa/src/unpickle.py: pickles and unpickles files ::

	$ unpickle.py --help
	usage: unpickle.py [-h] [-m str_split] [-c columns] [-s skip_rows]
	                   [-l log.txt] [-r] [-k str_man_key] [-x]
	                   [input] [output]

	pickle and unpickle files.

	positional arguments:
	  input           input pickle or text file
	  output          output pickle or text file

	optional arguments:
	  -h, --help      show this help message and exit
	  -m str_split    Split between key and value
	  -c columns      Number of columns to map
	  -s skip_rows    Number of header rows to skip at top of file
	  -l log.txt      Optional log file containing status metavariables
	  -r              Reverse flag
	  -k str_man_key  Flag to specify output for specific key in the pickle
	  -x              Give output in R package metadata format

* arepa/src/makeunique.py: Takes a malformed gene mapping file, removes duplicates and splits up one-to-many mappings ::

	$ makeunique.py --help
	usage: makeunique.py [-h] [-m str_split] [-c columns] [-s skip_rows]
	                     [-l log.txt]
	                     [input.dat] [output.dat]

	Gets rid of duplicate entries from a tab-delimited file of unordered tuples.

	positional arguments:
	  input.dat     Input tab-delimited text file with one or more columns
	  output.dat    Input tab-delimited text file with mapped columns

	optional arguments:
	  -h, --help    show this help message and exit
	  -m str_split  Ambiguous field element classifier; a or b; e.g. in the case
	                of a///b the value will be ///
	  -c columns    Number of columns to map
	  -s skip_rows  Number of header rows to skip at top of file
	  -l log.txt    Optional log file containing output mapping status

* arepa/src/merge_genemapping.py: Merges two gene maps ::
	
	# Usage: merge_genemapping.py <map1.txt> <map2.txt> <out.txt>

* arepa/GeneMapper/src/bridgemapper.py: Performs gene mapping (gene standardization) ::

	$ bridgemapper.py --help
	usage: bridgemapper.py [-h] [-m mapping.txt] [-c columns] [-f from_format]
	                       [-t to_format] [-u max_lines] [-s skip_rows]
	                       [-l log.txt] [-x]
	                       [input.dat] [output.dat]

	Maps gene IDs from one or more tab-delimited text columns from and to
	specified formats.

	positional arguments:
	  input.dat       Input tab-delimited text file with one or more columns
	  output.dat      Input tab-delimited text file with mapped columns

	optional arguments:
	  -h, --help      show this help message and exit
	  -m mapping.txt  Required mapping file in tab-delimited BridgeMapper format
	  -c columns      Columns to map, formatted as [1,2,3]
	  -f from_format  BridgeMapper single-character type code for input format
	  -t to_format    BridgeMapper single-character type code for output format
	  -u max_lines    Maximum lines in input file; this is done for memory reasons
	  -s skip_rows    Number of header rows to skip at top of file
	  -l log.txt      Optional log file containing output mapping status
	  -x              Optional flag turning on/off gene identifier sniffer
	                  (automatically decide geneid_from)


Section 3.4 Unit-Testing ARepA
--------------------------------------------

ARepA has a built-in unit testing script, located in the main **src** directory.
While in the root directory, type
::

	$ python src/test.py

The default behavior of the testing script assumes that the entire build of ARepA is completed *prior* to running the script. If this is not the case, one can pass the optional argument "scons" to the test script and scons will be called in each submodule before the targets are checked. This method is error-prone and time-intensive and is not recommended. ::

	$ python test.py scons

Section 3.5 Include/Exclude Behavior for Submodules 
------------------------------------------------------

The following is a description of the way ARepA handles what datasets it will include or exclude during the downloading process for 
all the submodules. 

#. ARepA fetches the list of all possible datasets under the specified taxonomy in the `tmp` directory. We call this the "universe" of datasets for each repository. 
#. If `etc/exclude` and `etc/include` exist, ARepA launches build for datasets specified in (`universe` **intersect** `include`) **setminus** `exclude`.
#. Sometimes the user will wish to curtail this default behavior and simply download only the files listed in the `etc/include` file. This behavior can be turned off by setting the `etc/batch` configuration to "False". This feature is especially useful for GEO. See the GEO section in the previous chapter for more details. 

Chapter 4 Frequently Asked Questions (FAQ)
============================================

NB: All questions should be directed to the arepa-users Google Group.

1. I get the following error when I run ARepA ::

	ImportError: No module named arepa

*Solution*
 Make sure you add the **src** directory of ARepA's root level to the python UNIX path.

2. I get the following error when I run ARepA ::

	ImportError: No module named sfle

*Solution*
 Make sure you add the **src** directory of ARepA's root level to the python UNIX path.

3. Help, I got a 404 error from (IntAct or GEOmetadb or Bacteriome or...)

*Solution*
 Academic software doesn't always work - ours included, but in this case it's not our fault!  Some files from some repositories are periodically unavailable, preventing ARepA from downloading them.  The recommended workaround is documented above, specifically running ARepA using the ``scons -k`` flag.

4. Where can I find configuration information for my pipelines?

*Solution*
 All configuration information is in the **etc** folder of every directory. See the chapter on specific modules for more details on configuration information for a particular repository.

5. I don't get any per-sample metadata in GDS datasets from GEO?

*Solution*
 GEO's downloads for GDS files don't include per-sample metadata, which prevents ARepA from annotating it.  To retrieve this information, use the GSE equivalents for the target GDS dataset(s) instead (e.g. GSE22648 for GDS3921).

6. Where is the per-condition GEO metadata?

*Solution*
 Added to the ``*.pkl`` file, and to the expression set (if ``GEO/etc/rpackage`` is set to True). It can be extracted from the ``.pkl`` file using the shared script ``unpickle.py``.

Acknowledgements
============================================

The authors would like to extend a special thanks to Felix Wong, Timothy Tickle, Svitlana Tyekucheva, Markus Schröder, Owen White, and Arthur Brady for assisting in the testing process of ARepA.

References
=============================================

* Tools
	* Sleipnir: 		http://huttenhower.sph.harvard.edu/sleipnir/index.html
	* GEOquery: 		http://watson.nci.nih.gov/~sdavis/
	* BridgeDb: 		http://www.bridgedb.org/

* Databases
	* Bacteriome: 		http://www.compsysbio.org/bacteriome/
	* IntAct :			http://www.ebi.ac.uk/intact/
	* GEO:				http://www.ncbi.nlm.nih.gov/geo/
	* MPIDB:	 		http://jcvi.org/mpidb/about.php
	* BioGRID:	 		http://thebiogrid.org/
	* RegulonDB: 		http://regulondb.ccg.unam.mx/
	* STRING:	 		http://string-db.org/

License
==============================================

This software is licensed under the MIT license.

Copyright (c) 2013 Yo Sup Moon, Daniela Boernigen, Levi Waldron, Eric Franzosa, Xochitl Morgan, and Curtis Huttenhower

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
