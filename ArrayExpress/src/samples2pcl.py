#!/usr/bin/env python

import arepa
import re
import sys

def isprobe( strToken ):
	return ( strToken in ("Reporter Name", "Composite Element Name") )

def isgene( strToken ):
	return ( ( strToken.find( "GENE" ) >= 0 ) or
		( strToken == "Composite Element Database Entry[locus]" ) )

def istable( strToken ):
	return ( strToken in ("Derived Array Data File", "Derived Array Data Matrix File", "Scan Name") )

def issource( strToken ):
	return ( strToken == "Source Name" )

def isdesc( strToken ):
	return ( strToken.find( "escription" ) >= 0 )

def isorg( strToken ):
	return ( strToken.find( "[Organism]" ) >= 0 )

if len( sys.argv ) < 2:
	raise Exception( "Usage: samples2pcl.py <sdrf.txt> [adf.txt]+" )
strSDRF, astrADFs = sys.argv[1], sys.argv[2:]

strTaxID = None
hashSDRF = {}
aastrSDRF = arepa.entable( open( strSDRF ), [issource, istable, isdesc, isorg] )
for astrLine in aastrSDRF:
	strSource, strTable, strDesc, strOrg = astrLine
	if strSource and strTable:
		hashSDRF[strTable] = (strSource, strDesc)
		hashSDRF[strSource] = (strSource, strDesc)
	if strOrg and ( not strTaxID ):
		strTaxID = arepa.org2taxid( strOrg )

hashADFs = {}
for strADF in astrADFs:
	aastrADF = arepa.entable( open( strADF ), [isprobe, isgene, lambda x: x] )
	for astrLine in aastrADF:
		strProbe, strGene, strX = astrLine 
		if strProbe and strGene:
			hashADFs[strProbe] = strGene

hashCache = {}
fFirst = True
for strLine in sys.stdin:
	astrLine = strLine.strip( ).split( "\t" )
	strID, astrData = astrLine[0], astrLine[1:]
	if fFirst:
		if hashSDRF:
			for i in range( len( astrData ) ):
				strDatum = astrData[i]
				astrTo = hashSDRF.get( strDatum )
				if not astrTo:
					strDatum = re.sub( r'\.[^.]+$', "", strDatum )
					astrTo = hashSDRF.get( strDatum )
				if not astrTo:
					strDatum += " 1"
					astrTo = hashSDRF.get( strDatum )
				if astrTo:
					astrData[i] = astrTo[0] + ( ( ": " + astrTo[1] ) if astrTo[1] else "" )
				else:
					sys.stderr.write( "Data file not found in %s: %s\n" % (strSDRF, astrData[i]) )
		astrData.insert( 0, "NAME" )
		astrData.insert( 1, "GWEIGHT" )
	else:
		astrData.insert( 0, strID )
		astrData.insert( 1, "1" )
		strID = hashADFs.get( strID, re.sub( r'^.+:', "", strID ) )
		if strTaxID:
			strTmp = hashCache.get( strID )
			if strTmp == None:
				strID = hashCache[strID] = ( arepa.geneid( strID, strTaxID ) or strID )
			else:
				strID = strTmp
	print(( "\t".join( [strID] + astrData ) ))
	if fFirst:
		fFirst = False
		print(( "EWEIGHT		" + ( "	1" * ( len( astrData ) - 2 ) ) ))
