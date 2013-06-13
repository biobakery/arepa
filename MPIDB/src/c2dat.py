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
import cfile
import re
import sys

c_iColumns	= 16

def callback( aArgs, strAs, strBs, strAltAs, strAltBs, strSynAs, strSynBs, strMethods, strAuthors, strPMIDs,
	strTaxAs, strTaxBs, strTypes, strDBs, strIDs, strConfs, strScore ):

	setPairs, strTaxID, hashCache = aArgs
	astrAB = []
	for astrCur in ([strAs, strAltAs, strSynAs], [strBs, strAltBs, strSynBs]):
		astrTokens = []
		for strTokens in astrCur:
			astrTokens += strTokens.split( "|" )
		strGene = None
		for strToken in astrTokens:
			strType, strID, strGloss = cfile.split( strToken )
			strCur = hashCache.get( strID )
			if strCur == None:
				strCur = hashCache[strID] = strID
			if strCur:
				strGene = strCur
				break
		astrAB.append( strGene or astrTokens[0] )
	astrAB = sorted(astrAB)
	astrAB.append(str(float(strScore)/1000))
	setPairs.add( tuple(astrAB) )
	

if len( sys.argv ) != 2:
	raise Exception( "Usage: c2txt.py <id> < <intactc>" )
strTarget = sys.argv[1]

mtch = re.search( 'taxid_(\d+)', strTarget )
if not mtch:
	raise Exception( "Illegal target: " + strTarget )
strTaxID = mtch.group( 1 )

setPairs = set()
cfile.read( sys.stdin,c_iColumns, strTarget, callback, [setPairs, strTaxID, {}] )
for astrGenes in setPairs:
	sys.stdout.write( "\t".join( list(astrGenes) ) + "\n" )
