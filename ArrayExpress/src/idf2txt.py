#!/usr/bin/env python

import arepa
import re
import sys

def enhash( hashOut, strID, astrValues ):

	setOut = None
	for strValue in astrValues:
		setOut = setOut or hashOut.setdefault( strID, set() )
		setOut.add( strValue )

if len( sys.argv ) < 2:
	raise Exception( "Usage: idf2txt.py <taxdump.txt> [sdrf.txt] [adf.txt]+ < <idf.txt>" )
strTaxa = sys.argv[1]
strSDRF = sys.argv[2] if ( len( sys.argv ) > 2 ) else None
astrADFs = sys.argv[3:]

hashTaxa = {}
for strLine in open( strTaxa ):
	strFrom, strTo = strLine.strip( ).split( "\t" )
	hashTaxa[strFrom] = strTo

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
		enhash( hashValues, "types", [re.sub( r' by .+$', "", s ) for s in astrLine[1:]] )

if strSDRF:
	aastrSDRF = arepa.entable( open( strSDRF ), [
		lambda s: s == "Source Name",
		lambda s: s == "Characteristics[Organism]",
	] )
	enhash( hashValues, "conditions", [str(len( aastrSDRF ))] )
	setTaxa = set()
	for astrLine in aastrSDRF:
		strOrg = astrLine[1]
		setTaxa.add( hashTaxa.get( strOrg, strOrg ) )
	enhash( hashValues, "taxids", list(setTaxa) )

for strADF in astrADFs:
	for strLine in open( strADF ):
		astrLine = strLine.strip( ).split( "\t" )
		if astrLine[0] == "Array Design Name":
			enhash( hashValues, "platform", astrLine[1:] )

for strKey, setValues in hashValues.items( ):
	print( "\t".join( (strKey, "|".join( setValues )) ) )
