#!/usr/bin/env python

import csv
import os 
import sys
import sfle

def funcGetGSMids( infile ):
	aRet = [] 
	for astrLine in csv.reader( infile.read(), csv.excel_tab ):
		if not ( astrLine and astrLine[0] and ( astrLine[0][0] == "!" ) ):
			continue
		strFrom = astrLine[0][1:]
		if "Sample_supplementary_file" in strFrom:
			aRet += map (lambda x: os.path.basename(x) if \
				"CEL" in os.path.basename(x) else "#" + \
				os.path.basename(x), astrLine[1:])
		return aRet 
#Execute 
sys.stdout.write( "\n".join( funcGetGSMids( sys.stdin ) ) )
