#!/usr/bin/env python

import arepa

#Import( "pE" )
#Import( "hashArgs" )
#Import( "c_strID" )
#Import( "c_strFileIDRawPCL" )
#Import( "c_strFileIDNormPCL" )
c_strFileIDPCL	= c_strID + ".pcl"
c_strFileIDDAB	= c_strID + ".dab"

#- Normalize
def funcIDNormPCL( target, source, env, iMaxLines = 100000 ):
	strT, astrSs = arepa.ts( target, source )
	strS = astrSs[0]
	iLC = arepa.lc( strS )
	return ( arepa.ex( "Normalizer -t pcl -T medmult < " + strS, strT )
		if ( iLC < iMaxLines ) else arepa.ex( "head -n 3 < " + strS, strT ) )
Command( c_strFileIDNormPCL, c_strFileIDRawPCL, funcIDNormPCL )

#- Impute
def funcIDKNNPCL( target, source, env, iMaxLines = 40000 ):
	strT, astrSs = arepa.ts( target, source )
	strS = astrSs[0]
	iLC = arepa.lc( strS )
	return ( arepa.ex( "KNNImputer < " + strS, strT )
		if ( iLC < iMaxLines ) else arepa.ex( "head -n 3 < " + strS, strT ) )
Command( c_strFileIDPCL, c_strFileIDNormPCL, funcIDKNNPCL )
Default( c_strFileIDPCL )

#- PCL -> DAB
def funcIDDAB( target, source, env ):
	strT, astrSs = arepa.ts( target, source )
	strS = astrSs[0]
	iLC = arepa.lc( strS )
	return ( arepa.ex( " ".join( ("Distancer -o", strT, "<", strS) ) )
		if ( iLC > 3 ) else arepa.ex( "echo", strT ) )
#Command( c_strFileIDDAB, c_strFileIDPCL, funcIDDAB )
#Default( c_strFileIDDAB )
