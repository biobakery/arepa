#!/usr/bin/env python

import arepa
import mpidb
import re
import sys

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
			strType, strID, strGloss = mpidb.split( strToken )
			strCur = hashCache.get( strID )
			if strCur == None:
				strCur = hashCache[strID] = strID
			if strCur:
				strGene = strCur
				break
		astrAB.append( strGene or astrTokens[0] )
	setPairs.add( tuple(sorted( astrAB )) )

if len( sys.argv ) != 2:
	raise Exception( "Usage: c2txt.py <id> < <intactc>" )
strTarget = sys.argv[1]

mtch = re.search( 'taxid_(\d+)', strTarget )
if not mtch:
	raise Exception( "Illegal target: " + strTarget )
strTaxID = mtch.group( 1 )

setPairs = set()
mpidb.read( sys.stdin, strTarget, callback, [setPairs, strTaxID, {}] )
for astrGenes in setPairs:
	sys.stdout.write( "\t".join( list(astrGenes) + ["1"] ) + "\n" )
