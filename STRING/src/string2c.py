#!/usr/bin/env python
"""
ARepA: Automated Repository Acquisition 

ARepA is licensed under the MIT license.

Copyright (C) 2013 Yo Sup Moon, Daniela Boernigen, Levi Waldron, Eric Franzosa, Xochitl Morgan, and Curtis Huttenhower

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation 
files (the "Software"), to deal in the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons 
to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or 
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import arepa
import csv
import re
import sfle
import sys

c_repo 		= arepa.cwd()
c_strTaxid	= c_repo+"_taxid_"
c_strMode	= "mode_"


def symbol( hashSymbols, strValue ):
	return hashSymbols.setdefault( strValue, len( hashSymbols ) )

if len( sys.argv ) < 1:
	 raise Exception( "Usage: string2c.py [taxa] < <string.txt>" )
iMin = int(sys.argv[1])
strTaxa = None if ( len( sys.argv ) <= 2 ) else sys.argv[2]

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
	hashTaxa.setdefault(strMode, {}).setdefault( strTax1, [] ).append( [symbol( hashSymbols, s ) for s in (strA, strB, strMode, strAction, strActor, strScore)] )

aaSymbols = sorted( hashSymbols.items( ), cmp = lambda aOne, aTwo: cmp( aOne[1], aTwo[1] ) )
print( "\n".join( aCur[0] for aCur in aaSymbols ) )

#for strTaxon, aaiLines in hashTaxa.items( ):
#	print( ">" + c_strTaxid + strTaxon )
#	for aiLine in aaiLines:
#		print( "\t".join( str(i) for i in aiLine ) )

hashBins = {}
for strMode, hashTaxa in hashTaxa.items( ):
	for strTaxon, aaiLines in hashTaxa.items( ):
		strTaxid = c_strTaxid + strTaxon
		strBin = strTaxid + ( "" if ( ( not strMode ) or ( len( aaiLines ) < iMin ) ) else \
			 ( "_" + c_strMode + strMode ) )
		hashBins.setdefault( strBin, [] ).extend( aaiLines )

for strBin, aaiLines in hashBins.items( ):
	print( ">" + strBin )
	for aiLine in aaiLines:
		print( "\t".join( str(i) for i in aiLine ) )
