#!/usr/bin/env python

import arepa
import os
import subprocess
import sys

if __name__ == "__main__":
	iLevel, strTo, strFrom = arepa.scons_args( sys.argv )
	if iLevel != 2:
		sys.exit( 1 )
	sys.exit( subprocess.call( "unzip -l " + strFrom + " | grep sample_table",
		shell = True ) )

pE = Environment( )
c_strID					= arepa.dir( pE )
c_strType				= c_strID[2:6]
c_strFileIDTXT			= c_strID + ".txt"
c_strFileIDRawPCL		= c_strID + "_00raw.pcl"
c_strFileIDNormPCL		= c_strID + "_01norm.pcl"
c_strFileIDPCL			= c_strID + ".pcl"
c_strFileIDDAB			= c_strID + ".dab"
c_strInputIDSDRF		= str(( Glob( "../*.sdrf.txt" ) or [""] )[0])
c_strProgMergeTables	= arepa.path_arepa( ) + arepa.c_strSource + "merge_tables.py" 
c_strProgSamples2PCL	= arepa.path_repo( pE ) + arepa.c_strSource + "samples2pcl.py"
c_afileInputsSamples	= Glob( "../*sample_table*" )
c_strURL				= "ftp://ftp.ebi.ac.uk/pub/databases/microarray/data/array/"

#===============================================================================
# Parse ADF IDs from SDRF and download
#===============================================================================

aastrSDRF = arepa.entable( open( c_strInputIDSDRF ), [lambda s: s == "Array Design REF"] )
setArrays = set(astrLine[0] for astrLine in aastrSDRF)
afileADFs = []
for strArray in setArrays:
	if not strArray:
		continue
	strFile = strArray + ".adf.txt"
	afileADFs.extend( arepa.download( pE, strFile, c_strURL + c_strType + "/" +
		strArray + "/" + strFile ) )

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

arepa.cmd( pE, c_strProgMergeTables, c_strFileIDTXT,
	[[True, fileCur] for fileCur in afileTables] )

#===============================================================================
# Calculate the final PCL + DAB
#===============================================================================

#- Map probe IDs and add PCL formatting
arepa.pipe( pE, c_strFileIDTXT, c_strProgSamples2PCL, c_strFileIDRawPCL,
	[[True, fileCur] for fileCur in ( [c_strInputIDSDRF] + afileADFs )] )

#- Normalize
def funcIDNormPCL( target, source, env ):
	strT, astrSs = arepa.ts( target, source )
	return arepa.ex( "Normalizer -t pcl -T medmult < " + astrSs[0], strT )
c_iMaxLines = 100000
def funcIDNormPCLGate( target, source, env ):
	strT, astrSs = arepa.ts( target, source )
	strWC = arepa.check_output( "wc -l " + astrSs[0] ).strip( ).split( )[0]
	if int(strWC) > c_iMaxLines:
		target = None
		Default( astrSs[0] )
	return target, source
pBld = Builder( action = funcIDNormPCL, emitter = funcIDNormPCLGate )
pE.Append( BUILDERS = {"funcIDNormPCL" : pBld} )
pE.funcIDNormPCL( c_strFileIDNormPCL, c_strFileIDRawPCL )
#arepa.spipe( pE, c_strFileIDRawPCL, "Normalizer -t pcl -T medmult",
#	c_strFileIDNormPCL )

#- Impute
arepa.spipe( pE, c_strFileIDNormPCL, "KNNImputer", c_strFileIDPCL )

#- PCL -> DAB
def funcIDDAB( target, source, env ):
	strT, astrSs = arepa.ts( target, source )
	return arepa.ex( "Distancer -o " + strT + " < " + astrSs[0] )
pE.Command( c_strFileIDDAB, c_strFileIDPCL, funcIDDAB )

