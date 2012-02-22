#!/usr/bin/env python

import biogrid
import metadata
import sys

def metadatum( funcMetadata, astrTokens, iIndex ):

	for strTokens in astrTokens:
		setstrTokens = set()
		for strToken in strTokens.split( "|" ):
			astrToken = biogrid.split( strToken )
			setstrTokens.add( astrToken[iIndex] or strToken )
		funcMetadata( setstrTokens )

def callback( pMetadata, strAs, strBs, strAltAs, strAltBs, strSynAs, strSynBs, strMethods, strAuthors, strPMIDs,
	strTaxAs, strTaxBs, strTypes, strDBs, strIDs, strConfs ):

	metadatum( pMetadata.taxid, [strTaxAs, strTaxBs], 1 )
	metadatum( pMetadata.pmid, [strPMIDs], 1 )
	metadatum( pMetadata.type, [strTypes.lower( )], 2 )
	metadatum( pMetadata.platform, [strMethods], 2 )

if len( sys.argv ) != 2:
	raise Exception( "Usage: c2metadata.py <id> < <biogridc.txt>" )
strTarget = sys.argv[1]

pMetadata = metadata.open( )
biogrid.read( sys.stdin, strTarget, callback, pMetadata )
pMetadata.save( sys.stdout )
