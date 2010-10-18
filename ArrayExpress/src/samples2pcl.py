#!/usr/bin/env python

import arepa
import sys

def isprobe( strToken ):
	return ( strToken == "Reporter Name" )

def isgene( strToken ):
	return ( strToken.find( "GENE" ) >= 0 )

def istable( strToken ):
	return ( strToken == "Derived Array Data File" )

def issource( strToken ):
	return ( strToken == "Source Name" )

def isdesc( strToken ):
	return ( strToken.find( "escription" ) >= 0 )

strSDRF, astrADFs = sys.argv[1], sys.argv[2:]

hashSDRF = {}
aastrSDRF = arepa.entable( open( strSDRF ), [issource, istable, isdesc] )
for astrLine in aastrSDRF:
	strSource, strTable, strDesc = astrLine
	if strSource and strTable:
		hashSDRF[strTable] = (strSource, strDesc)

hashADFs = {}
for strADF in astrADFs:
	aastrADF = arepa.entable( open( strADF ), [isprobe, isgene] )
	for astrLine in aastrADF:
		strProbe, strGene = astrLine
		if strProbe and strGene:
			hashADFs[strProbe] = strGene

fFirst = True
for strLine in sys.stdin:
	astrLine = strLine.strip( ).split( "\t" )
	strID, astrData = astrLine[0], astrLine[1:]
	if fFirst:
		for i in range( len( astrData ) ):
			astrTo = hashSDRF.get( astrData[i] )
			astrData[i] = astrTo[0] + ( ( ": " + astrTo[1] ) if astrTo[1] else "" )
		astrData.insert( 0, "NAME" )
		astrData.insert( 1, "GWEIGHT" )
	else:
		astrData.insert( 0, strID )
		astrData.insert( 1, "1" )
		strID = hashADFs.get( strID, strID )
	print( "\t".join( [strID] + astrData ) )
	if fFirst:
		fFirst = False
		print( "EWEIGHT		" + ( "	1" * ( len( astrData ) - 2 ) ) )
