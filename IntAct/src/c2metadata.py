#!/usr/bin/env python

import cfile
import metadata
import sys
import csv 

c_iColumns	= 15

def metadatum( funcMetadata, astrTokens, iIndex ):

	for strTokens in astrTokens:
		setstrTokens = set()
		for strToken in strTokens.split( "|" ):
			astrToken = cfile.split( strToken )
			setstrTokens.add( astrToken[iIndex] or strToken )
		funcMetadata( setstrTokens )

def callback( pMetadata, strAs, strBs, strAltAs, strAltBs, strSynAs, strSynBs, strMethods, strAuthors, strPMIDs,
	strTaxAs, strTaxBs, strTypes, strDBs, strIDs, strConfs ):

	metadatum( pMetadata.taxid, [strTaxAs, strTaxBs], 1 )
	metadatum( pMetadata.pmid, [strPMIDs], 1 )
	metadatum( pMetadata.type, [strTypes.lower( )], 2 )
	metadatum( pMetadata.platform, [strMethods], 2 )

if len( sys.argv ) < 2:
	raise Exception( "Usage: c2metadata.py <id> < <intactc>" )

strTarget = sys.argv[1]
strStatus = sys.argv[2] if len(sys.argv[1:]) > 1 else None 


pMetadata = metadata.open( )
cfile.read( sys.stdin,c_iColumns, strTarget, callback, pMetadata )

if strStatus:
        strMapped, strBool = [x for x in csv.reader(open(strStatus),csv.excel_tab)][0]
        fMapped = True if strBool == "True" else False 
        pMetadata.set(strMapped, fMapped)
pMetadata.save( sys.stdout )
