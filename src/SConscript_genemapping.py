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

c_strID 		= arepa.cwd( )
c_strPathRepo		= os.path.basename( os.path.dirname( arepa.path_repo( ) ) )
c_strRepo		= os.path.basename( arepa.path_repo( )[:-1] if arepa.path_repo( )[-1]=="/" else arepa.path_repo( ) )

c_strDirData		= sfle.d( arepa.path_repo( ), sfle.c_strDirData )

c_strSufMap 		= ".map" 
c_strDirManMap          = sfle.d( arepa.path_repo( ), sfle.c_strDirEtc, "manual_mapping" )

c_strMapped		= "_mapped" 
c_astrGeneTo            = sfle.readcomment( sfle.d( arepa.path_arepa(),sfle.c_strDirEtc,"geneid" ) or ["H"] ) 
c_piCounter		=  itertools.count(0) 

c_strPathGeneMapper	= sfle.d( arepa.path_arepa(), "GeneMapper")
c_strPathUniprotKO	= sfle.d( c_strPathGeneMapper, sfle.c_strDirEtc, "uniprotko" )
c_fileProgMakeUnique    = sfle.d( arepa.path_arepa(),sfle.c_strDirSrc,"makeunique.py")
c_funcGeneMapper        = sfle.d( c_strPathGeneMapper, sfle.c_strDirSrc, "bridgemapper.py" )

c_pHashBridgeDB = {"Homo sapiens": sfle.d(pE,arepa.path_arepa(), "GeneMapper",										sfle.c_strDirEtc,"Hs_Derby_20110601.bridge"),
			"Mus musculus": sfle.d(pE,arepa.path_arepa(), "GeneMapper",
				sfle.c_strDirEtc,"Mm_Derby_20100601.bridge"), 
			"Saccharomyces cerevisiae": sfle.d(pE,arepa.path_arepa(), "GeneMapper",
				sfle.c_strDirEtc,"Sc_Derby_20110603.bridge"), 		
			}

pHashBridgeDBTaxIDs = {k:arepa.org2taxid( k, True ) for k in c_pHashBridgeDB.keys()}


def funcCounter( pCount ):
	return "%02d" %next(pCount)

def funcGeneIDMapping( pE, strDATin, strLOGout, strMAPin = None, strCOL =  "[0,1]", strSkip = "0" ):
	if not(strMAPin):
		strDirAuto = c_strDirData if c_strID == c_strPathRepo else "" 
		strAutoMAPtmp	= sfle.d( strDirAuto, c_strID + c_strSufMap )
		strAutoMAP	= strAutoMAPtmp if glob.glob(strAutoMAPtmp) else None 
		strMAPin = reduce( lambda x,y: x or y, filter( lambda x: c_strID in x,
                       glob.glob(sfle.d(c_strDirManMap,"*" + c_strSufMap)) ), strAutoMAP )
		astrMatch = re.findall(r'taxid_([0-9]+)', c_strID)
		strTaxa = astrMatch[0].strip() if astrMatch else None
		if not(strMAPin) and strTaxa:
			for strSpeciesName in c_pHashBridgeDB.keys():
				if strSpeciesName in arepa.taxid2org( strTaxa ):
					strMAPin = c_pHashBridgeDB[strSpeciesName] 
		if not(strMAPin) and strTaxa:
			for strMAPname in glob.glob(sfle.d( c_strPathUniprotKO, "*.map" )):
				if strTaxa in strMAPname:
					strMAPin = strMAPname 	
	strBase, strExt = os.path.splitext(str(strDATin))
	strCount = funcCounter(c_piCounter)    	
	strT = strBase+c_strMapped+strCount+strExt
	if strMAPin:
    		return sfle.op( pE, c_funcGeneMapper, [[strDATin], [True,strT],"-m",[strMAPin],
			"-c",strCOL,"-f", c_strGeneFrom,"-t",c_astrGeneTo[0],"-s", 
			strSkip, "-l",[True, strLOGout]] )
	else:
		return sfle.op( pE, c_funcGeneMapper, [[strDATin], [True,strT],"-c",strCOL,"-f", 
			c_strGeneFrom,"-t",c_astrGeneTo[0],"-s", strSkip, "-l",[True, strLOGout]] )	

def funcMakeUnique( pE, strDATin ):
	strSkip = "0" if c_strRepo != "GEO" else "2" 
	strBase, strExt = os.path.splitext(str(strDATin))
	iCount = funcCounter(c_piCounter)
	strT = strBase[:-2]+iCount+strExt
    	return sfle.op(pE, c_fileProgMakeUnique, [[strDATin], [True,strT],"-s", strSkip])
