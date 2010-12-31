#!/usr/bin/env python

import arepa
import metadata
import re
import sys

def metadatum( funcMetadata, astrValues ):

	for strValue in astrValues:
		funcMetadata( strValue )

strSDRF = sys.argv[1] if ( len( sys.argv ) > 1 ) else None
astrADFs = sys.argv[2:]
if strSDRF in ("-h", "-help", "--help"):
	raise Exception( "Usage: idf2txt.py [sdrf.txt] [adf.txt]+ < <idf.txt>" )

pMetadata = metadata.CMetadata( )
for strLine in sys.stdin:
	astrLine = strLine.strip( ).split( "\t" )
	if astrLine[0] == "PubMed ID":
		metadatum( pMetadata.pmid, astrLine[1:] )
	elif astrLine[0] == "Investigation Title":
		metadatum( pMetadata.title, astrLine[1:] )
	elif astrLine[0] == "Experiment Description":
		metadatum( pMetadata.gloss, astrLine[1:] )
	elif astrLine[0] == "Experimental Design":
		metadatum( pMetadata.type, [re.sub( r' by .+$', "", s.lower( ) ) for s in astrLine[1:]] )

if strSDRF:
	aastrSDRF = arepa.entable( open( strSDRF ), [
		lambda s: s == "Source Name",
		lambda s: re.search( r'Characteristics\s*\[Organism\]', s ),
	] )
	metadatum( pMetadata.conditions, [str(len( aastrSDRF ))] )
	setTaxa = set()
	for astrLine in aastrSDRF:
		strOrg = astrLine[1]
		setTaxa.add( arepa.org2taxid( strOrg ) or strOrg )
	metadatum( pMetadata.taxid, list(setTaxa) )

for strADF in astrADFs:
	for strLine in open( strADF ):
		astrLine = strLine.strip( ).split( "\t" )
		if astrLine[0] == "Array Design Name":
			metadatum( pMetadata.platform, astrLine[1:] )
pMetadata.save( sys.stdout )
