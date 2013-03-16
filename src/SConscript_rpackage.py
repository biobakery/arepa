#!/usr/bin/env python 
''' 
Shared SConscript script to generate R package across all of arepa's modules 

R CMD BATCH build 

Requirements for R package building: 

* man/ directory with description files 
** .Rd files per dataset, and a master package file 
* data/ directory with matching .RData files 
* NAMESPACE file assigning rule to find names 
* DESCRIPTION file 
	/** example **/ 

	Package: curatedOvarianData
	Type: Package
	Title: Clinically Annotated Data for the Ovarian Cancer Transcriptome
	Version: 1.0.1
	Date: 2013-02-22
	Author: Benjamin F. Ganzfried, Markus Riester, Steve Skates, Victoria Wang, Thomas Risch, Benjamin Haibe-Kains, Svitlana Tyekucheva,
	Maintainer: Levi Waldron <levi@jimmy.harvard.edu>
	Description: The curatedOvarianData package provides data for gene expression analysis in patients with ovarian cancer.
	Depends: R (>= 2.10.0), affy
	Imports: BiocGenerics
	Suggests: survival, RUnit, metafor, genefilter, logging, sva, xtable
	License: Artistic-2.0
	URL: http://bcb.dfci.harvard.edu/ovariancancer
	biocViews: ExperimentData, Cancer, Ovarian, RNAExpressionData

'''

import sfle 
import arepa
import sys  
import pickle

c_strNAMESPACE		= r"'exportPattern(\\'^[[:alpha:]]+\\')'"

c_fileProgUnpickle	= sfle.d( pE, arepa.path_arepa(), sfle.c_strDirSrc, "unpickle.py" )

def funcCheckRStructure( pE, strDatasetName, filePKL, fileNAMESPACE, fileDESCRIPTION, fileManMaster, strNAMESPACE = c_strNAMESPACE ):
	'''
	Completes necessary components for R package building 
	Assumes that data/ and man/ directories have the corresponding data and manual files per dataset
	
	Input: 
	fileNAMESPACE = pointer to NAMESPACE file to be tracked 
	fileManMaster = pointer to the master manual file in man/ 
	'''

	def _makeDescription( target, source, env ):
		strT, astrSs = sfle.ts( target, source )
		pHash = pickle.load(open(astrSs[0]))
		pHashDescription	= { "Package": strDatasetName.replace("-","."), "Type": "Package", "Title": pHash.get("title"), 
		  						"Version": arepa.c_strVersion, "Author": ", ".join(arepa.c_astrAuthors), 
		 						"Date": arepa.c_strDate, "Maintainer": arepa.c_strMaintainer, 
								"Depends": "R (>= 2.10.0), affy", "Suggests": "survival", "URL": arepa.c_strURL,
								"License": arepa.c_strLicense, "Description": pHash.get("gloss") or " " }
		with open(strT, "w") as outputf:
			for k,v in pHashDescription.items():
				outputf.write( k + ": " + v + "\n" )
				
	def _makeMasterMan( target, source, env ):
		strT, astrSs = sfle.ts( target, source )
		pHash = pickle.load(open(astrSs[0]))
		def _metaStr( strDescription, strContent ):
			return "\\"+ strDescription + "{" + strContent + "}"
						
		strDataAccession = arepa.cwd( ) + "-package"
		strDataTitle = pHash.get( "title" ) or ""
		strDataGloss = pHash.get( "gloss" ) or ""
	
		aastrOut = [("name", strDataAccession),("title", strDataTitle),("description", strDataGloss)]
		
		with open( strT, "w" ) as outputf:
			for strDescription, strContent in aastrOut:
				outputf.write( _metaStr( strDescription, strContent ) + "\n" )
			#print _metaStr( strDescription, strContent )

	# Make NAMESPACE File 
	return ( sfle.scmd( pE, "echo " + strNAMESPACE, fileNAMESPACE ) +
	# Make DESCRIPTION File 
		Command( fileDESCRIPTION, filePKL, _makeDescription ) + 
	# Make Master Man File 
		Command( fileManMaster, filePKL, _makeMasterMan ) )


def funcMakeRPackage( pE, strDirectory, filePackageLog ):
	'''
	Compile the R package 
	
	Input: 
	strDirectory = directory to look in 
	filePackageLog = log file for scons to track 
	'''
	
	def _compileR( target, source, env ):
		strT, astrSs = sfle.ts( target, source )
		sfle.ex( ["chmod", "755", strDirectory] )
		sfle.ex( ["R","CMD","build", strDirectory] )
		with open( strT, "w" ) as outputf:
			outputf.write( "R package compiled OK")
	
	return pE.Command( filePackageLog, None, _compileR )
