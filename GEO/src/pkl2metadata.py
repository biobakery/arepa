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

pkl2metadata.py:

This script produces 2 tab-delimited tables:
one for the per-experiment metadata and 
one for the per-condition metadata
"""

import arepa 
import csv 
import sys
import metadata 

c_strCurated	= "curated"

if not(2 <= len(sys.argv[1:]) <= 3):				
	raise Exception("usage: pkl2metadata.py <ID.pkl> <per-exp.txt> [per-cond.txt]")
 
c_fileIDpkl, c_fileExpTable 	= sys.argv[1:3]
c_fileCondTable		    	= sys.argv[3] if len( sys.argv[1:] ) > 2 else None 

hashMeta = metadata.open( open( c_fileIDpkl, "r" ) ) 

def writeTable( hMeta, astrKeys, outputf, bIter = False ):
	hMeta = {k:hMeta[k] for k in astrKeys}
	csvw = csv.writer( open( outputf, "w" ), csv.excel_tab )
	if bIter:	
		astrHeader = hMeta.get("sample_name") or hMeta.get("")
		_astrKeys = [x for x in astrKeys if hMeta.get(x) != astrHeader]
		csvw.writerow( ["sample_name"] + _astrKeys )
		for iSample, strSample in enumerate(astrHeader):
			csvw.writerow( [str(x).replace("\n", " ") for x in [ strSample ] + [hMeta.get(s)[iSample] for s in \
			_astrKeys]]) 
	else:
		csvw.writerow( astrKeys )
		csvw.writerow( [str(x).replace("\n", " ") for x in [hMeta[k] for k in astrKeys]] )

#write per-experiment table 
astrExp = [k for k in list(hashMeta.keys()) if isinstance(hashMeta.get(k), str or int or float)] 
writeTable( hashMeta, astrExp, c_fileExpTable, False )

#write per-condition table
if c_fileCondTable:
	astrCond = [k for k in list(hashMeta.keys()) if isinstance(hashMeta.get(k), list) and \
        k != c_strCurated]
	writeTable( hashMeta, astrCond, c_fileCondTable, True )

