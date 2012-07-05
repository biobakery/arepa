#!/usr/bin/env python

import arepa
import os
import sfle
import sys
import metadata
import glob

def test( iLevel, strID, hashArgs ):
	return ( iLevel == 1 )
if locals( ).has_key( "testing" ):
	sys.exit( )

c_strID					= arepa.cwd( )
c_fileInputIntactC		= File( sfle.d( arepa.path_repo( ), sfle.c_strDirTmp, "intactc" ) )
c_fileIDPKL				= File( c_strID + ".pkl" )
c_fileIDDAB				= File( c_strID + ".dab" )
c_fileIDDAT             = File( c_strID + ".dat" )
c_fileIDQUANT           = File( c_strID + ".quant" )

c_fileProgC2Metadata	= File( sfle.d( arepa.path_repo( ), sfle.c_strDirSrc, "c2metadata.py" ) )
c_fileProgC2DAT			= File( sfle.d( arepa.path_repo( ), sfle.c_strDirSrc, "c2dat.py" ) )

#For GeneMapper:
c_fileIDMapDAT      =  c_strID + "_mapped.dat" 
c_fileIDMapDAB      =  c_strID + "_mapped.dab"
c_fileIDMapQUANT    =  c_strID + "_mapped.quant"
c_path_GeneMapper   =  sfle.d( arepa.path_arepa(), "GeneMapper")
c_funcGeneMapper    =  sfle.d( c_path_GeneMapper, sfle.c_strDirSrc, "bridgemapper.py" )
c_path_Mappingfiles =  sfle.d( arepa.path_repo( ), sfle.c_strDirEtc)
#c_fileMappingfileUniprot2KO = sfle.d(c_path_Mappingfiles, "mappingfile_allspecies_uniref2KO.map")
c_fileMappingHuman  =  sfle.d( c_path_GeneMapper, sfle.c_strDirEtc,"Hs_Derby_20110601.bridge")
c_funcChildrenTaxa  =  sfle.d( c_path_GeneMapper, sfle.c_strDirSrc, "getTaxidsFromChildren.py" )
c_filetaxachildren  =  sfle.d( arepa.path_repo( ), sfle.c_strDirTmp,"taxachildren.txt")



pE = DefaultEnvironment( )

afileIDTXT = sfle.pipe( pE, c_fileInputIntactC, c_fileProgC2Metadata, c_fileIDPKL,
	[[False, c_strID]] )
Default( afileIDTXT )

def funcDAB( target, source, env ):
	strT, astrSs = sfle.ts( target, source )
	strProg, strIn = astrSs[:2]
	return sfle.ex( (sfle.cat( strIn ), "|", strProg, c_strID, "| Dat2Dab -o", strT) )
Command( c_fileIDDAB, [c_fileProgC2DAT, c_fileInputIntactC], funcDAB )

def funcDAT(target, source, env):
    strT, astrSs = sfle.ts( target, source )
    strIn = astrSs[0]
    if os.stat(strIn)[6]!=0:
        return sfle.ex([" Dat2Dab -o", strT, "-i", strIn])
    else:
        return strIn
Command( c_fileIDDAT, c_fileIDDAB, funcDAT )

def funcIDQUANT( target, source, env ):
    strT, astrSs = sfle.ts( target, source )
    strS = astrSs[0]
    return (sfle.ex("echo '0.5\t1.5' >" + strT))
Command( c_fileIDQUANT, c_fileIDDAB ,funcIDQUANT )
Default ( c_fileIDQUANT)


##############################################
#- Gene id mapping from Uniprot to Genesymbols
##############################################

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
    strT, astrSs = sfle.ts( target, source )
    strFunc, strDATin, strPKL = astrSs[:3]
    pMetadata = metadata.open(open(strPKL,"rb") )
    c_Taxa = pMetadata["taxid"]
    sys.stderr.write("+++ GENE ID Mapping +++ \n")
    ## START DETERMINE MAPPINGFILE
    c_mappingfilename = func_GetMappingfileFromDir(c_Taxa) #Normal mapping in Human: func_GetMappingfile(c_Taxa)
    c_mappingfile = sfle.d(c_path_Mappingfiles, c_mappingfilename)
    ## END DETERMINE MAPPINGFILE
    ## START FIND TAXONOMICAL CHILDREN MAPPINGFILE IF ORIGINAL DOES NOT EXIST!
    if not os.path.exists(c_mappingfile):
        sys.stderr.write("+++ Original mappingfile does not exist, try one of its taxonomical children.  +++ \n")
        sfle.ex([c_funcChildrenTaxa, c_Taxa, c_filetaxachildren])
        for line in open(c_filetaxachildren,"r"):
            mapping = func_GetMappingfileFromDir(line.split("\n")[0])
            mapping = sfle.d(c_path_Mappingfiles, mapping)
            if os.path.exists(mapping):
                c_mappingfile = mapping
                break
    ## END FIND TAXONOMICAL CHILDREN MAPPINGFILE
    ## START Take general Uniprot to KO mappingfile if no mappingfile exists so far...
    if not os.path.exists(c_mappingfile):
        sys.stderr.write("+++ No species-specific mappingfile exists, take the general mappingfile from uniprot.  +++ \n")
        c_mappingfile = c_fileMappingfileUniprot2KO
    ## END Take general Uniprot to KO mappingfile if no mappingfile exists so far...
    return sfle.ex([ strFunc, strDATin, strT, c_mappingfile,"[0,1]", "S", "Ck"])
#Command(c_fileIDMapDAT, [c_funcGeneMapper, c_fileIDDAT, c_fileIDPKL], funcGeneIdMapping)


def funcGeneIdMapping2( target, source, env):
    strT, astrSs = sfle.ts( target, source )
    strFunc, strDATin = astrSs[:2]
    sys.stderr.write("+++ GENE ID Mapping +++ \n")
    return sfle.ex([ strFunc, strDATin, strT, c_fileMappingHuman,"[0,1]", "S", "Ck"])
Command(c_fileIDMapDAT, [c_funcGeneMapper, c_fileIDDAT], funcGeneIdMapping2)


def funcDABmapped( target, source, env ):
    strT, astrSs = sfle.ts( target, source )
    fileOut,fileMap = astrSs[:2]
    if os.stat(fileMap)[6]!=0:
        return sfle.ex([" Dat2Dab -o", strT, "-i", fileMap])
    else:
        return sfle.ex(["touch",strT])
Command( c_fileIDMapDAB, [c_fileIDDAT,c_fileIDMapDAT], funcDABmapped )
Default(c_fileIDMapDAB)

def funcIDQUANTMapped( target, source, env ):
    strT, astrSs = sfle.ts( target, source )
    fileOut,fileMap = astrSs[:2]
    if os.stat(fileMap)[6]!=0:
        return (sfle.ex("echo '0.5\t1.5' >" + strT))
    else:
        return sfle.ex(["touch",strT])
Command( c_fileIDMapQUANT, [c_fileIDDAT,c_fileIDMapDAT] ,funcIDQUANTMapped )
Default ( c_fileIDMapQUANT)

