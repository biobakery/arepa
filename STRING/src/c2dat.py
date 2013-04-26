#!/usr/bin/env python

import arepa
import csv
import cfile
import re
import sys

def callback( aArgs, strA, strB, strMode, strAction, strActor, strScore ):
	hashScores = aArgs
	strA, strB = sorted( (strA, strB) )
	hashScores[(strA, strB)] = float(strScore) / 1000

if len( sys.argv ) != 2:
	raise Exception( "Usage: c2dat.py <taxid> < <stringc>" )
strTaxid = sys.argv[1]

hashScores = {}
string1.read( sys.stdin, strTaxid, callback, hashScores )
csvw = csv.writer( sys.stdout, csv.excel_tab )
for astrAB, dScore in hashScores.items( ):
	csvw.writerow( list(astrAB) + [dScore] )
