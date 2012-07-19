#!/usr/bin/env python 
'''
Microarray pipeline -- gene mapping, normalization, imputation, 
co-expression network construction
'''
import sys
import csv
import pickle
import sfle
import arepa
import os
import metadata
import glob 

c_strSufMap		= ".map"
c_strManMap		= "manual_mapping"
c_fileIDNormPCL		= File( c_strID + "_01norm.pcl" )
c_fileIDPCL		= File( c_strID + ".pcl" )
c_fileIDDAB		= File( c_strID + ".dab" )
c_fileIDQUANT       	= File( c_strID + ".quant" )

c_strDirManMap		= sfle.d( arepa.path_repo( ), sfle.c_strDirEtc, c_strManMap ) 
c_fileIDMappedPCL   	= File( c_strID + "_00mapped.pcl" )

## Gene Mapper:
c_path_GeneMapper   	= sfle.d( arepa.path_arepa(), "GeneMapper")
c_funcPclIds        	= sfle.d( c_path_GeneMapper, sfle.c_strDirSrc, "bridgemapper.py" )

# If manually curated mapping file exists, use. Otherwise, use automatically generated one. 
c_fileMap           	= reduce( lambda x,y: x or y, filter( lambda x: x==c_strID + c_strSufMap,\
				glob.glob(sfle.d(c_strDirManMap,"*" + c_strSufMap)) ),None ) \
				or File(c_strID + "_map.txt")

#- Gene id mapping
def funcGeneIdMapping( target, source, env):
    strT, astrSs = sfle.ts( target, source )
    strFunc, strDATin, strMapfile  = astrSs[:3]
    return sfle.ex([ strFunc,strDATin, strT, strMapfile, "[0]", "X", "H"])
Command( c_fileIDMappedPCL,[c_funcPclIds, c_fileIDRawPCL, c_fileMap], funcGeneIdMapping)

#- Normalize
def funcIDNormPCL( target, source, env, iMaxLines = 100000 ):
	strT, astrSs = sfle.ts( target, source )
	strS = astrSs[0]
	iLC = sfle.lc( strS )
	return ( sfle.ex( "Normalizer -t pcl -T medmult < " + strS, strT )
		if ( iLC < iMaxLines ) else sfle.ex( "head -n 3 < " + strS, strT ) )

Command( c_fileIDNormPCL, c_fileIDMappedPCL, funcIDNormPCL )

#- Impute
def funcIDKNNPCL( target, source, env, iMaxLines = 40000 ):
	strT, astrSs = sfle.ts( target, source )
	strS = astrSs[0]
	iLC = sfle.lc( strS )
	return ( sfle.ex( "KNNImputer < " + strS, strT )
		if ( iLC < iMaxLines ) else sfle.ex( "head -n 3 < " + strS, strT ) )

Command( c_fileIDPCL, c_fileIDNormPCL, funcIDKNNPCL )

#- PCL -> DAB
def funcIDDAB( target, source, env ):
	strT, astrSs = sfle.ts( target, source )
	strS = astrSs[0]
	iLC = sfle.lc( strS )
	return ( sfle.ex( (sfle.cat( strS ), " | Distancer -o", strT) )
		if ( iLC > 3 ) else sfle.ex( "echo", strT ) )

Command( c_fileIDDAB, c_fileIDPCL, funcIDDAB )

#- Generate Quant files
def funcIDQUANT( target, source, env ):
        strT, astrSs = sfle.ts( target, source )
        strS = astrSs[0]
        iLC = sfle.lc( strS )
        return (sfle.ex("echo '-1.5\t-0.5\t0.5\t1.5\t2.5\t3.5\t4.5' >" + strT))

Command( c_fileIDQUANT, c_fileIDPCL, funcIDQUANT )

