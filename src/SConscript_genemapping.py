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

c_strMapped		= "_mapped" 
c_astrGeneTo            = sfle.readcomment( sfle.d( arepa.path_arepa(),sfle.c_strDirEtc,"geneid" ) or ["H"] ) 
c_piCounter		=  itertools.count(0) 

c_path_GeneMapper       = sfle.d( arepa.path_arepa(), "GeneMapper")
c_fileProgMakeUnique    = sfle.d( arepa.path_arepa(),sfle.c_strDirSrc,"makeunique.py")
c_funcGeneMapper        = sfle.d( c_path_GeneMapper, sfle.c_strDirSrc, "bridgemapper.py" )

def funcCounter( pCount ):
	iTemp = next(pCount)
	iOut = None
	if iTemp < 10:
		iOut= "0"+str(iTemp)
	else:
		iOut= str(iTemp)
	return iOut  

def funcGeneIDMapping( pE, strDATin, strMAPin, strLOGout ):
	strBase, strExt = os.path.splitext(str(strDATin))
	iCount = funcCounter(c_piCounter)
    	strCOL = None 
    	if strExt == ".dat":
        	strCOL = "[0,1]"
    	elif strEXT == ".pcl":
        	strCOL = "[0]" 
	strT = strBase+c_strMapped+iCount+strExt
    	return sfle.op( pE, c_funcGeneMapper, [[strDATin], [True,strT],"-m",[strMAPin],"-c",strCOL,"-f", c_strGeneFrom,"-t",c_astrGeneTo[0],"-l",[True, strLOGout]] ) 

def funcMakeUnique( pE, strDATin ):
	strBase, strExt = os.path.splitext(str(strDATin))
	iCount = funcCounter(c_piCounter)
	strT = strBase[:-2]+iCount+strExt
    	return sfle.op(pE, c_fileProgMakeUnique, [[strDATin], [True,strT]])

# must check metadata in order to see what organism it is ... then do the mapping 
# this will change some of the code I wrote before 


'''

this code should be shared across all the modules 

#- Get Mappingfile
def func_GetMappingfileFromDir(taxid):
    # all mappingfiles from the directory:
    files = [os.path.basename(p) for p in glob.glob(sfle.d(c_path_Mappingfiles, "*.map"))]
    # our mappingfile that starts with the taxid:
    f = [mm.startswith(taxid+"_") for mm in files]
    try:
        ix = f.index(True)
        return files[ix]
    except ValueError:
        return "X"

def func_GetMappingfile(taxid):
    if taxid == "9606":
        return c_fileMappingHuman
    else:
        return "mapping_taxid"+str(c_Taxa)+".txt"

#- Do the Mapping:
def funcGeneIdMapping( target, source, env):
    astrTs, astrSs = ([f.get_abspath() for f in a] for a in (target,source))
    strT, strStatus = astrTs[:2]
    strFunc, strDATin, strPKL = astrSs[:3]
    pMetadata = metadata.open(open(strPKL,"rb") )
    c_Taxa = pMetadata["taxid"]
    sys.stderr.write("+++ GENE ID Mapping +++ \n")
    ## START DETERMINE MAPPINGFILE
    c_mappingfilename = func_GetMappingfileFromDir(c_Taxa) #Normal mapping in Human: func_GetMappingfile(c_Taxa)
    c_mappingfile = sfle.d(c_path_Mappingfiles, c_mappingfilename)
    if not os.path.exists(c_mappingfile):
        sys.stderr.write("+++ No species-specific mappingfile exists, take the general mappingfile from uniprot.  +++ \n")
        c_mappingfile = c_fileMappingfileUniprot2KO
        ## END Take general Uniprot to KO mappingfile if no mappingfile exists so far...
    return sfle.ex([ strFunc, strDATin, strT, "-m", c_mappingfile,"-c", "[0,1]", "-f", c_stringBiogridGeneID, "-t",c_strGeneTo[0], "-l", strStatus])
Command([c_fileIDMapDAT,c_fileStatus],[c_funcGeneMapper, c_fileIDDAT, c_fileIDPKL], funcGeneIdMapping)
'''


