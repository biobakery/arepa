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
import sfle
import sys

def print_tree( iID, aaiChildren, astrNames, iDepth ):

	if not astrNames[iID]:
		return
	print( ( " " * iDepth ) + astrNames[iID] + ( "\t%d" % iID ) )
	iDepth += 1
	aiChildren = aaiChildren[iID] if ( iID < len( aaiChildren ) ) else None
	for iChild in ( aiChildren or [] ):
		print_tree( iChild, aaiChildren, astrNames, iDepth )

astrNames = []
aaiChildren = []
setChildren = set()
for strLine in sys.stdin:
	astrLine = re.split( '\s*\|\s*', strLine.strip( ) )
	if len( astrLine ) == 5:
		strID, strName, strBlank, strType, strNull = astrLine
		if strType == "scientific name":
			iID = int(strID)
			sfle.aset( astrNames, iID, strName )
	else:
		iChild, iParent = (int(strCur) for strCur in astrLine[:2])
		if iChild == iParent:
			continue
		setChildren.add( iChild )
		aiChildren = sfle.aset( aaiChildren, iParent, None, False )
		if aiChildren == None:
			aaiChildren[iParent] = aiChildren = []
		aiChildren.append( iChild )

for i in range( len( astrNames ) ):
	if i not in setChildren:
		print_tree( i, aaiChildren, astrNames, 0 )
