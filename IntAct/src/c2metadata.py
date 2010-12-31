#!/usr/bin/env python

import intact
import metadata
import sys

def metadatum( funcMetadata, astrTokens, iIndex ):

	for strTokens in astrTokens:
		for strToken in strTokens.split( "|" ):
			astrToken = intact.split( strToken )
			funcMetadata( astrToken[iIndex] or strToken )

def callback( pMetadata, strAs, strBs, strAltAs, strAltBs, strSynAs, strSynBs, strMethods, strAuthors, strPMIDs,
	strTaxAs, strTaxBs, strTypes, strDBs, strIDs, strConfs ):

	metadatum( pMetadata.taxid, [strTaxAs, strTaxBs], 1 )
	metadatum( pMetadata.pmid, [strPMIDs], 1 )
	metadatum( pMetadata.type, [strTypes.lower( )], 2 )
	metadatum( pMetadata.platform, [strMethods], 2 )

if len( sys.argv ) != 2:
	raise Exception( "Usage: c2metadata.py <id> < <intactc>" )
strTarget = sys.argv[1]

pMetadata = metadata.CMetadata( )
intact.read( sys.stdin, strTarget, callback, pMetadata )
pMetadata.save( sys.stdout )
