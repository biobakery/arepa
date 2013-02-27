#!/usr/bin/env python

import re
import sys

#c_iColumns	= 6#15
c_iColumns	= 6

def split( strToken ):
	mtch = re.search( '^([^:]+):(.+)$', strToken )
	strType, strTmp = mtch.groups( ) if mtch else ("", strToken)
	mtch = re.search( '^(.+?)(?:\(([^)]+)\))?$', strTmp )
	strID, strGloss = mtch.groups( ) if mtch else (strTmp, "")
	return (strType, strID, strGloss)

def read( fileIntactC, strTarget, funcCallback, pArgs = None ):
	astrSymbols = []
	strID = fHit = None
	for strLine in fileIntactC:
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
			s = astrLine
			d=1
			aArgs = [pArgs] + map( lambda s: astrSymbols[int(s)], [s[0], s[1], d, d, d, d, d, d, s[4], s[1], s[2], s[3], s[5], d, d] )
			#aArgs = [pArgs] + map( lambda s: astrSymbols[int(s)], astrLine[:c_iColumns] )
			funcCallback( *aArgs )
