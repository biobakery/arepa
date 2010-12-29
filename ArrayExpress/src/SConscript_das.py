#!/usr/bin/env python

import arepa
import os
import re
import subprocess
import sys
import zipfile

def test( iLevel, strTo, strFrom, pArgs ):
	strZIP = str(pArgs)
	if ( iLevel != 2 ) or ( not re.search( r'\.zip$', strZIP ) ):
		return False
	pZIP = zipfile.ZipFile( strZIP )
	for strName in pZIP.namelist( ):
		if strName.find( "sample_table" ) >= 0:
			return True
	return False
if locals( ).has_key( "testing" ):
	sys.exit( )

Import( "pE" )
c_strID					= arepa.cwd( )
c_fileIDTXT				= File( c_strID + ".txt" )
c_fileIDRawTXT			= File( c_strID + "_00raw.txt" )
c_fileIDRawPCL			= File( c_strID + "_01raw.pcl" )
c_fileIDNormPCL			= File( c_strID + "_02norm.pcl" )
c_fileIDPCL				= File( c_strID + ".pcl" )
c_fileIDDAB				= File( c_strID + ".dab" )
c_fileProgMergeTables	= File( arepa.d( arepa.path_arepa( ), arepa.c_strDirSrc, "merge_tables.py" ) ) 
c_fileProgSamples2PCL	= File( arepa.d( arepa.path_repo( pE ), arepa.c_strDirSrc, "samples2pcl.py" ) )
c_afileInputsSamples	= Glob( "../*sample_table*" )
c_strURL				= "ftp://ftp.ebi.ac.uk/pub/databases/microarray/data/array/"

pE.Import( "c_strType" )
pE.Import( "c_fileIDSDRF" )
sys.stderr.write( "THREE: %s\n" % [pE, locals( ).get( "c_fileIDSDRF" )] )

#===============================================================================
# Parse ADF IDs from SDRF and download
#===============================================================================

aastrSDRF = arepa.entable( open( c_fileIDSDRF.get_abspath( ) ), [lambda s: s == "Array Design REF"] )
setArrays = set(astrLine[0] for astrLine in aastrSDRF)
afileADFs = []
for strArray in setArrays:
	if not strArray:
		continue
	strFile = strArray + ".adf.txt"
	afileADFs.extend( arepa.download( pE, c_strURL + c_strType + "/" + strArray + "/" + strFile,
		arepa.d( arepa.path_repo( pE ), arepa.c_strDirData, strFile ) ) )

#===============================================================================
# Clip sample tables to first two columns
#===============================================================================

afileTables = []
for fileSample in c_afileInputsSamples:
	strTable = os.path.basename( str(fileSample) )
	def funcTable( target, source, env ):
		strT, astrSs = arepa.ts( target, source )
		return arepa.ex( "cut -f1-2 < " + astrSs[0], strT )
	afileTables.extend( pE.Command( strTable, fileSample, funcTable ) )

#===============================================================================
# Merge sample tables to raw text file
#===============================================================================

arepa.cmd( pE, c_fileProgMergeTables, c_fileIDRawTXT,
	[[True, fileCur] for fileCur in afileTables] )

#===============================================================================
# Calculate the final PCL + DAB
#===============================================================================

#- Map probe IDs and add PCL formatting
arepa.pipe( pE, c_fileIDRawTXT, c_fileProgSamples2PCL, c_fileIDRawPCL,
	[[True, fileCur] for fileCur in ( [c_fileIDSDRF] + afileADFs )] )

#- Normalize
c_iMaxLines = 100000
def funcIDNormPCL( target, source, env ):
	strT, astrSs = arepa.ts( target, source )
	strS = astrSs[0]
	strWC = arepa.check_output( "wc -l " + strS ).strip( ).split( )[0]
	return ( arepa.ex( "Normalizer -t pcl -T medmult < " + strS, strT )
		if ( int(strWC) < c_iMaxLines ) else arepa.ex( " ".join( ("ln -s", strS, strT) ) ) )
pE.Command( c_fileIDNormPCL, c_fileIDRawPCL, funcIDNormPCL )

#- Impute
arepa.spipe( pE, c_fileIDNormPCL, "KNNImputer", c_fileIDPCL )

#- PCL -> DAB
def funcIDDAB( target, source, env ):
	strT, astrSs = arepa.ts( target, source )
	return arepa.ex( "Distancer -o " + strT + " < " + astrSs[0] )
pE.Command( c_fileIDDAB, c_fileIDPCL, funcIDDAB )
pE.Default( c_fileIDDAB )
