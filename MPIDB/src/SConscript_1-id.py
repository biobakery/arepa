#!/usr/bin/env python

import arepa
import os
import sfle
import sys

def test( iLevel, strID, hashArgs ):
	return ( iLevel == 1 )
if locals( ).has_key( "testing" ):
	sys.exit( )

c_strID					= arepa.cwd( )

c_fileInputC    		= File( sfle.d( arepa.path_repo( ), sfle.c_strDirTmp, "mpidbc" ) )

c_fileIDPKL				= File( c_strID + ".pkl" )
c_fileIDDAB				= File( c_strID + ".dab" )
c_fileIDQUANT             = File( c_strID + ".quant" )
c_fileIDDAT             = File( c_strID + ".dat" )



c_fileProgC2Metadata	= File( sfle.d( arepa.path_repo( ), sfle.c_strDirSrc, "c2metadata.py" ) )
c_fileProgC2DAT			= File( sfle.d( arepa.path_repo( ), sfle.c_strDirSrc, "c2dat.py" ) )

pE = DefaultEnvironment( )

afileIDTXT = sfle.pipe( pE, c_fileInputC, c_fileProgC2Metadata, c_fileIDPKL,[[False, c_strID]] )
Default( afileIDTXT )

def funcDAB( target, source, env ):
	strT, astrSs = sfle.ts( target, source )
	strProg, strIn = astrSs[:2]
	return sfle.ex( (sfle.cat( strIn ), "|", strProg, c_strID, "| Dat2Dab -o", strT) )
afileIDDAB = Command( c_fileIDDAB, [c_fileProgC2DAT, c_fileInputC], funcDAB )
Default( afileIDDAB )


def funcDAT(target, source, env):
    strT, astrSs = sfle.ts( target, source )
    strIn = astrSs[0]
    return sfle.ex([" Dat2Dab -o", strT, "-i", strIn])
afileIDDAT = Command( c_fileIDDAT, c_fileIDDAB, funcDAT )
Default(afileIDDAT)

def funcIDQUANT( target, source, env ):
    strT, astrSs = sfle.ts( target, source )
    strS = astrSs[0]
    return (sfle.ex("echo '0.5\t1.5' >" + strT))
Command( c_fileIDQUANT, c_fileIDDAB ,funcIDQUANT )
Default (c_fileIDQUANT)

