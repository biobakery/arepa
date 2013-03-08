#!/usr/bin/env python
'''
Shared utility for magic functions within
gene mapper 
'''

import arepa
import os
import sys 
import sfle 
import pickle 
import itertools 
import re 
import glob 

g_iterCounter			= itertools.count(0) 

c_strID 				= arepa.cwd( )
c_strPathRepo			= arepa.name_repo( )
c_strSufMap 			= ".map" 
c_strMapped				= "_mapped" 
c_strDirData			= sfle.d( arepa.path_repo( ), sfle.c_strDirData )
c_strDirManMap			= sfle.d( arepa.path_repo( ), sfle.c_strDirEtc, "manual_mapping" )
c_astrGeneTo			= sfle.readcomment( sfle.d( arepa.path_arepa(),sfle.c_strDirEtc,"geneid" ) 
							or [arepa.genemap_genename( )] ) 
c_strPathGeneMapper		= sfle.d( arepa.path_arepa(), "GeneMapper" )
c_strPathTopMapping		= sfle.d( c_strPathGeneMapper, sfle.c_strDirEtc, "manual_mapping" )
c_strPathUniprotKO		= sfle.d( c_strPathGeneMapper, sfle.c_strDirEtc, "uniprotko" )
c_fileProgMakeUnique	= sfle.d( arepa.path_arepa(), sfle.c_strDirSrc,"makeunique.py")
c_funcGeneMapper		= sfle.d( c_strPathGeneMapper, sfle.c_strDirSrc, "bridgemapper.py" )

c_strManualGeneIDs		= sfle.d( arepa.path_repo( ), sfle.c_strDirEtc, "manual_geneid")

c_pHashBridgeDB 		= dict((strName, sfle.d( arepa.path_arepa( ), "GeneMapper", sfle.c_strDirEtc, strDB )) 
							for strName, strDB in (
							("Homo sapiens",		"Hs_Derby_20120602.bridge"),
							("Mus musculus",		"Mm_Derby_20120602.bridge"),
							("Saccharomyces cerevisiae",	"Sc_Derby_20120602.bridge"),
								))

pHashBridgeDBTaxIDs 	= { k:arepa.org2taxid( k, True ) for k in c_pHashBridgeDB.keys()}
m_hashGeneIDs			= { k:v for k,v in map( lambda x: x.split("\t"), 
							sfle.readcomment(open(c_strManualGeneIDs)) ) }

def funcCounter( iter ):
	return ( "%02d" % next( iter ) )

def funcGeneIDMapping( pE, fileDATin, strGeneFrom = None, fileLOGout = None, strMAPin = None, aiCOL = [0,1], iSkip = 0, iLevel = 2):
	try:
		int(strMAPin)
		strTaxID, strMAPin = strMAPin, None
	except (ValueError, TypeError):
		strTaxID = None
	# Try to find taxid 
	if not strTaxID:
		astrMatch = re.findall( r'taxid_([0-9]+)', c_strID )
		strTaxID = astrMatch[0].strip( ) if astrMatch else None		
	if not strGeneFrom: 
		#if strGeneFrom is not specified, try to retrieve it from
		#the "manual_geneids.txt" file in the respective etc directory, else None 
		#this problem tends to arise in mixed microbial network data 
		if strTaxID: 
			strOrg = " ".join( arepa.taxid2org( strTaxID ).split(" ")[:iLevel] )
			strGeneFrom = m_hashGeneIDs.get( strOrg )
	if not(strMAPin):
		strDirAuto = c_strDirData if ( c_strID == c_strPathRepo ) else "" 
		strAutoMAPtmp = sfle.d( strDirAuto, c_strID + c_strSufMap )
		strAutoMAP = strAutoMAPtmp if os.path.exists( strAutoMAPtmp ) else None 
		# Use manual mapping files, files that are deeper down have priority
		#else try automatically generated mapping file
		strTopMAP = reduce( lambda x,y: x or y, glob.glob( sfle.d( c_strPathTopMapping, 
			"*" + c_strSufMap ) ), None )
		strMAPManTmp = sfle.d( c_strDirManMap, c_strID + c_strSufMap )
		strMAPin = (strMAPManTmp if os.path.exists( strMAPManTmp) else None) or strTopMAP or strAutoMAP  
		# Use provided mapping files  
		if not(strMAPin) and strTaxID:
			for strMAPname in glob.glob(sfle.d( c_strPathUniprotKO, "*.map" )):
				if re.search( r'\D' + strTaxID + r'\D', strMAPname ):
					strMAPin = strMAPname
					break
		# Else ask arepa to figure out an appropriate mapping file 
		if not(strMAPin) and strTaxID:
			strMAPin = arepa.get_mappingfile( strTaxID )
		# Else use BridgeDB files
		if not(strMAPin) and strTaxID:
			for strSpeciesName in c_pHashBridgeDB.keys():
				if strSpeciesName in arepa.taxid2org( strTaxID ):
					strMAPin = c_pHashBridgeDB[strSpeciesName]
					break 
		
	strBase, strExt = os.path.splitext( str(fileDATin) )
	strCount = funcCounter( g_iterCounter )
	strT = strBase + c_strMapped + strCount + strExt
	
	aastrPrefix 	= [[str(fileDATin)], [True, strT], "-c", str(aiCOL)]
	astrGeneFrom	= ["-f", strGeneFrom] if strGeneFrom else ["-x"]
	astrGeneTo		= ["-t", c_astrGeneTo[0]] 
	astrSkip		= ["-s", iSkip]
	afileLOGout 	= ["-l", [True, str(fileLOGout)]] if fileLOGout else [] 
	astrMapIn 		= ["-m", [strMAPin]] if strMAPin else [] 
	
	aastrArgs 		= aastrPrefix + astrGeneFrom + astrGeneTo + astrSkip + afileLOGout + astrMapIn
	
	afileRet = sfle.op( pE, c_funcGeneMapper, aastrArgs )
	
	pE.Depends( afileRet, sfle.scons_child( pE, c_strPathGeneMapper ) )
	return afileRet

def funcMakeUnique( pE, fileDATin, iSkip = 0, iCol = 2 ):
	strBase, strExt = os.path.splitext(str(fileDATin))
	iCount = funcCounter( g_iterCounter )
	strT = re.sub( r'_mapped[0-9]+', c_strMapped + iCount, str(fileDATin))
	return sfle.op(pE, c_fileProgMakeUnique, [[fileDATin], [True,strT],"-s", iSkip, "-c", iCol])
