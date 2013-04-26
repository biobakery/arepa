#!/usr/bin/env python

import re

c_iColumns	= 6

def split( strToken ):

	mtch = re.search( '^([^:]+):(.+)$', strToken )
	strType, strTmp = mtch.groups( ) if mtch else ("", strToken)
	mtch = re.search( '^(.+?)(?:\(([^)]+)\))?$', strTmp )
	strID, strGloss = mtch.groups( ) if mtch else (strTmp, "")
	return (strType, strID, strGloss)

def read( fileC, strTarget, funcCallback, pArgs = None ):
	
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
			if len( astrLine ) < c_iColumns:
				continue
			aArgs = [pArgs] + map( lambda s: astrSymbols[int(s)], astrLine[:c_iColumns] )
			funcCallback( *aArgs )
