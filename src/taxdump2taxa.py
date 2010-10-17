#!/usr/bin/env python

import sys

if len( sys.argv ) != 2:
	raise Exception( "Usage: taxdump2taxa.py <taxa> < <taxdump.txt>" )
strTaxa = sys.argv[1]

setTaxa = set()
for strLine in open( strTaxa ):
	strLine = strLine.strip( )
	if ( not strLine ) or ( strLine[0] == "#" ):
		continue
	setTaxa.add( strLine )

iHit = None
for strLine in sys.stdin:
	strTmp, strID = strLine.rstrip( ).split( "\t" )
	strTaxon = strTmp.strip( )
	iLevel = len( strTmp ) - len( strTaxon )
	if iLevel <= iHit:
		iHit = None
	if strTaxon in setTaxa:
		iHit = iLevel
	if iHit != None:
		print( "\t".join( (strID, strTaxon) ) )
