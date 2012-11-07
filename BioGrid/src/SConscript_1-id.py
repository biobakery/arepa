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

c_strID				= arepa.cwd( )

c_fileInputBioGridC		= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirTmp, "biogridc.txt" ) 

c_fileIDPKL			= sfle.d( pE, c_strID + ".pkl" )
c_fileIDDAB			= sfle.d( pE, c_strID + ".dab" )
c_fileIDDAT             	= sfle.d( pE, c_strID + ".dat" )
c_fileIDQUANT           	= sfle.d( pE, c_strID + ".quant" )
    
c_fileProgC2Metadata		= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "c2metadata.py" ) 
c_fileProgC2DAT			= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "c2dat.py" ) 

#For GeneMapper:
c_fileIDMapDAT      		=  c_strID + "_mapped.dat"
c_fileIDMapDAB      		=  c_strID + "_mapped.dab"
c_fileIDMapQUANT    		=  c_strID + "_mapped.quant"

c_path_Mappingfiles 		=  sfle.d( pE, arepa.path_arepa( ), "GeneMapper",sfle.c_strDirEtc,"uniprotko")
c_fileMappingHuman  		=  sfle.d( pE, c_path_GeneMapper, sfle.c_strDirEtc,"Hs_Derby_20110601.bridge")

c_fileMappingfileUniprot2KO 	= sfle.d( pE, c_path_Mappingfiles, "mappingfile_allspecies_uniref2KO.map")
c_fileStatus        		= sfle.d( pE,"status.txt" )

c_strGeneIDFrom  		= "H"

pE = DefaultEnvironment( )

afileIDTXT = sfle.pipe( pE, c_fileInputBioGridC, c_fileProgC2Metadata, c_fileIDPKL, [[c_strID]] )

sfle.pipe( pE, c_fileInputBioGridC, c_fileProgC2DAT, c_fileIDDAT, [[c_strID]] ) 

##############################################
#- Gene id mapping from Uniprot to Genesymbols
##############################################

funcGeneIDMapping( c_fileDATin, c_fileMappingHuman, c_fileStatus )

#do stuff for dat/dab, quant. 
