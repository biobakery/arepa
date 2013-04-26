#!/usr/bin/env python

import arepa
import csv
import re
import sfle
import sys

def symbol( hashSymbols, strValue ):
	return hashSymbols.setdefault( strValue, len( hashSymbols ) )

if len( sys.argv ) < 1:
	 raise Exception( "Usage: string2c.py [taxa] < <string.txt>" )
strTaxa = None if ( len( sys.argv ) <= 1 ) else sys.argv[1]

setTaxa = arepa.taxa( strTaxa )

hashSymbols = {}
hashTaxa = {}
fFirst = True
for astrLine in csv.reader( sys.stdin, csv.excel_tab ):
	if astrLine and astrLine[0].startswith( "#" ):
		continue
	if fFirst:
		fFirst = False
		continue
	strA, strB, strMode, strAction, strActor, strScore = astrLine
	strTax1, strTax2 = (re.sub( r'\..*$', "", s ) for s in (strA, strB))
	if not strTax1 or ( strTax1 != strTax2 ):
		strTax1 = "0"
	if setTaxa and ( strTax1 not in setTaxa ):
		continue
	strA, strB = (re.sub( r'^.*?\.', "", s ) for s in (strA, strB))
	hashTaxa.setdefault( strTax1, [] ).append( [symbol( hashSymbols, s ) for s in (strA, strB, strMode, strAction, strActor, strScore)] )

aaSymbols = sorted( hashSymbols.items( ), cmp = lambda aOne, aTwo: cmp( aOne[1], aTwo[1] ) )
print( "\n".join( aCur[0] for aCur in aaSymbols ) )

for strTaxon, aaiLines in hashTaxa.items( ):
	print( ">" + strTaxon )
	for aiLine in aaiLines:
		print( "\t".join( str(i) for i in aiLine ) )
