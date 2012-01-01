#!/usr/bin/env python

import arepa
import sfle
import sys

def test( iLevel, strID, hashArgs ):
	return ( iLevel == 2 ) and ( strID.find( "GSE" ) == 0 ) 
if locals( ).has_key( "testing" ):
	sys.exit( )

c_strID						= arepa.cwd( )

c_fileInputSConscript		= File( sfle.d( arepa.path_arepa( ), sfle.c_strDirSrc, "SConscript_pcl-dab.py" ) )
c_fileInputGSER				= File( sfle.d( arepa.path_repo( ), sfle.c_strDirSrc, "gse.R" ) )
c_fileInputManCurTXT		= File( sfle.d( arepa.path_repo( ), sfle.c_strDirEtc, "manual_curation/",
								c_strID + "_curated_pdata.txt" ) )

c_fileIDPKL					= File( c_strID + ".pkl" )
c_fileIDSeriesTXTGZ			= File( c_strID + "_series_matrix.txt.gz" )
c_fileRDataTXT				= File( c_strID + "_rdata.txt" )
c_fileRMetadataTXT			= File( c_strID + "_rmetadata.txt" )
c_fileRPlatformTXT			= File( c_strID + "_rplatform.txt" )
c_fileIDRawPCL				= File( c_strID + "_00raw.pcl" )

c_fileProgSeries2PCL		= File( sfle.d( arepa.path_repo( ), sfle.c_strDirSrc, "series2pcl.py" ) )
c_fileProgSeries2Metadata	= File( sfle.d( arepa.path_repo( ), sfle.c_strDirSrc, "series2metadata.py" ) )
c_fileProgSeries2Pickle		= File( sfle.d( arepa.path_repo( ), sfle.c_strDirSrc, "series2pickle.py" ) )

pE = DefaultEnvironment( )
Import( "hashArgs" )

#===============================================================================
# Download series matrix file
#===============================================================================

sfle.download( pE, hashArgs["c_strURLGSE"] + c_strID.split("-")[0] + "/" +
	os.path.basename( str(c_fileIDSeriesTXTGZ) ) )
NoClean( c_fileIDSeriesTXTGZ )

#===============================================================================
# Convert SERIES file with platform info to PKL and PCL
#===============================================================================

def funcGSER( target, source, env ):
	astrTs, astrSs = ([f.get_abspath( ) for f in a] for a in (target, source))
	strData, strMetadata, strPlatform = astrTs[:3]
	strProg, strSeriesGZ = astrSs[:2]
	return sfle.ex( (sfle.cat( strProg ), " | R --no-save --args", strSeriesGZ, strPlatform, strMetadata, strData) )
Command( [c_fileRDataTXT, c_fileRMetadataTXT, c_fileRPlatformTXT],
	[c_fileInputGSER, c_fileIDSeriesTXTGZ,], funcGSER )

sfle.pipe( pE, c_fileIDSeriesTXTGZ, c_fileProgSeries2Pickle, c_fileIDPKL,
	[[False, c_strID]] + ( [[True, c_fileInputManCurTXT]] if os.path.exists( str(c_fileInputManCurTXT) ) else [] ) )
Default( c_fileIDPKL )

sfle.pipe( pE, c_fileRDataTXT, c_fileProgSeries2PCL, c_fileIDRawPCL,
	[[True, f] for f in (c_fileRMetadataTXT, c_fileRPlatformTXT)] )

execfile( str(c_fileInputSConscript) )
