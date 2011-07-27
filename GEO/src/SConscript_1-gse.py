#!/usr/bin/env python

import arepa
import gzip
import os
import re
import sys

def test( iLevel, strID, hashArgs ):
	return ( iLevel == 1 ) and ( strID.find( "GSE" ) == 0 )
if locals( ).has_key( "testing" ):
	sys.exit( )

#Import( "pE" )
#Import( "hashArgs" )
c_strID					= arepa.cwd( )
c_strInputSConscript	= arepa.d( arepa.path_arepa( ), arepa.c_strDirSrc, "SConscript_pcl-dab.py" )
c_strInputGSER			= arepa.d( arepa.path_repo( ), arepa.c_strDirSrc, "gse.R" )
c_strFileIDTXT			= c_strID + ".txt"
c_strFileIDSeriesTXTGZ	= c_strID + "_series_matrix.txt.gz"
c_strFileRDataTXT		= c_strID + "_rdata.txt"
c_strFileRMetadataTXT	= c_strID + "_rmetadata.txt"
c_strFileRPlatformTXT	= c_strID + "_rplatform.txt"
c_strFileIDRawPCL		= c_strID + "_00raw.pcl"
c_strFileIDNormPCL		= c_strID + "_01norm.pcl"
c_strProgSeries2PCL		= arepa.d( arepa.path_repo( ), arepa.c_strDirSrc, "series2pcl.py" )
c_strProgSeries2Metadata	= arepa.d( arepa.path_repo( ), arepa.c_strDirSrc, "series2metadata.py" )
c_strURL				= "ftp://ftp.ncbi.nih.gov/pub/geo/DATA/"
c_strURLData			= c_strURL + "SeriesMatrix/"
c_strURLPlatform		= c_strURL + "annotation/platforms/"

#===============================================================================
# Download series matrix file
#===============================================================================

arepa.download( pE, c_strURLData + c_strID + "/" + c_strFileIDSeriesTXTGZ )
NoClean( c_strFileIDSeriesTXTGZ )

#===============================================================================
# Convert SOFT file with platform info to TXT and PCL
#===============================================================================

def funcMETA2( target, source, env ):
        strT, astrSs = arepa.ts( target, source )
        strProg, strSeriesGZ = astrSs[0], astrSs[1]
        return arepa.ex( " ".join( ("zcat", strSeriesGZ, "|", strProg)), strT )

def funcGSER( target, source, env ):
	astrTs, astrSs = ([f.get_abspath( ) for f in a] for a in (target, source))
	strData, strMetadata, strPlatform = astrTs
	strProg, strSeriesGZ  = astrSs
	return arepa.ex( " ".join( ("R --no-save --args", strSeriesGZ, strPlatform, strMetadata, strData, "<", strProg) ) )
Command( [c_strFileRDataTXT, c_strFileRMetadataTXT, c_strFileRPlatformTXT],
	[c_strInputGSER, c_strFileIDSeriesTXTGZ,], funcGSER )
IDmetadata = Command( c_strFileIDTXT, [c_strProgSeries2Metadata, c_strFileIDSeriesTXTGZ], funcMETA2 )
Default(IDmetadata)

arepa.pipe( pE, c_strFileRDataTXT, c_strProgSeries2PCL, c_strFileIDRawPCL,
	[[True, c_strFileRMetadataTXT], [True, c_strFileRPlatformTXT]] )

execfile( c_strInputSConscript )


