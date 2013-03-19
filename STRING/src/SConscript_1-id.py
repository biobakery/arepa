#!/usr/bin/env python

import arepa
import os
import sfle
import sys
import metadata
import glob


def test( iLevel, strID, hashArgs ):
	return ( iLevel == 1 )
if locals( ).has_key( "testing" ):
	sys.exit( )

pE = DefaultEnvironment( )


c_strID 			= arepa.cwd( )
c_fileInputC    		= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirTmp, "stringc" ) 

c_fileIDPKL             	= sfle.d( pE, c_strID + ".pkl" )
c_fileIDDAB           		= sfle.d( pE, c_strID + ".dab" )
c_fileIDQUANT           	= sfle.d( c_strID + ".quant" )
c_fileIDRawDAT             	= sfle.d( pE, c_strID + "_00raw.dat" )
c_fileIDDAT					= sfle.d( pE, c_strID + ".dat")

c_fileProgUnpickle		= sfle.d( pE, arepa.path_arepa( ), sfle.c_strDirSrc, "unpickle.py" )
c_fileProgC2Metadata		= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "c2metadata.py" )
c_fileProgC2DAT			= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "c2dat.py" )

c_fileInputSConscriptGM		= sfle.d( pE, arepa.path_arepa(),sfle.c_strDirSrc,"SConscript_genemapping.py")
c_fileInputSConscriptDAB	= sfle.d( pE, arepa.path_arepa(), sfle.c_strDirSrc, "SConscript_dat-dab.py" )

c_fileStatus	    	= sfle.d( pE, "status.txt" )
c_strGeneFrom		= None #we do not know a priori what the gene identifiers are going to be

afileIDDAT = sfle.pipe( pE, c_fileInputC, c_fileProgC2DAT, c_fileIDRawDAT, [c_strID] )

#Launch gene mapping 
execfile(str(c_fileInputSConscriptGM))

astrMapped = funcGeneIDMapping( pE, c_fileIDRawDAT, c_strGeneFrom, c_fileStatus )

#Make identifiers unique 
astrUnique = funcMakeUnique( pE, astrMapped[0] )

#Make metadata
afileIDTXT = sfle.pipe( pE, c_fileInputC, c_fileProgC2Metadata, c_fileIDPKL,[c_strID,[c_fileStatus]] )

execfile(str(c_fileInputSConscriptDAB))

#DAT to DAB
astrDAB = funcDAB( pE, c_fileIDDAB, [c_fileIDRawDAT, astrUnique[0]] )
funcPCL( pE, c_fileIDDAT, astrUnique[0] )
funcQUANT( pE, c_fileIDQUANT )
