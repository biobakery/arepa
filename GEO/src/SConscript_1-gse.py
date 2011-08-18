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
c_strDatabaseURL 		= "ftp.ncbi.nih.gov"
c_strDatasetURL			= "pub/geo/DATA/SeriesMatrix/"
c_strURL				= "ftp://ftp.ncbi.nih.gov/pub/geo/DATA/"
c_strURLData			= c_strURL + "SeriesMatrix/"
c_strURLPlatform		= c_strURL + "annotation/platforms/"

# Need this for new revision 
c_strPlatformTXT		= "platforms.txt"
#==============================================================================
# Fetch platform count and recurse
#==============================================================================
def funcIDsTXT( target, source, env ):
	strT, astrSs = arepa.ts( target, source ) 
	list = arepa.ftppeak( c_strDatabaseURL, c_strDatasetURL, c_strID )
	def gplmodify( list, platform_list = None ):
		if not platform_list:
			platform_list = []
		if list == []:
			 pass
		elif list != []:
			if len( list ) == 1:
				for item in list:
					platform_list.append( re.findall( r"GSE\d+", item )[0] )
			elif len( list ) == 0:
				pass
			else:
				for item in list:
					platform_list.append(re.findall(r"GSE.*-GPL\d*", item)[0])
		return platform_list
	with open( strT, "w") as fileOut:
		for item in gplmodify( list ):
			fileOut.write( "%s\n" % item )
	return None 
afileIDsTXT = Command( c_strPlatformTXT, None, funcIDsTXT )

def funcScannerIDs( target, source, env ):
	for strLine in open( str(source[0]) ):
                env["sconscript_child"]( target, source[0], env, strLine.strip( ))
arepa.sconscript_children( pE, afileIDsTXT, funcScannerIDs, 2 )
	

