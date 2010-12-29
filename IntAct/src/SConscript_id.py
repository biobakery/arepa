#!/usr/bin/env python

import arepa
import os
import sys

def test( iLevel, strTo, strFrom, pArgs ):
	return ( iLevel == 1 )
if locals( ).has_key( "testing" ):
	sys.exit( )

Import( "pE" )
c_strID				= arepa.cwd( )
c_fileIDTXT			= File( c_strID + ".txt" )
c_fileIDDAB			= File( c_strID + ".dab" )
c_fileProgC2TXT		= File( arepa.d( arepa.path_repo( pE ), arepa.c_strDirSrc, "c2txt.py" ) )
c_fileProgC2DAT		= File( arepa.d( arepa.path_repo( pE ), arepa.c_strDirSrc, "c2dat.py" ) )

pE.Import( "c_fileIntactC" )

afileIDTXT = arepa.pipe( pE, c_fileIntactC, c_fileProgC2TXT, c_fileIDTXT, [[False, c_strID]] )
pE.Default( afileIDTXT )

def funcDAB( target, source, env ):
	strT, astrSs = arepa.ts( target, source )
	strProg, strIn = astrSs
	return arepa.ex( " ".join( [strProg, c_strID, "<", strIn, "| Dat2Dab -o", strT] ) )
afileIDDAB = pE.Command( c_fileIDDAB, [c_fileProgC2DAT, c_fileIntactC], funcDAB )
pE.Default( afileIDDAB )
