#!/usr/bin/env python

import arepa
import string1
import re
import sys

def callback( aArgs, strAs, strBs, strAltAs, strAltBs, strSynAs, strSynBs, strMethods, strAuthors, strPMIDs,     strTaxAs, strTaxBs, strDBs, strScores, strIDs, strConfs ):
     setPairs, strTaxID, hashCache = aArgs
     astrAB = []
     for astrCur in ([strAs, strAltAs, strSynAs], [strBs, strAltBs, strSynBs]):
          astrTokens = []
          for strTokens in astrCur:
               astrTokens += strTokens.split( "|" )
          strGene = None
          for strToken in astrTokens:
               strDBs, strID, strGloss = string1.split( strToken )
               strCur = hashCache.get( strID )
               if strCur == None:
                    strCur = hashCache[strID] = strID
               if strCur:
                    strGene = strCur
                    break
          astrAB.append( strGene or astrTokens[0] )
     strScores = str(float(strScores)/1000)
     astrAB.append(strScores) #Add scores 
     setPairs.add( tuple( astrAB ) )  

if len( sys.argv ) != 2:
    raise Exception( "Usage: c2txt.py <id> < <intactc>" )
strTarget = sys.argv[1]
mtch = re.search( 'taxid_(\d+)', strTarget )
if not mtch:
    raise Exception( "Illegal target: " + strTarget )
strTaxID = mtch.group( 1 )
setPairs = set()
string1.read( sys.stdin, strTarget, callback, [setPairs, strTaxID, {}] )
for astrGenes in setPairs:
    print( "\t".join( list(astrGenes)  ) ) 
