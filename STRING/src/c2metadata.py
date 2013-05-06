#!/usr/bin/env python

import cfile
import metadata
import sys
import csv 

c_iColumns = 6


def metadatum( funcMetadata, astrTokens, iIndex ):

	for strTokens in astrTokens:
		setstrTokens = set()
		for strToken in strTokens.split( "|" ):
			astrToken = cfile.split( strToken )
			setstrTokens.add( astrToken[iIndex] or strToken )
		funcMetadata( setstrTokens )


def callback( pMetadata, strA, strB, strMode, strAction, strActor, strScore ):
	metadatum( pMetadata.taxid, [strTaxon], 1 )
	metadatum( pMetadata.mode, [strMode], 1 )

if len( sys.argv ) < 2:
	raise Exception( "Usage: c2metadata.py <taxid> [status.txt] < <stringc>" )
strTarget = sys.argv[1]
strStatus = sys.argv[2] if ( len(sys.argv[1:]) > 1 ) else None 
strTaxon = strTarget.split("_")[2]

pMetadata = metadata.open( )
cfile.read( sys.stdin,c_iColumns, strTarget, callback, pMetadata )

if strStatus:
	strMapped, strBool = [x for x in csv.reader(open(strStatus),csv.excel_tab)][0]
	fMapped = ( strBool == "True" )
	pMetadata.set( strMapped, fMapped )
pMetadata.save( sys.stdout )
