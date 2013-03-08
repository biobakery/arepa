#!/usr/bin/env python 
''' 
Shared SConscript script to generate R package across all of arepa's modules 

R CMD BATCH build 

Requirements for R package building: 

* man/ directory with description files 
** .Rd files per dataset, and a master package file 
* data/ directory with matching .RData files 
* NAMESPACE file assigning rule to find names 

'''

import sfle 
import arepa 

c_strNAMESPACE		= r"'exportPattern(\\'^[[:alpha:]]+\\')'"
c_fileProgUnpickle	= sfle.d( pE, arepa.path_arepa(), sfle.c_strDirSrc, "unpickle.py" )

def funcCheckRStructure( pE, filePKL, fileNAMESPACE, fileManMaster, strNAMESPACE = c_strNAMESPACE ):
	'''
	Completes necessary components for R package building 
	Assumes that data/ and man/ directories have the corresponding data and manual files per dataset
	
	Input: 
	fileNAMESPACE = pointer to NAMESPACE file to be tracked 
	fileManMaster = pointer to the master manual file in man/ 
	
	'''
	# Make NAMESPACE File 
	return ( sfle.scmd( pE, "echo " + strNAMESPACE, fileNAMESPACE ) +
	# Make Master Man File 
		sfle.cmd( pE, c_fileProgUnpickle, fileManMaster, ["-x", filePKL] ) )

def funcMakeRPackage( pE, strDirectory, filePackageLog ):
	'''
	Compile the R package 
	
	Input: 
	strDirectory = directory to look in 
	filePackageLog = log file for scons to track 
	'''
	
	return ( sfle.sop( pE, "R CMD build", [strDirectory] ) +
		sfle.scmd( pE, "echo R package compiled OK", filePackageLog ) )
