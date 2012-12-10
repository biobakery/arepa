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

pE = DefaultEnvironment( )

c_strSufMap         	= ".map"
c_strManMap         	= "manual_mapping"
c_fileIDNormPCL		= sfle.d( pE, c_strID + "_01norm.pcl" )
c_fileIDPCL		= sfle.d( pE, c_strID + ".pcl" )
c_fileIDDAB		= sfle.d( pE, c_strID + ".dab" )
c_fileIDQUANT       	= sfle.d( pE, c_strID + ".quant" )
c_fileIDPKL         	= sfle.d( pE, c_strID + ".pkl" )
c_fileStatus		= sfle.d( pE, "status.txt" )

c_strDirManMap		= sfle.d( arepa.path_repo( ), sfle.c_strDirEtc, c_strManMap ) 
c_fileIDMappedPCL  	= sfle.d( pE, c_strID + "_00mapped.pcl" )
c_fileIDMappedPCL2	= sfle.d( pE, c_strID + "_01mapped.pcl" )

## Gene Mapper:
c_fileInputSConscriptGM = sfle.d( pE, arepa.path_arepa(),sfle.c_strDirSrc,"SConscript_genemapping.py")
c_strCOL		= "[0]"
c_strSkip		= "2"
c_path_GeneMapper   	= sfle.d( arepa.path_arepa(), "GeneMapper")
c_strGeneFrom		= "X"
c_strGeneTo         	= sfle.readcomment( sfle.d( arepa.path_arepa(),sfle.c_strDirEtc,"geneid" ) or ["H"] )
c_funcPclIds       	= sfle.d( c_path_GeneMapper, sfle.c_strDirSrc, "bridgemapper.py" )
c_funcMakeUnique	= sfle.d( arepa.path_arepa(), sfle.c_strDirSrc, "makeunique.py" )

#Load GeneMapper SConscript 
execfile( str(c_fileInputSConscriptGM) )

#Perform Gene Mapping 
astrMapped = funcGeneIDMapping( pE, c_fileIDRawPCL, c_fileStatus, None, c_strCOL, c_strSkip )

#Get rid of duplicate identifiers 
astrUnique = funcMakeUnique( pE, astrMapped[0], c_strSkip ) 

#- Normalize
def funcIDNormPCL( target, source, env, iMaxLines = 100000 ):
	strT, astrSs = sfle.ts( target, source )
	strS = astrSs[1] if sfle.readcomment(astrSs[1]) > int(c_strSkip) else astrSs[0] 
	iLC = sfle.lc( strS )
	return ( sfle.ex( "Normalizer -t pcl -T medmult < " + strS, strT )
		if ( iLC < iMaxLines ) else sfle.ex( "head -n 3 < " + strS, strT ) )

Command( c_fileIDNormPCL, [c_fileIDRawPCL, astrUnique[0]], funcIDNormPCL )

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
