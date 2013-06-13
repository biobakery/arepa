#!/usr/bin/env python
"""
ARepA: Automated Repository Acquisition 

ARepA is licensed under the MIT license.

Copyright (C) 2013 Yo Sup Moon, Daniela Boernigen, Levi Waldron, Eric Franzosa, Xochitl Morgan, and Curtis Huttenhower

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation 
files (the "Software"), to deal in the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons 
to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or 
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import arepa
import csv
import cfile
import re
import sys

c_iColumns = 6

def callback( aArgs, strA, strB, strMode, strAction, strActor, strScore ):
	hashScores = aArgs
	strA, strB = sorted( (strA, strB) )
	hashScores[(strA, strB)] = float(strScore) / 1000

if len( sys.argv ) != 2:
	raise Exception( "Usage: c2dat.py <taxid> < <stringc>" )
strTaxid = sys.argv[1]

hashScores = {}
cfile.read( sys.stdin,c_iColumns, strTaxid, callback, hashScores )
csvw = csv.writer( sys.stdout, csv.excel_tab )
for astrAB, dScore in hashScores.items( ):
	csvw.writerow( list(astrAB) + [dScore] )
