#!/usr/bin/env python

import csv
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
for astrLine in csv.reader( sys.stdin, csv.excel_tab ):
	strTmp, strID = astrLine[:2]
	strTaxon = strTmp.strip( )
	iLevel = len( strTmp ) - len( strTaxon )
	if iLevel <= iHit:
		iHit = None
	if strTaxon in setTaxa:
		iHit = iLevel
	if iHit != None:
		print( "\t".join( (strID, strTaxon) ) )
