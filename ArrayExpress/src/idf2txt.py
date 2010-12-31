#!/usr/bin/env python

import arepa
import re
import sys

def enhash( hashOut, strID, astrValues ):

	setOut = None
	for strValue in astrValues:
		setOut = setOut or hashOut.setdefault( strID, set() )
		setOut.add( strValue )

strSDRF = sys.argv[1] if ( len( sys.argv ) > 1 ) else None
astrADFs = sys.argv[2:]
if strSDRF in ("-h", "-help", "--help"):
	raise Exception( "Usage: idf2txt.py [sdrf.txt] [adf.txt]+ < <idf.txt>" )

hashValues = {}
for strLine in sys.stdin:
	astrLine = strLine.strip( ).split( "\t" )
	if astrLine[0] == "PubMed ID":
		enhash( hashValues, "pmids", astrLine[1:] )
	elif astrLine[0] == "Investigation Title":
		enhash( hashValues, "title", astrLine[1:] )
	elif astrLine[0] == "Experiment Description":
		enhash( hashValues, "gloss", astrLine[1:] )
	elif astrLine[0] == "Experimental Design":
		enhash( hashValues, "types", [re.sub( r' by .+$', "", s.lower( ) ) for s in astrLine[1:]] )

if strSDRF:
	aastrSDRF = arepa.entable( open( strSDRF ), [
		lambda s: s == "Source Name",
		lambda s: re.search( r'Characteristics\s*\[Organism\]', s ),
	] )
	enhash( hashValues, "conditions", [str(len( aastrSDRF ))] )
	setTaxa = set()
	for astrLine in aastrSDRF:
		strOrg = astrLine[1]
		setTaxa.add( arepa.org2taxid( strOrg ) or strOrg )
	enhash( hashValues, "taxids", list(setTaxa) )

for strADF in astrADFs:
	for strLine in open( strADF ):
		astrLine = strLine.strip( ).split( "\t" )
		if astrLine[0] == "Array Design Name":
			enhash( hashValues, "platform", astrLine[1:] )

for strKey, setValues in hashValues.items( ):
	print( "\t".join( (strKey, "|".join( filter( lambda s: s, setValues ) )) ) )
