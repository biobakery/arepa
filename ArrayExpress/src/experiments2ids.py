#!/usr/bin/env python

import arepa
import re
import sys

strTaxa = None if ( len( sys.argv ) <= 1 ) else sys.argv[1]

setTaxa = arepa.taxa( strTaxa, True )

setIDs = set()
for strLine in sys.stdin:
	mtch = re.search( 'accession\>([^<]+)\<.*species\>([^<]+)\<', strLine )
	if not mtch:
		continue
	strID, strTaxon = mtch.groups( )
	if strTaxon in setTaxa:
		setIDs.add( (strID, strTaxon) )
print( "\n".join( "\t".join( astrCur ) for astrCur in setIDs ) )
