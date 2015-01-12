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
		if strName.find( "processed-data" ) >= 0:
			return True
	return False
if "testing" in locals( ):
	sys.exit( )

#Import( "pE" )
#Import( "hashArgs" )
c_strID						= arepa.cwd( )
c_strPrefix, c_strSuffix	= c_strID.split( "_" )
c_strType					= c_strID[2:6]
c_strInputIDSDRF			= hashArgs["strFileIDSDRF"]
c_astrInputADFs				= hashArgs["astrFileADFs"]
c_strInputSConscript		= arepa.d( arepa.path_arepa( ), arepa.c_strDirSrc, "SConscript_pcl-dab.py" )
c_strFileIDRawPCL			= c_strID + "_00raw.pcl"
c_strFileIDNormPCL			= c_strID + "_01norm.pcl"
c_strProgSamples2PCL		= arepa.d( arepa.path_repo( ), arepa.c_strDirSrc, "samples2pcl.py" )
c_fileInputData				= Glob( "../" + c_strPrefix + "*processed-data*" + c_strSuffix + "*" )[0]

#===============================================================================
# Calculate the final PCL + DAB
#===============================================================================

#- Map probe IDs and add PCL formatting
arepa.pipe( pE, c_fileInputData, c_strProgSamples2PCL, c_strFileIDRawPCL,
	[[True, s] for s in ( [c_strInputIDSDRF] + c_astrInputADFs )] )

exec(compile(open( c_strInputSConscript ).read(), c_strInputSConscript, 'exec'))
