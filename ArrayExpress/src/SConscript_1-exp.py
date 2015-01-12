#!/usr/bin/env python

import arepa
import os
import sfle
import sys

def test( iLevel, strID, hashArgs ):
	return ( iLevel == 1 )
if "testing" in locals( ):
	sys.exit( )

c_strID				= arepa.cwd( )
c_strType			= c_strID[2:6]
c_strSufTXT			= ".txt"
c_strProcessedData	= "-processed-data-"
c_strURL			= "ftp://ftp.ebi.ac.uk/pub/databases/microarray/data/"
c_strURLExp			= c_strURL + "experiment/"
c_strURLArray		= c_strURL + "array/"

c_fileIDZIP			= File( c_strID + ".processed.1.zip" )
c_fileIDSDRF		= File( c_strID + ".sdrf.txt" )
c_fileIDIDF			= File( c_strID + ".idf.txt" )
c_fileADFsTXT		= File( "adfs.txt" )

pE = DefaultEnvironment( )

#===============================================================================
# Download processed data file, SDRF, and ADF files
#===============================================================================

strURL = c_strURLExp + c_strType + "/"
for file in (c_fileIDZIP, c_fileIDSDRF, c_fileIDIDF):
	sfle.download( pE, strURL + c_strID + "/" + os.path.basename( str(file) ) )
	NoClean( file )

def funcADFsTXT( target, source, env ):
	strT, astrSs = sfle.ts( target, source )
	strIDSDRF = astrSs[0]
	with open( strT, "w" ) as fileOut:
		aastrSDRF = sfle.entable( open( strIDSDRF ), [lambda s: s == "Array Design REF"] )
		setArrays = set(astrLine[0] for astrLine in aastrSDRF)
		fileOut.write( "\n".join( [s for s in setArrays if s] ) )
	return None
afileADFsTXT = Command( c_fileADFsTXT, c_fileIDSDRF, funcADFsTXT )

def funcScannerADFs( target, source, env, strURL = c_strURLArray ):
	for strLine in open( str(source[0]) ):
		strArray = strLine.strip( )
		strType = strArray[2:6]
		afileADF = sfle.download( env, "/".join( (strURL, strType, strArray, strArray + ".adf.txt") ) )
		pE.Dictionary( ).setdefault( "adfs", [] ).extend( afileADF )
afileADFs = sfle.sconscript_children( pE, afileADFsTXT, funcScannerADFs, 2, arepa.c_strProgSConstruct, funcADFsTXT )

#===============================================================================
# Parse IDs from ZIP and recurse
#===============================================================================

def funcIDsTXT( target, source, env ):
	strT, astrSs = sfle.ts( target, source )
	strDir = os.path.dirname( os.path.abspath( strT ) )
	sfle.ex( ("unzip", "-d", strDir, "-u", astrSs[0]) )
	with open( strT, "w" ) as fileOut:
		afileProcs = Glob( sfle.d( strDir, "*" + c_strProcessedData + "*" ) )
		if afileProcs:
			for fileProc in afileProcs:
				strID = os.path.basename( str(fileProc) ).replace( c_strProcessedData, "_" ).replace( c_strSufTXT, "" )
				fileOut.write( "%s\n" % strID )
			return None
		afileSamples = Glob( sfle.d( strDir, "*sample_table*" ) )
		if afileSamples:
			fileOut.write( "%s\n" % ( c_strID + "_GSM" ) )
	return None
afileIDsTXT = Command( c_strID + c_strSufTXT, c_fileIDZIP, funcIDsTXT )

hashArgs = {
	"strFileZIP": c_fileIDZIP.get_abspath( ),
	"strFileIDSDRF": c_fileIDSDRF.get_abspath( ),
	"strFileIDIDF": c_fileIDIDF.get_abspath( ),
}
def funcScannerIDs( target, source, env, hashArgs = hashArgs ):
	afileADFs = pE.Dictionary( ).get( "adfs", [] )
	hashArgs["astrFileADFs"] = [f.get_abspath( ) for f in afileADFs]
	for strLine in open( str(source[0]) ):
		env["sconscript_child"]( target, source[0], env, strLine.strip( ), hashArgs, afileADFs )
sfle.sconscript_children( pE, afileIDsTXT + afileADFs, funcScannerIDs, 2, arepa.c_strProgSConstruct )
