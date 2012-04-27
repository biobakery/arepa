import sys
import csv
import pickle
import sfle
import arepa
import os
import metadata

c_fileIDNormPCL		= File( c_strID + "_01norm.pcl" )
c_fileIDPCL			= File( c_strID + ".pcl" )
c_fileIDDAB			= File( c_strID + ".dab" )
c_fileIDQUANT       = File( c_strID + ".quant" )

c_fileIDPCLorig     = File(c_strID + "_orig.pcl")
c_fileIDPKL         = File(c_strID + ".pkl")
c_fileIDMappedPCL   = File( c_strID + "_00mapped.pcl" )
c_funcPclIds        = sfle.d( arepa.path_arepa( ), sfle.c_strDirSrc, "pclids.py" )
c_pathmappingfiles  = sfle.d(arepa.path_arepa(),sfle.c_strDirEtc)


#- Gene id mapping
def funcGeneIdMapping( target, source, env):
    strT, astrSs = sfle.ts( target, source )
    strFunc, strRawPCL, strMapping, strPKL = astrSs[:4]
    pMetadata = metadata.open(open(strPKL,"rb") )
    c_Taxa = pMetadata["taxid"]
    c_platform = pMetadata["platform"]
    c_mappingfilename = str(c_platform)+"_taxid"+str(c_Taxa)+".txt"
    c_mappingfile = sfle.d(strMapping, c_mappingfilename)
    sys.stderr.write("+++ GENE ID Mapping +++ \n"+str(c_platform)+"\n")
    return sfle.ex([ strFunc, strRawPCL, strT, c_mappingfile])

Command(c_fileIDMappedPCL, [c_funcPclIds, c_fileIDRawPCL, c_pathmappingfiles , c_fileIDPKL], funcGeneIdMapping)


#- Normalize
def funcIDNormPCL( target, source, env, iMaxLines = 100000 ):
	strT, astrSs = sfle.ts( target, source )
	strS = astrSs[0]
	iLC = sfle.lc( strS )
	return ( sfle.ex( "Normalizer -t pcl -T medmult < " + strS, strT )
		if ( iLC < iMaxLines ) else sfle.ex( "head -n 3 < " + strS, strT ) )

Command( c_fileIDNormPCL, c_fileIDMappedPCL, funcIDNormPCL )
#Command( c_fileIDNormPCL, c_fileIDRawPCL, funcIDNormPCL ) #call if gene id mapping is skipped


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

