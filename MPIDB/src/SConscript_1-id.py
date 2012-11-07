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
c_fileInputC    			= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirTmp, "mpidbc" ) )
c_fileIDPKL				= sfle.d( pE, c_strID + ".pkl" )
c_fileIDDAB				= sfle.d( pE, c_strID + ".dab" )
c_fileIDQUANT             		= sfle.d( c_strID + ".quant" )
c_fileIDDAT             		= sfle.d( pE, c_strID + ".dat" )

c_fileProgC2Metadata			= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "c2metadata.py" ) 
c_fileProgC2DAT				= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "c2dat.py" ) 

#For GeneMapper:
c_fileIDMapDAT      			=  sfle.d( pE, c_strID + "_mapped.dat" )
c_fileIDMapDAB      			=  sfle.d( pE, c_strID + "_mapped.dab" )
c_fileIDMapQUANT    			=  sfle.d( pE, c_strID + "_mapped.quant" )
c_strGeneTo         			=  sfle.readcomment( sfle.d( arepa.path_arepa(),sfle.c_strDirEtc,"geneid" ) or ["Ck"] )
c_path_GeneMapper   			=  sfle.d( pE, arepa.path_arepa(), "GeneMapper")
c_funcGeneMapper    			=  sfle.d( pE, c_path_GeneMapper, sfle.c_strDirSrc, "bridgemapper.py" )
c_path_Mappingfiles 			=  sfle.d( pE, arepa.path_arepa( ), "GeneMapper", sfle.c_strDirEtc, "uniprotko")
c_fileMappingfileUniprot2KO		=  sfle.d( pE, c_path_Mappingfiles, "mappingfile_allspecies_uniref2KO.map")
c_fileMappingHuman  			=  sfle.d( pE, c_path_GeneMapper, sfle.c_strDirEtc,"Hs_Derby_20110601.bridge")
c_funcChildrenTaxa  			=  sfle.d( pE, c_path_GeneMapper, sfle.c_strDirSrc, "getTaxidsFromChildren.py" )
c_filetaxachildren  			=  sfle.d( pE, arepa.path_repo( ), sfle.c_strDirTmp,"taxachildren.txt")
c_fileStatus	    			=  sfle.d(pE, "status.txt")

c_stringMPIDBGeneID 			= "S"

pE = DefaultEnvironment( )

afileIDTXT = sfle.pipe( pE, c_fileInputC, c_fileProgC2Metadata, c_fileIDPKL,[[c_strID]] )

def funcDAB( target, source, env ):
	strT, astrSs = sfle.ts( target, source )
	strProg, strIn = astrSs[:2]
	return sfle.ex( (sfle.cat( strIn ), "|", strProg, c_strID, "| Dat2Dab -o", strT) )
afileIDDAB = Command( c_fileIDDAB, [c_fileProgC2DAT, c_fileInputC], funcDAB )

##############################################
#- Gene id mapping from Uniprot to Genesymbols
##############################################

