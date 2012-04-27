#!/usr/bin/env python

import arepa
import sfle
import sys

def test( iLevel, strID, hashArgs ):
	return ( iLevel == 2 ) and ( strID.find( "GDS" ) == 0 ) 
if locals( ).has_key( "testing" ):
	sys.exit( )

c_strID						= arepa.cwd( )
astrID						= c_strID.split( "-" )
c_strGDS					= astrID[0]
c_strGPL					= astrID[1]

c_fileInputSConscript		= File( sfle.d( arepa.path_arepa( ), sfle.c_strDirSrc, "SConscript_pcl-dab.py" ) )
c_fileInputSOFTGZ			= File( "../" + c_strGDS + ".soft.gz" )

c_filePPfun                                     = File( sfle.d( arepa.path_repo( ), sfle.c_strDirEtc, "preprocess"))
c_strPPfun                                      = sfle.readcomment( c_filePPfun )[0]

c_fileIDPKL					= File( c_strID + ".pkl" )
c_fileGPLTXTGZ				= File( c_strGPL + ".annot.gz" )
c_fileIDRawPCL				= File( c_strID + "_00raw.pcl" )
c_fileEset                              = File( c_strID + ".RData" )

c_fileProgSOFT2PCL			= File( sfle.d( arepa.path_repo( ), sfle.c_strDirSrc, "soft2pcl.py" ) )
c_fileProgSOFT2Metadata		= File( sfle.d( arepa.path_repo( ), sfle.c_strDirSrc, "soft2metadata.py" ) )
c_fileProgProcessRaw            = File( sfle.d( arepa.path_repo( ), sfle.c_strDirSrc, "preprocessRaw.R" ) )

pE = DefaultEnvironment( )
Import( "hashArgs" )

#===============================================================================
# Convert SOFT file with platform info to TXT and PCL
#===============================================================================
def funcGetEset( target, source, env ):
        strT, astrSs = sfle.ts(target, source)
        strIn, strRData = astrSs[:2]
        return sfle.ex( (sfle.cat( strIn ), " | R --no-save --args", strRData, strT, c_strPPfun ) )

sfle.download( pE, hashArgs["c_strURLGPL"] + os.path.basename( str(c_fileGPLTXTGZ) ) )

sfle.pipe( pE, c_fileInputSOFTGZ, c_fileProgSOFT2Metadata, c_fileIDPKL,
	[[True, c_fileGPLTXTGZ]] )
#Default( c_fileIDPKL )

sfle.pipe( pE, c_fileInputSOFTGZ, c_fileProgSOFT2PCL, c_fileIDRawPCL,
	[[True, c_fileGPLTXTGZ]] )

Command( c_fileEset, [c_fileProgProcessRaw,c_fileIDRawPCL], funcGetEset )

execfile( str(c_fileInputSConscript) )
