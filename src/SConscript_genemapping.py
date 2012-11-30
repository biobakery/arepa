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

c_strID 		= arepa.cwd( )
c_strRepo		= os.path.basename( arepa.path_repo( )[:-1] if arepa.path_repo( )[-1]=="/" else arepa.path_repo( ) )

c_strMapped		= "_mapped" 
c_astrGeneTo            = sfle.readcomment( sfle.d( arepa.path_arepa(),sfle.c_strDirEtc,"geneid" ) or ["H"] ) 
c_piCounter		=  itertools.count(0) 

c_path_GeneMapper       = sfle.d( arepa.path_arepa(), "GeneMapper")
c_fileProgMakeUnique    = sfle.d( arepa.path_arepa(),sfle.c_strDirSrc,"makeunique.py")
c_funcGeneMapper        = sfle.d( c_path_GeneMapper, sfle.c_strDirSrc, "bridgemapper.py" )

# Pre-defined mapping files 
c_fileMappingHuman  	=  sfle.d(pE,arepa.path_arepa(), "GeneMapper",sfle.c_strDirTmp,"Hs_Derby_20110601.bridge")
c_fileMappingMouse  	=  sfle.d(pE,arepa.path_arepa(), "GeneMapper",sfle.c_strDirTmp,"Mm_Derby_20100601.bridge")
c_fileMappingYeast  	=  sfle.d(pE,arepa.path_arepa(), "GeneMapper",sfle.c_strDirTmp,"Sc_Derby_20110603.bridge")

c_astrTaxaHuman		= ["9606", "63221", "741158"]
c_astrTaxaMouse		= ["10090", "10091", "10092", "35531", 
				"39442", "46456", "57486", "80274", 
				"116058", "179238","477815", "477816", 
				"947985"]
c_astrTaxaYeast		= ["4932"]

def funcCounter( pCount ):
	iTemp = next(pCount)
	iOut = None
	if iTemp < 10:
		iOut= "0"+str(iTemp)
	else:
		iOut= str(iTemp)
	return iOut  

def funcGeneIDMapping( pE, strDATin, strLOGout, strMAPin = None ):
	if not(strMAPin) and c_strRepo!="GEO":
		astrMatch = re.findall(r'taxid_([0-9]+)', c_strID)
		strTaxa = astrMatch[0] if astrMatch else None 
		if strTaxa in c_astrTaxaHuman: 
			strMAPin = c_fileMappingHuman
		elif strTaxa in c_astrTaxaMouse:
			strMAPin = c_fileMappingMouse
		elif strTaxa in c_astrTaxaYeast:
			strMapin = c_fileMappingYeast
		else:
			strMAPin = None 
	strBase, strExt = os.path.splitext(str(strDATin))
	iCount = funcCounter(c_piCounter)
    	strCOL = None 
    	if strExt == ".dat":
        	strCOL = "[0,1]"
    	elif strEXT == ".pcl":
        	strCOL = "[0]" 
	strT = strBase+c_strMapped+iCount+strExt
	if strMAPin:
    		return sfle.op( pE, c_funcGeneMapper, [[strDATin], [True,strT],"-m",[strMAPin],
			"-c",strCOL,"-f", c_strGeneFrom,"-t",c_astrGeneTo[0],"-l",[True, strLOGout]] )
	else:
		return sfle.op( pE, c_funcGeneMapper, [[strDATin], [True,strT],"-c",strCOL,"-f", 
			c_strGeneFrom,"-t",c_astrGeneTo[0],"-l",[True, strLOGout]] )	

def funcMakeUnique( pE, strDATin ):
	strBase, strExt = os.path.splitext(str(strDATin))
	iCount = funcCounter(c_piCounter)
	strT = strBase[:-2]+iCount+strExt
    	return sfle.op(pE, c_fileProgMakeUnique, [[strDATin], [True,strT]])
