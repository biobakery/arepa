#!/usr/bin/env python

import arepa
import os
import sys

def test( iLevel, strID, hashArgs ):
	return ( iLevel == 1 )
if locals( ).has_key( "testing" ):
	sys.exit( )

Import( "pE" )
c_strID				= arepa.cwd( )
c_strType			= c_strID[2:6]
c_strFileIDZIP		= c_strID + ".processed.1.zip"
c_strFileIDSDRF		= c_strID + ".sdrf.txt"
c_strFileIDIDF		= c_strID + ".idf.txt"
c_strFileADFsTXT	= "adfs.txt"
c_strProcessedData	= "-processed-data-"
c_strURL			= "ftp://ftp.ebi.ac.uk/pub/databases/microarray/data/"
c_strURLExp			= c_strURL + "experiment/"
c_strURLArray		= c_strURL + "array/"
c_strTXT			= ".txt"

#===============================================================================
# Download processed data file, SDRF, and ADF files
#===============================================================================

strURL = c_strURLExp + c_strType + "/"
arepa.download( pE, strURL + c_strID + "/" + os.path.basename( c_strFileIDZIP ) )
NoClean( c_strFileIDZIP )

arepa.download( pE, strURL + c_strID + "/" + os.path.basename( c_strFileIDSDRF ) )
NoClean( c_strFileIDSDRF )

arepa.download( pE, strURL + c_strID + "/" + os.path.basename( c_strFileIDIDF ) )
NoClean( c_strFileIDIDF )

def funcADFsTXT( target, source, env ):
	strT, astrSs = arepa.ts( target, source )
	strIDSDRF = astrSs[0]
	with open( strT, "w" ) as fileOut:
		aastrSDRF = arepa.entable( open( strIDSDRF ), [lambda s: s == "Array Design REF"] )
		setArrays = set(astrLine[0] for astrLine in aastrSDRF)
		fileOut.write( "\n".join( filter( lambda s: s, setArrays ) ) )
	return None
afileADFsTXT = Command( c_strFileADFsTXT, c_strFileIDSDRF, funcADFsTXT )

def funcScannerADFs( target, source, env, strURL = c_strURLArray + c_strType + "/" ):
	for strLine in open( str(source[0]) ):
		strArray = strLine.strip( )
		afileADF = arepa.download( env, strURL + strArray + "/" + strArray + ".adf.txt" )
		pE.Dictionary( ).setdefault( "adfs", [] ).extend( afileADF )
afileADFs = arepa.sconscript_children( pE, afileADFsTXT, funcScannerADFs, 2, funcADFsTXT )

#===============================================================================
# Parse IDs from ZIP and recurse
#===============================================================================

def funcIDsTXT( target, source, env ):
	strT, astrSs = arepa.ts( target, source )
	strDir = os.path.dirname( os.path.abspath( strT ) )
	arepa.ex( " ".join( ("unzip", "-d", strDir, "-u", astrSs[0]) ) )
	with open( strT, "w" ) as fileOut:
		afileProcs = Glob( arepa.d( strDir, "*" + c_strProcessedData + "*" ) )
		if afileProcs:
			for fileProc in afileProcs:
				strID = os.path.basename( str(fileProc) ).replace( c_strProcessedData, "_" ).replace( c_strTXT, "" )
				fileOut.write( "%s\n" % strID )
			return None
		afileSamples = Glob( arepa.d( strDir, "*sample_table*" ) )
		if afileSamples:
			fileOut.write( "%s\n" % ( c_strID + "_GSM" ) )
	return None
afileIDsTXT = Command( c_strID + c_strTXT, c_strFileIDZIP, funcIDsTXT )

hashArgs = {
	"strFileZIP"	: os.path.abspath( c_strFileIDZIP ),
	"strFileIDSDRF"	: os.path.abspath( c_strFileIDSDRF ),
	"strFileIDIDF"	: os.path.abspath( c_strFileIDIDF ),
}
def funcScannerIDs( target, source, env, hashArgs = hashArgs ):
	afileADFs = pE.Dictionary( ).get( "adfs", [] )
	hashArgs["astrFileADFs"] = [f.get_abspath( ) for f in afileADFs]
	for strLine in open( str(source[0]) ):
		env["sconscript_child"]( target, source[0], env, strLine.strip( ), hashArgs, afileADFs )
arepa.sconscript_children( pE, afileIDsTXT + afileADFs, funcScannerIDs, 2 )
