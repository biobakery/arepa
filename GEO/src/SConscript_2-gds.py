#!/usr/bin/env python

import arepa
import sfle
import sys
import re
import gzip

def test( iLevel, strID, hashArgs ):
	return ( iLevel == 2 ) and ( strID.find( "GDS" ) == 0 ) 
if locals( ).has_key( "testing" ):
	sys.exit( )

pE = DefaultEnvironment( )

c_strID				= arepa.cwd( )
astrID				= c_strID.split( "-" )
c_strGDS			= astrID[0]
c_strGPL			= astrID[1]

c_fileInputSConscript		= sfle.d( pE, arepa.path_arepa( ), sfle.c_strDirSrc, "SConscript_pcl-dab.py" ) 
c_fileInputSOFTGZ		= sfle.d( pE, "../" + c_strGDS + ".soft.gz" )
c_filePPfun			= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirEtc, "preprocess")
c_strPPfun 			= sfle.readcomment( c_filePPfun )[0]

c_fileStatus			= sfle.d( pE, "status.txt" )
c_fileIDMap			= sfle.d( pE, c_strID + ".map" )
c_fileIDMapRaw			= sfle.d( pE, c_strID + "_raw.map" )
c_fileIDPKL			= sfle.d( pE, c_strID + ".pkl" )
c_fileGPLTXTGZ			= sfle.d( pE, c_strGPL + ".annot.gz" )
c_fileIDRawPCL			= sfle.d( pE, c_strID + "_00raw.pcl" )
c_fileEset 			= sfle.d( pE, c_strID + ".RData" )

c_fileExpTable			= sfle.d( pE, c_strID + "_exp_metadata.txt" )

c_fileProgSOFT2PCL		= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "soft2pcl.py" ) 
c_fileProgSOFT2Metadata		= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "soft2metadata.py" ) 
c_fileProgProcessRaw		= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "preprocessRaw.R" ) 
c_fileProgAnnot2Map		= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "annot2map.py" ) 	
c_fileProgMergeMapping		= sfle.d( pE, arepa.path_arepa( ), sfle.c_strDirSrc, "merge_genemapping.py" )
c_fileProgPkl2Metadata		= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "pkl2metadata.py" ) 

Import( "hashArgs" )

#===============================================================================
# Convert SOFT file with platform info to TXT and PCL
#===============================================================================

def funcTaxID():
	astrMatch = re.findall( r'dataset_sample_organism = ([A-Za-z ]+)', 
		gzip.open( str(c_fileInputSOFTGZ), 'rb' ).read() )
	return ( arepa.org2taxid( astrMatch[0] ) if astrMatch else None )

#Download annotation files: in the case for GDS, GPLid is always included in name and always exists
sfle.download( pE, hashArgs["c_strURLGPL"] + os.path.basename( str( c_fileGPLTXTGZ ) ) )

#Produce pcl files 
sfle.pipe( pE, c_fileInputSOFTGZ, c_fileProgSOFT2PCL, c_fileIDRawPCL,
	[[c_fileGPLTXTGZ]] )

#Clean microarray data -- Impute, Normalize, Gene Mapping 
execfile( str(c_fileInputSConscript) )
funcPCL2DAB( pE, c_fileIDRawPCL, c_fileGPLTXTGZ, c_fileProgAnnot2Map, c_fileProgMergeMapping, funcTaxID() )

#Get metadata from soft file 
sfle.pipe( pE, c_fileInputSOFTGZ, c_fileProgSOFT2Metadata, c_fileIDPKL,
	[[c_fileStatus], [c_fileGPLTXTGZ]] )

#Create Tables 
sfle.sop( pE, "python", [[c_fileProgPkl2Metadata],[c_fileIDPKL],[True,c_fileExpTable]] )

#Produce expression set file
sfle.ssink( pE, str(c_fileProgProcessRaw), "R --no-save --args", [[c_fileIDRawPCL],[True,c_fileEset], c_strPPfun, [c_fileExpTable]])

