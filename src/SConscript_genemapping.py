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

c_strID 		= arepa.cwd( )

c_astrGeneTo             = sfle.readcomment( sfle.d( arepa.path_arepa(),sfle.c_strDirEtc,"geneid" ) or ["H"] ) 
c_piCounter		=  itertools.count(0) 

c_path_GeneMapper       = sfle.d( arepa.path_arepa(), "GeneMapper")
c_fileProgMakeUnique    = sfle.d( arepa.path_arepa(),sfle.c_strDirSrc,"makeunique.py")
c_funcGeneMapper        = sfle.d( c_path_GeneMapper, sfle.c_strDirSrc, "bridgemapper.py" )

pE = DefaultEnvironment( )

def funcCounter( pCount ):
	iTemp = next(pCount)
	iOut = None
	if iTemp < 10:
		iOut="_mapped0"+str(iTemp)
	else:
		iOut="_mapped"+str(iTemp)
	return iOut  

def funcGeneIdMapping( strDATin, strMAPin, strLOGout ):
	strBase, strExt = os.path.splitext(strDATin)
	iCount = funcCounter(c_piCounter)
    	strCOL = None 
    	if strExt == ".dat":
        	strCOL = "[0,1]"
    	elif strEXT == ".pcl":
        	strCOL = "[0]" 
    	return sfle.op( pE, c_funcGeneMapper, [strDATin, strBase+iCount+strExt,"-m",strMAPin,"-c",strCOL,"-f", c_strGeneFrom,"-t",c_astrGeneTo[0],"-l",strLOGout] ) 

def funcMakeUnique( strDATin ):
	strBase, strExt = os.path.splitext(strDATin)
	iCount = funcCounter(c_piCounter)
    	return sfle.op( pE, c_fileProgMakeUnique, [strDATin, strBase+iCount+strExt] )

