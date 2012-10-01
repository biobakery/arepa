#!/usr/bin/env python

import arepa
import csv
import re
import sfle
import sys

c_strTaxid	= "mpidb_taxid_"
c_strPMID	= "pmid_"

def symbol( hashSymbols, strValue ):
	
	return hashSymbols.setdefault( strValue, len( hashSymbols ) )

if len( sys.argv ) < 2:
	raise Exception( "Usage: intact2c.py <min> [taxa] < <intact.txt>" )
iMin = int(sys.argv[1])
strTaxa = None if ( len( sys.argv ) <= 2 ) else sys.argv[2]

setTaxa = arepa.taxa( strTaxa )

hashSymbols = {}
hashhashPMTaxa = {}
for astrLine in csv.reader( sys.stdin, csv.excel_tab ):
	if astrLine and astrLine[0].startswith( "#" ):
		continue
	strPMID = sfle.regs( 'pubmed:(\d+)', astrLine[8], 1 )
	strTax1, strTax2 = (sfle.regs( 'taxid:(\d+)', strCur, 1 ) for strCur in
		astrLine[9:11])
	if not strTax1 or ( strTax1 != strTax2 ):
		strTax1 = "0"
	if setTaxa and ( strTax1 not in setTaxa ):
		continue
	hashhashPMTaxa.setdefault( strPMID, {} ).setdefault( strTax1, [] ).append(
		[symbol( hashSymbols, strCur ) for strCur in astrLine] )

aaSymbols = sorted( hashSymbols.items( ), cmp = lambda aOne, aTwo: cmp( aOne[1], aTwo[1] ) )
print( "\n".join( aCur[0] for aCur in aaSymbols ) )

hashBins = {}
for strPMID, hashTaxa in hashhashPMTaxa.items( ):
	for strTaxon, aaiLines in hashTaxa.items( ):
		strTaxid = c_strTaxid + strTaxon
		strBin = strTaxid + ( "" if ( ( not strPMID ) or ( len( aaiLines ) < iMin ) ) else \
			( "_" + c_strPMID + strPMID ) )
		hashBins.setdefault( strBin, [] ).extend( aaiLines )

for strBin, aaiLines in hashBins.items( ):
	print( ">" + strBin )
	for aiLine in aaiLines:
		print( "\t".join( str(i) for i in aiLine ) )
