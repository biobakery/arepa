#!/usr/bin/env python

import arepa
import sfle
import sys

def test( iLevel, strID, hashArgs ):
	return ( iLevel == 2 ) and ( strID.find( "GDS" ) == 0 ) 
if locals( ).has_key( "testing" ):
	sys.exit( )

c_strID				= arepa.cwd( )
astrID				= c_strID.split( "-" )
c_strGDS			= astrID[0]
c_strGPL			= astrID[1]

c_fileInputSConscript	= File( sfle.d( arepa.path_arepa( ), sfle.c_strDirSrc, \
							"SConscript_pcl-dab.py" ) )
c_fileInputSOFTGZ	= File( "../" + c_strGDS + ".soft.gz" )
c_filePPfun			= File( sfle.d( arepa.path_repo( ), sfle.c_strDirEtc, "preprocess"))
c_strPPfun 			= sfle.readcomment( c_filePPfun )[0]

c_fileStatus		= File( "status.txt" )
c_fileIDMap			= File( c_strID + "_map.txt" )
c_fileIDPKL			= File( c_strID + ".pkl" )
c_fileGPLTXTGZ		= File( c_strGPL + ".annot.gz" )
c_fileIDRawPCL		= File( c_strID + "_00raw.pcl" )
c_fileEset 			= File( c_strID + ".RData" )

c_fileExpTable		= File( c_strID + "_exp_metadata.txt" )

c_fileProgSOFT2PCL	= File( sfle.d( arepa.path_repo( ), sfle.c_strDirSrc, \
						"soft2pcl.py" ) )
c_fileProgSOFT2Metadata	= File( sfle.d( arepa.path_repo( ), sfle.c_strDirSrc, \
							"soft2metadata.py" ) )
c_fileProgProcessRaw	= File( sfle.d( arepa.path_repo( ), sfle.c_strDirSrc, \
							"preprocessRaw.R" ) )
c_fileProgAnnot2Map		= File( sfle.d( arepa.path_repo( ), sfle.c_strDirSrc, \
							"annot2map.py" ) )	
c_fileProgPkl2Metadata	= File( sfle.d( arepa.path_repo( ), sfle.c_strDirSrc, \
							"pkl2metadata.py" ) )

pE = DefaultEnvironment( )
Import( "hashArgs" )

#===============================================================================
# Convert SOFT file with platform info to TXT and PCL
#===============================================================================

def funcMetaTable( target, source, env ):
	astrTs, astrSs = ([f.get_abspath( ) for f in a] for a in (target,source))
	strExp = astrTs[0]
	strProg, strPkl = astrSs[:2]
	return sfle.ex(("python", strProg, strPkl, strExp ))

def funcGetEset( target, source, env ):
	strT, astrSs = sfle.ts(target, source)
	strIn, strRData, strExpMetadata = astrSs[:3]
	return sfle.ex( (sfle.cat( strIn ), " | R --no-save --args", strRData, strT,
		c_strPPfun, strExpMetadata ) )

#Download annotation files: in the case for GDS, GPLid is always included in name and always exists
sfle.download( pE, hashArgs["c_strURLGPL"] + os.path.basename( str( c_fileGPLTXTGZ ) ) )

#Produce mapping files for gene mapping 
sfle.pipe( pE, c_fileGPLTXTGZ, c_fileProgAnnot2Map, c_fileIDMap )

#Get metadata from soft file 
sfle.pipe( pE, c_fileInputSOFTGZ, c_fileProgSOFT2Metadata, c_fileIDPKL,
	[[c_fileStatus], [c_fileGPLTXTGZ]] )

#Produce pcl files 
sfle.pipe( pE, c_fileInputSOFTGZ, c_fileProgSOFT2PCL, c_fileIDRawPCL,
	[[c_fileGPLTXTGZ]] )

#Create Tables 
Command( c_fileExpTable, [c_fileProgPkl2Metadata, c_fileIDPKL], funcMetaTable ) 

#Produce expression set file
Command( c_fileEset, [c_fileProgProcessRaw,c_fileIDRawPCL, c_fileExpTable], funcGetEset )

#Clean microarray data -- Impute, Normalize, Gene Mapping 
execfile( str(c_fileInputSConscript) )
