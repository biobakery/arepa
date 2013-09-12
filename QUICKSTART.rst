======================================================
ARepA QUICKSTART 
======================================================

..  This document follows reStructuredText syntax and conventions.
	You can compile this file to a PDF or HTML document.
	For instructions on how to do so, visit the reStructeredText webpage
	(http://docutils.sourceforge.net/rst.html).

Welcome to the quickstart tutorial to ARepA. You should always refer to the ARepA full README (http://huttenhower.sph.harvard.edu/arepa/manual) for a more thorough description of ARepA. Here, we will walkthrough a small toy example to get you used to ARepA's various functionalities. First, you should download and extract ARepA, making sure that all required dependencies are installed on your machine. It is highly recommended that Sleipnir (http://huttenhower.sph.harvard.edu/content/getting-started-sleipnir) is installed if you want the complete set of features available for ARepA. 


What is the ARepA build process?
==============================================

The `scons` command in the root directory of ARepA launches all processes across all submodules (repositories). For instructional purposes, however, ARepA is better understood by looking at the subcomponents of its complete build process. We will break down the build process into sequential components. 

1. Build components necessary for submodules
----------------------------------------------
For you to be able to fetch data from a certain repository, say Bacteriome, you will first need to tell ARepA to build certain components that are shared across all the repositories. This process only needs to be completed once per change in the taxonomy input. 

For this tutorial we will be getting E. coli data. This information can be inputted in the `etc/taxa` file :: 

	$ less etc/taxa 

	Homo sapiens
	Escherichia coli
	Mus musculus
	Saccharomyces cerevisiae
	Bacillus subtilis
	Pseudomonas aeruginosa

We will turn off all other organisms by writing a hash sign (#) before each line ::

	#Homo sapiens
	Escherichia coli
	#Mus musculus
	#Saccharomyces cerevisiae
	#Bacillus subtilis
	#Pseudomonas aeruginosa

Now, we will instruct ARepA to download all taxonomic information associated with E. coli ::

	$ scons -k tmp/

	scons: Reading SConscript files ...
	scons: done reading SConscript files.
	scons: Building targets ...
	funcDownload(["tmp/taxdump.tar.gz"], [])
	curl   -f -z /home/ysupmoon/hg/arepa/tmp/taxdump.tar.gz 'ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz' > "/home/ysupmoon/hg/arepa/tmp/taxdump.tar.gz"
	Warning: Illegal date format for -z, --timecond (and not a file name). 
	Warning: Disabling time condition. See curl_getdate(3) for valid date syntax.
	  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
	                                 Dload  Upload   Total   Spent    Left  Speed
	100 25.4M  100 25.4M    0     0   9.9M      0  0:00:02  0:00:02 --:--:-- 20.5M
	funcTaxdumpTXT(["tmp/taxdump.txt"], ["src/taxdump2txt.py", "tmp/taxdump.tar.gz"])
	tar -xzOf /home/ysupmoon/hg/arepa/tmp/taxdump.tar.gz names.dmp nodes.dmp | /home/ysupmoon/hg/arepa/src/taxdump2txt.py > "/home/ysupmoon/hg/arepa/tmp/taxdump.txt"
	funcPipe(["tmp/taxids"], ["src/taxdump2taxa.py", "tmp/taxdump.txt", "etc/taxa"])
	cat "/home/ysupmoon/hg/arepa/tmp/taxdump.txt" | /home/ysupmoon/hg/arepa/src/taxdump2taxa.py "/home/ysupmoon/hg/arepa/etc/taxa" > "/home/ysupmoon/hg/arepa/tmp/taxids"
	scons: done building targets.

The command "scons -k tmp/" instructs ARepA to only build files that will be saved in the `tmp` directory. Any output following "scons:" in the terminal signifies a message from the build process of ARepA (provided by SCons, a make-like software build tool that ARepA utilizes to handle its hierarchical dependency tracking). In particular, you will always see "scons: done building targets" after some process in ARepA has finished.

2. Build an external submodule
----------------------------------------------

An **internal** submodule is a submodule that is associated with a repository; this is where data handling for a specific repository is done (e.g. Bacteriome). An **external** submodule is one that performs significant tasks associated globally within ARepA. One such example is an external submodule that is dedicated to the standardization of gene identifiers ("gene mapping"). This module is the "GeneMapper" submodule. As before, a process can be launched by typing the "scons" command :: 

	$ cd GeneMapper 
	$ scons -k 

	scons: Reading SConscript files ...
	rm -f tmp/race.log
	scons: done reading SConscript files.
	scons: Building targets ...
	funcCheckoutTrunk(["tmp/checkout.log"], [])
	svn checkout -r 587 http://svn.bigcat.unimaas.nl/bridgedb/trunk/
	Checked out revision 587.
	sed -i.orig 's/^java -jar/java -Xmx4096m -jar/g' trunk/batchmapper.sh
	echo checked out OK > "/home/ysupmoon/hg/arepa/GeneMapper/tmp/checkout.log"
	funcCompileTrunk(["tmp/compile.log"], ["tmp/checkout.log"])
	ant -buildfile trunk/build.xml
	Buildfile: /home/ysupmoon/hg/arepa/GeneMapper/trunk/build.xml

	... 

When done, you will see the following output, as before ::

	scons: done building targets. 

We are ready to download files from a repository! 

3. Get data from Bacteriome 
----------------------------------------------

You should now be familiar with how you can launch a submodule. To get data from Bacteriome, simply (you guessed it) launch scons in the Bacteriome submodule :: 

	$ cd Bacteriome 
	$ scons -kj4 

Important: the `-k` flag ensures that ARepA continues to build when it encounters errors; the `-j4` flag tells ARepA to run 4 threads at once. 
In general, it is not adviseable to run more threads than the number of cores in the machine. For instance, if you have a dual-core processor, you would type `scons -kj2`. 

You should see the following output :: 

	$ cd data 
	$ ls 

	bacteriome_00raw.dat  bacteriome_00raw_mapped00.dat  bacteriome_00raw_mapped01.dat  bacteriome_00raw.quant  bacteriome.dat  bacteriome.pkl  status.txt

The final output data is always the name of the repository (or dataset) with either a `.dat` or `.pcl` extension. Output metadata is followed by a `.pkl` extension. Here we assume that Sleipnir is correctly installed on the machine. ::

	$ head -10 bacteriome.dat 

	UniRef90_P00561	UniRef90_A7ZH92	0.408408
	UniRef90_P00561	UniRef90_P00934	0.408408
	UniRef90_P00561	UniRef90_P0A9R0	0.408408
	UniRef90_A7ZH92	UniRef90_P00934	0.408408
	UniRef90_P00934	UniRef90_Q0T7R6	0.31006
	UniRef90_Q3Z606	UniRef90_P33570	0.320571
	UniRef90_P0AF04	UniRef90_A4W6D5	0.92
	UniRef90_P0AF04	UniRef90_P12281	0.271021
	UniRef90_P0AF04	UniRef90_P09152	0.271021
	UniRef90_P0AF04	UniRef90_P37411	0.87

What you see is a standardized and normalized pairwise gene network. A script in the root level of arepa can be used to view the metadata :: 

	$ python ../../src/unpickle.py bacteriome.pkl 

	title	Bacteriome
	url	http://www.compsysbio.org/bacteriome/dataset/combined_interactions.txt
	conditions	3888
	gloss	Bacterial Protein Interaction Database
	taxid	83333
	mapped	True
	type	protein interaction


We are ready for a more complex example. 

4. Get data from GEO 
----------------------------------------------

GEO is the most complex ARepA module, allowing for the construction of very flexible pipelines to download and process data. In particular, you can specify the names of GSE/GDS datasets without having to download the entirity of the datasets from that particular taxonomy (E. coli is the running example). Let's take a look at its configuration file :: 

	$ cd ../../GEO/etc
	$ less include 

	#------Model Organisms------

	#Mouse
	GDS640
	GSE22648

	#Yeast
	GDS104
	GSE10066

	#Ecoli
	GDS3123
	GSE12831

	#Pseudomonas
	GDS1910
	GSE36647

	#Human 
	GDS2250
	GSE6066
	GSE10183

	#Bacillus subtilis 
	GSE30000
	GSE30001

GEO by default downloads these sample datasets for six model organisms. Let's modify the file so that we only download "GDS3123", an E. coli dataset. As before, we can comment out the other datasets :: 

	#------Model Organisms------

	#Mouse
	#GDS640
	#GSE22648

	#Yeast
	#GDS104
	#GSE10066

	#Ecoli
	GDS3123
	#GSE12831

	#Pseudomonas
	#GDS1910
	#GSE36647

	#Human 
	#GDS2250
	#GSE6066
	#GSE10183

	#Bacillus subtilis 
	#GSE30000
	#GSE30001

Now, we can run scons on the root level of GEO ::

	$ cd ..
	$ scons -k

After the build has completed, take a look at the output :: 

	$ cd data
	$ ls 

	GDS3123

	$ cd GDS3123 
	$ ls 

	GDS3123-GPL199  GDS3123.soft.gz  GDS3123.txt  SConscript  SConstruct

ARepA organizes the GSE/GDS datasets by further separating them by platform (GPL199 is the only platform in this case). ::

	$ cd GDS3123-GPL199
	$ ls  

	GDS3123-GPL199_00raw_mapped00.pcl  GDS3123-GPL199_00raw.pcl         GDS3123-GPL199.map  GDS3123-GPL199.pkl      GPL199.annot.gz  SConscript  status.txt  GDS3123-GPL199_00raw_mapped01.pcl  GDS3123-GPL199_exp_metadata.txt  GDS3123-GPL199.pcl  GDS3123-GPL199_raw.map  platform.txt     SConstruct  taxa.txt

Now, as before, the final output files follow the same convention: `GDS3123-GPL199.pcl` is the final data output, and `GDS3123-GPL199.pkl` is the final metadata output. ::

	$ head -10 GDS3123-GPL199.pcl

	GID	NAME	GWEIGHT	Value for GSM247608: Exp_WT_rep1; src: Exponential growth of MG1655 wild type in LB at OD600 of 0.3	Value for GSM247612: Exp_WT_rep2; src: Exponential growth of MG1655 wild type in LB at OD600 of 0.3	Value for GSM247613: Exp_WT_rep3; src: Exponential growth of MG1655 wild type in LB at OD600 of 0.3	Value for GSM247614: Exp_rpoS_rep1; src: Exponential growth of MG1655 rpoS mutants in LB at OD600 of 0.3	Value for GSM247615: Exp_rpoS_rep2; src: Exponential growth of MG1655 rpoS mutants in LB at OD600 of 0.3	Value for GSM247616: Exp_rpoS_rep3; src: Exponential growth of MG1655 rpoS mutants in LB at OD600 of 0.3
	UniRef90_A7ZLK8	azoR	1	8.89555	8.77647	8.75413	8.91209	8.64127	8.80571
	UniRef90_A9MGY0	acpS	1	9.84225	9.82403	9.64156	9.52278	9.47872	9.61615
	UniRef90_A7ZIA4	frmA	1	10.8236	10.7661	10.7316	11.0447	11.0896	11.1802
	UniRef90_P39451	adhP	1	9.59428	9.71486	9.70127	9.10223	9.40085	9.40134
	UniRef90_P37009	afuC	1	9.29912	9.63063	9.15553	9.08512	8.86153	8.94394
	UniRef90_P33997	alpA	1	7.89904	8.53974	7.52528	6.78781	6.27701	6.89319
	UniRef90_P00811	ampC	1	9.35653	9.66537	9.16437	9.03056	8.46607	9.02675
	UniRef90_P0A9J4	panE	1	9.79544	9.75334	9.70425	9.69354	9.36834	9.53492
	UniRef90_P05052	appY	1	3.31578	3.7059	3.10876	2.77084	3.42425	0.34575

	$ python ../../../../src/unpickle.py GDS3123-GPL199.pkl
	title	Stress factor RpoS regulon in exponential-phase bacteria
	conditions	6
	gloss	Analysis of rpoS knockout mutants of bacteria K-12 strain MG1655 cells in exponential phase. RpoS, an alternative sigma factor and a stress response regulator, is a major regulator of genes required for stationary phase adaptation. Results provide insight into the role of RpoS in exponential phase.
	taxid	83333
	channels	1
	platform	GPL199
	mapped	True
	pmid	18158608
	type	expression profiling

To add more datasets to download, simply write it in the `etc/include` file. This concludes the quickstart tutorial. For a more thorough reference, consult the README. 

License
==============================================

This software is licensed under the MIT license.

Copyright (c) 2013 Yo Sup Moon, Daniela Boernigen, Levi Waldron, Eric Franzosa, Xochitl Morgan, and Curtis Huttenhower

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
