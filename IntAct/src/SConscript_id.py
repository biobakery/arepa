#!/usr/bin/env python

import arepa
import os
import sys

def test( iLevel, strTo, strFrom, pArgs ):
	return ( iLevel == 1 )
if locals( ).has_key( "testing" ):
	sys.exit( )

Import( "pE" )
pE.Import( "c_fileIntactC" )
c_strID				= arepa.cwd( )
c_fileIDTXT			= pE.File( c_strID + ".txt" )
c_fileIDDAB			= pE.File( c_strID + ".dab" )
c_fileProgC2TXT		= pE.File( arepa.d( arepa.path_repo( pE ), arepa.c_strDirSrc, "c2txt.py" ) )
c_fileProgC2DAT		= pE.File( arepa.d( arepa.path_repo( pE ), arepa.c_strDirSrc, "c2dat.py" ) )

afileIDTXT = arepa.pipe( pE, c_fileIntactC, c_fileProgC2TXT, c_fileIDTXT, [[False, c_strID]] )
pE.Default( afileIDTXT )

def funcDAB( target, source, env ):
	strT, astrSs = arepa.ts( target, source )
	strProg, strIn = astrSs
	return arepa.ex( " ".join( [strProg, c_strID, "<", strIn, "| Dat2Dab -o", strT] ) )
afileIDDAB = pE.Command( c_fileIDDAB, [c_fileProgC2DAT, c_fileIntactC], funcDAB )
pE.Default( afileIDDAB )
