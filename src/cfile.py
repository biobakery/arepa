#!/usr/bin/env python

import re
import sys

def split( strToken ):

	mtch = re.search( '^([^:]+):(.+)$', strToken )
	strType, strTmp = mtch.groups( ) if mtch else ("", strToken)
	mtch = re.search( '^(.+?)(?:\(([^)]+)\))?$', strTmp )
	strID, strGloss = mtch.groups( ) if mtch else (strTmp, "")
	return (strType, strID, strGloss)

def read( fileC, ncolumns, strTarget, funcCallback, pArgs = None ):

	astrSymbols = []
	strID = fHit = None
	for strLine in fileC:
		if strLine.startswith( ">" ):
			if fHit:
				break
			strID = strLine[1:].strip( )
		elif not strID:
			astrSymbols.append( strLine.strip( ) )
		elif strID == strTarget:
			fHit = True
			astrLine = strLine.strip( ).split( "\t" )
			if len( astrLine ) < ncolumns:
				continue
			aArgs = [pArgs] + map( lambda s: astrSymbols[int(s)], astrLine[:ncolumns] )
			funcCallback( *aArgs )
