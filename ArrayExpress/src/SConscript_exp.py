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
c_strProcessedData	= "-processed-data-"
c_strURL			= "ftp://ftp.ebi.ac.uk/pub/databases/microarray/data/experiment/"
c_strTXT			= ".txt"

arepa.download( pE, c_strURL + c_strType + "/" + c_strID + "/" + os.path.basename( c_strFileIDZIP ),
	c_strFileIDZIP )
NoClean( c_strFileIDZIP )

arepa.download( pE, c_strURL + c_strType + "/" + c_strID + "/" + os.path.basename( c_strFileIDSDRF ),
	c_strFileIDSDRF )
NoClean( c_strFileIDSDRF )

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

def funcScanner( target, source, env, strFileZIP = c_strFileIDZIP ):
	for fileSource in source:
		for strLine in open( str(fileSource) ):
			env["sconscript_child"]( target, fileSource, env, strLine.strip( ),
				{"strFileZIP" : os.path.abspath( strFileZIP )} )
arepa.sconscript_children( pE, afileIDsTXT, funcScanner, 2 )
