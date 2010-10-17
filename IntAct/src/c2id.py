#!/usr/bin/env python

import sys

if len( sys.argv ) != 2:
	raise Exception( "Usage: c2id.py <id> < <intactc>" )
strTarget = sys.argv[1]

astrSymbols = []
strID = fHit = None
for strLine in sys.stdin:
	if strLine.startswith( ">" ):
		if fHit:
			break
		strID = strLine[1:].strip( )
	elif not strID:
		astrSymbols.append( strLine.strip( ) )
	elif strID == strTarget:
		fHit = True
		astrLine = strLine.strip( ).split( "\t" )
		print( "\t".join( astrSymbols[int(strCur)] for strCur in astrLine ) )
