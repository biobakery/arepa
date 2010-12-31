#!/usr/bin/env python

import arepa
import os
import re
import sys
import zipfile

def test( iLevel, strID, hashArgs ):
	strZIP = hashArgs.get( "strFileZIP", "" )
	if ( iLevel != 2 ) or ( not re.search( r'\.zip$', strZIP ) ):
		return False
	pZIP = zipfile.ZipFile( strZIP )
	for strName in pZIP.namelist( ):
		if strName.find( "sample_table" ) >= 0:
			return True
	return False
if locals( ).has_key( "testing" ):
	sys.exit( )

#Import( "pE" )
#Import( "hashArgs" )
c_strID					= arepa.cwd( )
c_strType				= c_strID[2:6]
c_strInputIDSDRF		= hashArgs["strFileIDSDRF"]
c_astrInputADFs			= hashArgs["astrFileADFs"]
c_strInputSConscript	= arepa.d( arepa.path_arepa( ), arepa.c_strDirSrc, "SConscript_pcl-dab.py" )
c_strFileIDRawTXT		= c_strID + "_00raw.txt"
c_strFileIDRawPCL		= c_strID + "_01raw.pcl"
c_strFileIDNormPCL		= c_strID + "_02norm.pcl"
c_strFileIDPCL			= c_strID + ".pcl"
c_strFileIDDAB			= c_strID + ".dab"
c_strProgMergeTables	= arepa.d( arepa.path_arepa( ), arepa.c_strDirSrc, "merge_tables.py" ) 
c_strProgSamples2PCL	= arepa.d( arepa.path_repo( ), arepa.c_strDirSrc, "samples2pcl.py" )
c_afileInputSamples		= Glob( "../*sample_table*" )

#===============================================================================
# Clip sample tables to first two columns
#===============================================================================

afileTables = []
for fileSample in c_afileInputSamples:
	strTable = os.path.basename( str(fileSample) )
	def funcTable( target, source, env ):
		strT, astrSs = arepa.ts( target, source )
		return arepa.ex( "cut -f1-2 < " + astrSs[0], strT )
	afileTables.extend( Command( strTable, fileSample, funcTable ) )

#===============================================================================
# Merge sample tables to raw text file
#===============================================================================

arepa.cmd( pE, c_strProgMergeTables, c_strFileIDRawTXT,
	[[True, fileCur] for fileCur in afileTables] )

#===============================================================================
# Calculate the final PCL + DAB
#===============================================================================

#- Map probe IDs and add PCL formatting
arepa.pipe( pE, c_strFileIDRawTXT, c_strProgSamples2PCL, c_strFileIDRawPCL,
	[[True, s] for s in ( [c_strInputIDSDRF] + c_astrInputADFs )] )

execfile( c_strInputSConscript )
