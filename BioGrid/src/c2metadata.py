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

import cfile
import metadata
import sys
import csv

c_iColumns	= 18

def metadatum( funcMetadata, astrTokens, iIndex ):

	for strTokens in astrTokens:
		setstrTokens = set()
		for strToken in strTokens.split( "|" ):
			astrToken = cfile.split( strToken )
			setstrTokens.add( astrToken[iIndex] or strToken )
		funcMetadata( setstrTokens )


def callback( pMetadata, strAltAs , strAltBs , strSynAs , strSynBs , strSynAs2, strSynBs2, strAs, strBs, strAl, strSynAs3, strSynBs3, strMethods, strTypes,strAuthors, strPMIDs, strTaxAs, strTaxBs, strAl2): 

	metadatum( pMetadata.taxid, [strTaxAs], 1 )
	metadatum( pMetadata.pmid, [strPMIDs], 1 )
	metadatum( pMetadata.type, [strTypes.lower( )], 2 )
	metadatum( pMetadata.platform, [strMethods], 2 )

if len( sys.argv ) < 2:
	raise Exception( "Usage: c2metadata.py <id> < <biogridc.txt>" )
strTarget = sys.argv[1]
strStatus = sys.argv[2] if len(sys.argv[1:]) > 1 else None 


pMetadata = metadata.open( )
cfile.read( sys.stdin,c_iColumns, strTarget, callback, pMetadata )
if strStatus:
        strMapped, strBool = [x for x in csv.reader(open(strStatus),csv.excel_tab)][0]
        fMapped = True if strBool == "True" else False 
        pMetadata.set(strMapped, fMapped)
pMetadata.save( sys.stdout )
