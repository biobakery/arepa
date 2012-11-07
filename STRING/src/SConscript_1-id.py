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
c_strTaxa                  		= c_strID.split("_")[1]


c_fileInputC    			= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirTmp, "stringc" ) 

c_fileIDPKL				= sfle.d( pE, c_strID + ".pkl" )
c_fileIDDAB				= sfle.d( pE, c_strID + ".dab" )
c_fileIDDAT             		= sfle.d( pE, c_strID + ".dat" )
c_fileIDQUANT          			= sfle.d( pE,  c_strID + ".quant" )

c_fileProgC2Metadata			= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "c2metadata.py" ) 
c_fileProgC2DAT				= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "c2dat.py" ) 


#For GeneMapper:
c_fileIDMapDAT      =  c_strID + "_mapped.dat"
c_fileIDMapDAB      =  c_strID + "_mapped.dab"
c_fileIDMapQUANT    =  c_strID + "_mapped.quant"
c_strGeneTo         = sfle.readcomment( sfle.d( arepa.path_arepa(),sfle.c_strDirEtc,"geneid" ) or ["Ck"] )
c_path_Mappingfiles =  sfle.d( arepa.path_arepa( ), "GeneMapper", sfle.c_strDirEtc, "uniprotko")
c_fileMappingfileUniprot2KO = sfle.d(c_path_Mappingfiles, "mappingfile_allspecies_uniref2KO.map")
c_fileMappingHuman  =  sfle.d( c_path_GeneMapper, sfle.c_strDirEtc,"Hs_Derby_20110601.bridge")

c_fileStatus	    = sfle.d( pE, "status.txt" )

pE = DefaultEnvironment( )

afileIDTXT = sfle.pipe( pE, c_fileInputC, c_fileProgC2Metadata, c_fileIDPKL,[[c_strID]] )

def funcDAB( target, source, env ):
	strT, astrSs = sfle.ts( target, source )
	strProg, strIn = astrSs[:2]
	return sfle.ex( (sfle.cat( strIn ), "|", strProg, c_strID, "| Dat2Dab -o", strT) )
Command( c_fileIDDAB, [c_fileProgC2DAT, c_fileInputC], funcDAB )

def funcDAT(target, source, env):
    strT, astrSs = sfle.ts( target, source )
    strIn = astrSs[0]
    return sfle.ex([" Dat2Dab -o", strT, "-i", strIn])
Command( c_fileIDDAT, c_fileIDDAB, funcDAT )

def funcIDQUANT( target, source, env ):
    strT, astrSs = sfle.ts( target, source )
    strS = astrSs[0]
    return (sfle.ex("echo '0.5\t1.5' >" + strT))
Command( c_fileIDQUANT, c_fileIDDAB ,funcIDQUANT )
Default (c_fileIDQUANT)

#use shared code for dat and dab 

##############################################
#- Gene id mapping from Uniprot to Genesymbols
##############################################

#use shared code 
