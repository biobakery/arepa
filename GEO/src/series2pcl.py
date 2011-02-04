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
			if astrLine[i] in set(("Name", "SPOT_ID")):
				iProbe = i
				break
	if iName == None:
		for i in range( len( astrLine ) ):
			if astrLine[i] in set(("GB_ACC",)):
				iName = i
				break
	if ( iProbe != None ) or ( iName != None ):
# index = probe, name
		hashPlatform[astrLine[0]] = [astrLine[iProbe or 0], astrLine[iName or iProbe or 0]]

hashMetadata = {}
for astrLine in csv.reader( open( strMetadata ) ):
	# id = gloss
	hashMetadata[astrLine[0]] = astrLine[1]

fFirst = True
for astrLine in csv.reader( sys.stdin ):
	if fFirst:
		fFirst = False
		astrHeader = astrLine
		for i in range( len( astrHeader ) ):
			strCur = hashMetadata.get( astrHeader[i] )
			if strCur:
				astrHeader[i] += ": " + strCur
		print( "GID	NAME	GWEIGHT	" + "\t".join( astrHeader ) )
		print( "EWEIGHT		" + ( "	1" * len( astrHeader ) ) )
		continue
	astrID = hashPlatform.get( astrLine[0] )
	strID, strName = astrID if astrID else [astrLine[0], astrLine[0]]
	print( "\t".join( [strID, strName, "1"] + [( "" if ( s == "NA" ) else s ) for s in astrLine[1:]] ) )
