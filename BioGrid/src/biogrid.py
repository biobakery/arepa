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

import re
import csv
import sys


c_iColumns	= 15 

def split( strToken ):

	mtch = re.search( '^([^:]+):(.+)$', strToken )
	strType, strTmp = mtch.groups( ) if mtch else ("", strToken)
	mtch = re.search( '^(.+?)(?:\(([^)]+)\))?$', strTmp )
	strID, strGloss = mtch.groups( ) if mtch else (strTmp, "")
	
	return (strType, strID, strGloss)

def read( fileIntactC, strTarget, funcCallback, pArgs = None ):
	
	astrSymbols = []
	strID = fHit = None
	for strLine in fileIntactC:
		if strLine.startswith( ">" ):
			if fHit:
				break
			strID = strLine[1:].strip( )
		elif not strID:
			astrSymbols.append( strLine.strip( ) )
		elif strID == strTarget:
			fHit = True
			astrLine = strLine.strip( ).split( "\t" )
			if len( astrLine ) < c_iColumns:
				continue
			s = astrLine
			aArgs = [pArgs] + [astrSymbols [int(s)] for s in [s[7], s[8], s[9], s[10], s[1], s[2], 
		s[11], s[13], s[14], s[15], s[16], s[12], s[20], s[23], s[0]]]	
			funcCallback( *aArgs )

