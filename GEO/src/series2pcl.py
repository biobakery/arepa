#!/usr/bin/env python

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
fFirst = True
for astrLine in csv.reader( sys.stdin ):
	if fFirst:
		fFirst = False
		astrHeader = astrLine[1:]
		for i in range( len( astrHeader ) ):
			strCur = hashMetadata.get( astrHeader[i] )
			if strCur:
				astrHeader[i] += ": " + strCur
		csvw.writerow( ["GID", "NAME", "GWEIGHT"] + astrHeader )
		csvw.writerow( ["EWEIGHT", "", ""] + ( [1] * len( astrHeader ) ) )
		continue
	strID, strName = hashPlatform.get( astrLine[0] ) or ( [astrLine[0]] * 2 )
	csvw.writerow( [strID, strName, "1"] + [( "" if ( s == "NA" ) else s ) for s in astrLine[1:]] )
