#!/usr/bin/env python

import arepa
import cfile
import re
import sys

c_iColumns	= 15

def callback( aArgs, strAs, strBs, strAltAs, strAltBs, strSynAs, strSynBs, strMethods, strAuthors, strPMIDs,
	strTaxAs, strTaxBs, strTypes, strDBs, strIDs, strConfs ):

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
	if "-" not in astrAB:
		astrAB.append(strConfs.split( "intact-miscore:")[1])
		setPairs.add( tuple(astrAB) )


if len( sys.argv ) != 2:
	raise Exception( "Usage: c2txt.py <id> < <intactc>" )
strTarget = sys.argv[1]

mtch = re.search( 'taxid_(\d+)', strTarget )
if not mtch:
	raise Exception( "Illegal target: " + strTarget )
strTaxID = mtch.group( 1 )

setPairs = set()
cfile.read( sys.stdin,c_iColumns,strTarget, callback, [setPairs, strTaxID, {}] )
for astrGenes in setPairs:
	print( "\t".join( list(astrGenes) ) )
