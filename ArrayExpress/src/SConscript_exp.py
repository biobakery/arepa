#!/usr/bin/env python

import arepa
import os
import sys

def test( iLevel, strTo, strFrom, pArgs ):
	return ( iLevel == 1 )
if locals( ).has_key( "testing" ):
	sys.exit( )

c_strID				= arepa.cwd( )
c_strType			= c_strID[2:6]
c_fileIDZIP			= File( c_strID + ".processed.1.zip" )
c_fileIDSDRF		= File( c_strID + ".sdrf.txt" )
c_strProcessedData	= "-processed-data-"
c_strURL			= "ftp://ftp.ebi.ac.uk/pub/databases/microarray/data/experiment/"
c_strTXT			= ".txt"

Import( "pE" )

arepa.download( pE, c_strURL + c_strType + "/" + c_strID + "/" + os.path.basename( str(c_fileIDZIP) ),
	c_fileIDZIP )
pE.NoClean( c_fileIDZIP )

arepa.download( pE, c_strURL + c_strType + "/" + c_strID + "/" + os.path.basename( str(c_fileIDSDRF) ),
	c_fileIDSDRF )
pE.NoClean( c_fileIDSDRF )

def funcIDsTXT( target, source, env ):
	strT, astrSs = arepa.ts( target, source )
	strDir = os.path.dirname( strT )
	arepa.ex( " ".join( ("unzip", "-d", strDir, "-u", astrSs[0]) ) )
	with open( strT, "w" ) as fileOut:
		afileProcs = Glob( arepa.d( strDir, "*" + c_strProcessedData + "*" ) )
		if afileProcs:
			for fileProc in afileProcs:
				strID = str(fileProc).replace( c_strProcessedData, "_" ).replace( c_strTXT, "" )
				fileOut.write( "%s\n" % strID )
			return None
		afileSamples = Glob( arepa.d( strDir, "*sample_table*" ) )
		if afileSamples:
			fileOut.write( "%s\n" % ( c_strID + "_GSM" ) )
	return None
afileIDsTXT = pE.Command( c_strID + c_strTXT, c_fileIDZIP, funcIDsTXT )

def funcScanner( target, source, env, fileZIP = c_fileIDZIP ):
	for fileSource in source:
		for strLine in open( str(fileSource) ):
			env["sconscript_child"]( target, fileSource, env, strLine.strip( ), fileZIP )
sys.stderr.write( "TWO: %s\n" % [pE, locals( ).get( "c_fileIDSDRF" )] )
arepa.sconscript_children( pE, afileIDsTXT, funcScanner, 2, globals( ) )
