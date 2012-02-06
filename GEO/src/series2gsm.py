#!/usr/bin/env python

import csv
import sys
import re

def _stripquotes( strIn ):

        mtch = re.search( r'^"(.*)"$', strIn )
        if mtch:
                strIn = mtch.group( 1 )
        return strIn

for astrLine in csv.reader( sys.stdin, csv.excel_tab ):
        if not ( astrLine and astrLine[0] and ( astrLine[0][0] == "!" ) ):
                continue
        strFrom = astrLine[0][1:]

        if strFrom == 'Sample_geo_accession':
		print( "\n".join( astrLine[1:]  ) )

