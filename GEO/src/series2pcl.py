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

if len( sys.argv ) != 3:
	raise Exception( "Usage: series2pcl.py <metadata.txt> <platform.txt> < <data.txt>" )
strMetadata, strPlatform = sys.argv[1:]

iProbe = iName = None
hashPlatform = {}
for astrLine in csv.reader( open( strPlatform ) ):
	if iProbe == None:
		for i in range( len( astrLine ) ):
			if astrLine[i] in ("Name", "SPOT_ID", "ID"):
				iProbe = i
				break
	if iName == None:
		for i in range( len( astrLine ) ):
			if astrLine[i] in ("GB_ACC", "ORF"):
				iName = i
				break
	if ( iProbe != None ) or ( iName != None ):
		# index = probe, name
		hashPlatform[astrLine[0]] = [astrLine[iProbe or 0], astrLine[iName or iProbe or 0]]

hashMetadata = {}
for astrLine in csv.reader( open( strMetadata ) ):
	# id = gloss
	hashMetadata[astrLine[0]] = astrLine[1]

csvw = csv.writer( sys.stdout, csv.excel_tab )
iLines = -1
for astrLine in csv.reader( sys.stdin ):
	iLines += 1
	if not iLines:
		astrHeader = astrLine[1:]
		for i in range( len( astrHeader ) ):
			strCur = hashMetadata.get( astrHeader[i] )
			if strCur:
				astrHeader[i] += ": " + strCur
		csvw.writerow( ["GID", "NAME", "GWEIGHT"] + astrHeader )
		csvw.writerow( ["EWEIGHT", "", ""] + ( [1] * len( astrHeader ) ) )
		continue
	strID, strName = hashPlatform.get( astrLine[0] ) or ( [astrLine[0]] * 2 )
	csvw.writerow( [strID, strName, 1] + [( "" if ( s == "NA" ) else s ) for s in astrLine[1:]] )
if not iLines:
	csvw.writerow( ["NULL", "", 1] + ( [None] * len( astrHeader ) ) )
