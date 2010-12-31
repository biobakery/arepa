#!/usr/bin/env python

import arepa
import gzip
import os
import re
import sys

def test( iLevel, strID, hashArgs ):
	return ( iLevel == 1 )
if locals( ).has_key( "testing" ):
	sys.exit( )

#Import( "pE" )
#Import( "hashArgs" )
c_strID					= arepa.cwd( )
c_strInputSConscript	= arepa.d( arepa.path_arepa( ), arepa.c_strDirSrc, "SConscript_pcl-dab.py" )
c_strFileIDTXT			= c_strID + ".txt"
c_strFileIDSOFTGZ		= c_strID + ".soft.gz"
c_strFileIDRawPCL		= c_strID + "_00raw.pcl"
c_strFileIDNormPCL		= c_strID + "_01raw.pcl"
c_strFileGPLsTXT		= "gpls.txt"
c_strProgSOFT2PCL		= arepa.d( arepa.path_repo( ), arepa.c_strDirSrc, "soft2pcl.py" )
c_strProgSOFT2TXT		= arepa.d( arepa.path_repo( ), arepa.c_strDirSrc, "soft2txt.py" )
c_strURL				= "ftp://ftp.ncbi.nih.gov/pub/geo/DATA/"
c_strURLData			= c_strURL + "SOFT/GDS/"
c_strURLPlatform		= c_strURL + "annotation/platforms/"

#===============================================================================
# Download SOFT file
#===============================================================================

arepa.download( pE, c_strURLData + c_strFileIDSOFTGZ )
NoClean( c_strFileIDSOFTGZ )

def funcGPLsTXT( target, source, env ):
	strT, astrSs = arepa.ts( target, source )
	setGPLs = set()
	for strLine in gzip.open( astrSs[0] ):
		mtch = re.search( r'^!dataset_platform\s*=\s*(\S+)', strLine )
		if mtch:
			setGPLs.add( mtch.group( 1 ) )
	with open( strT, "w" ) as fileOut:
		fileOut.write( "%s\n" % "\n".join( setGPLs ) )
	return None
afileGPLsTXT = Command( c_strFileGPLsTXT, c_strFileIDSOFTGZ, funcGPLsTXT )

def funcScannerGPLs( target, source, env ):
	afileGPLs = []
	for strLine in open( str(source[0]) ):
		afileGPL = arepa.download( env, c_strURLPlatform + strLine.strip( ) + ".annot.gz" )
		afileGPLs.extend( afileGPL )
# Locate here due to dependency on annotation files
	Command( c_strFileIDTXT, [c_strProgSOFT2TXT, c_strFileIDSOFTGZ] + afileGPLs, funcSOFT2 )
	Command( c_strFileIDRawPCL, [c_strProgSOFT2PCL, c_strFileIDSOFTGZ] + afileGPLs, funcSOFT2 )
	execfile( c_strInputSConscript )
afileGPLs = arepa.sconscript_children( pE, afileGPLsTXT, funcScannerGPLs, 2, funcGPLsTXT )

#===============================================================================
# Convert SOFT file with platform info to TXT and PCL
#===============================================================================

def funcSOFT2( target, source, env ):
	strT, astrSs = arepa.ts( target, source )
	strProg, strSOFTGZ, astrGPLGZs = astrSs[0], astrSs[1], astrSs[2:]
	return arepa.ex( " ".join( ("zcat", strSOFTGZ, "|", strProg, " ".join( astrGPLGZs )) ), strT )
