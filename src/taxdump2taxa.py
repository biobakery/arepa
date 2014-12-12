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
		print(( "\t".join( (strID, strTaxon) ) ))
