#!/usr/bin/env python

import arepa
import os
import sys

if __name__ == "__main__":
	iLevel, strTo, strFrom = arepa.scons_args( sys.argv )
	sys.exit( 0 if ( iLevel == 1 ) else 1 )

c_strID				= arepa.dir( )
c_fileIDTXT			= File( c_strID + ".txt" )
c_fileIDDAB			= File( c_strID + ".dab" )
c_fileProgC2TXT		= File( arepa.d( arepa.path_repo( ), arepa.c_strDirSrc, "c2txt.py" ) )
c_fileProgC2DAT		= File( arepa.d( arepa.path_repo( ), arepa.c_strDirSrc, "c2dat.py" ) )

Import( "c_fileIntactC" )
Import( "pE" )

afileIDTXT = arepa.pipe( pE, c_fileIntactC, c_fileProgC2TXT, c_fileIDTXT, [[False, c_strID]] )
Default( afileIDTXT )

def funcDAB( target, source, env ):
	strT, astrSs = arepa.ts( target, source )
	strProg, strIn = astrSs
	return arepa.ex( " ".join( [strProg, c_strID, "<", strIn, "| Dat2Dab -o", strT] ) )
afileIDDAB = pE.Command( c_fileIDDAB, [c_fileProgC2DAT, c_fileIntactC], funcDAB )
Default( afileIDDAB )
