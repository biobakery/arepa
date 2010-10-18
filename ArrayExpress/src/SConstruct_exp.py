#!/usr/bin/env python

import arepa
import os
import sys

if __name__ == "__main__":
	iLevel, strTo, strFrom = arepa.scons_args( sys.argv )
	sys.exit( 0 if ( iLevel == 1 ) else 1 )

pE = Environment( )
c_strID				= arepa.dir( pE )
c_strType			= c_strID[2:6]
c_strFileIDZIP		= c_strID + ".processed.1.zip"
c_strFileIDSDRF		= c_strID + ".sdrf.txt"
c_strProcessedData	= "-processed-data-"
c_strURL			= "ftp://ftp.ebi.ac.uk/pub/databases/microarray/data/experiment/"
c_strTXT			= ".txt"

arepa.download( pE, c_strFileIDZIP, c_strURL + c_strType + "/" +
	c_strID + "/" + c_strFileIDZIP )
pE.NoClean( c_strFileIDZIP )

arepa.download( pE, c_strFileIDSDRF, c_strURL + c_strType + "/" +
	c_strID + "/" + c_strFileIDSDRF )
pE.NoClean( c_strFileIDSDRF )

def funcIDTMP( target, source, env ):
	strT, astrSs = arepa.ts( target, source )
	arepa.ex( " ".join( ("unzip", "-u", astrSs[0]) ) )
	afileProcs = Glob( "*" + c_strProcessedData + "*" )
	if afileProcs:
		for fileProc in afileProcs:
			strID = str(fileProc).replace( c_strProcessedData, "_" ).replace( c_strTXT, "" )
			arepa.sconstruct( env, strID, astrSs[0] )
		return
	afileSamples = Glob( "*sample_table*" )
	if afileSamples:
		arepa.sconstruct( env, c_strID + "_GSM", astrSs[0] )
pE.Command( c_strID + ".tmp", c_strFileIDZIP, funcIDTMP )
