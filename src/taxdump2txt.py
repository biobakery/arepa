#!/usr/bin/env python

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
