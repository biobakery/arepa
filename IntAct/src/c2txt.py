#!/usr/bin/env python

import intact
import sys

def enhash( hashOut, strID, astrTokens, iIndex ):

	setOut = None
	for strTokens in astrTokens:
		for strToken in strTokens.split( "|" ):
			setOut = setOut or hashOut.setdefault( strID, set() )
			astrToken = intact.split( strToken )
			setOut.add( astrToken[iIndex] or strToken )

def callback( hashHits, strAs, strBs, strAltAs, strAltBs, strSynAs, strSynBs, strMethods, strAuthors, strPMIDs,
	strTaxAs, strTaxBs, strTypes, strDBs, strIDs, strConfs ):

	enhash( hashHits, "taxids", [strTaxAs, strTaxBs], 1 )
	enhash( hashHits, "pmids", [strPMIDs], 1 )
	enhash( hashHits, "types", [strTypes], 2 )
	enhash( hashHits, "platforms", [strMethods], 2 )

if len( sys.argv ) != 2:
	raise Exception( "Usage: c2txt.py <id> < <intactc>" )
strTarget = sys.argv[1]

hashHits = {}
intact.read( sys.stdin, strTarget, callback, hashHits )
for strKey, setValues in hashHits.items( ):
	print( "\t".join( (strKey, "|".join( setValues )) ) )
