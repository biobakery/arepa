#!/usr/bin/env python

import os
import re
import sys

astrTables = sys.argv[1:]

aastrHeaders = []
hashResults = {}
for iTable in range( len( astrTables ) ):
	fFirst = True
	for strLine in open( astrTables[iTable] ):
		astrLine = [strToken.strip( ) for strToken in strLine.split( "\t" )]
		astrData = astrLine[1:]
		if fFirst:
			fFirst = False
			aastrHeaders.append( astrData )
			continue
		aastrRow = hashResults.setdefault( astrLine[0], [] )
		if len( aastrRow ) <= iTable:
			aastrRow += [None] * ( 1 + iTable - len( aastrRow ) )
		aastrRow[iTable] = astrData

sys.stdout.write( "ID" )
for iTable in range( len( astrTables ) ):
	astrHeaders = [os.path.basename( astrTables[iTable] )] + aastrHeaders[iTable][1:]
	sys.stdout.write( "\t" + "\t".join( astrHeaders ) )
print( "" )

for strID, aastrData in hashResults.items( ):
	sys.stdout.write( strID )
	for iDatum in range( len( aastrHeaders ) ):
		astrData = aastrData[iDatum] if ( iDatum < len( aastrData ) ) else \
			None
		strData = "\t".join( astrData ) if astrData else \
			( "\t" * ( len( aastrHeaders[iDatum] ) - 1 ) )
		sys.stdout.write( "\t" + strData )
	print( "" )