#!/usr/bin/env python

import arepa
import os
import sys

def test( iLevel, strID, hashArgs ):
	return ( iLevel == 2 ) and ( strID.find( "E-GEOD-11810" ) >= 0 )
if "testing" in locals( ):
	sys.exit( )

#Import( "pE" )
#Import( "hashArgs" )
c_strID					= arepa.cwd( )
c_strFileIDTXT			= c_strID + ".txt"

def funcTest( target, source, env ):
	strT, astrSs = arepa.ts( target, source )
	with open( strT, "w" ) as fileOut:
		fileOut.write( "Hi!\n" )
	return None
arepa.override( pE, c_strFileIDTXT )
Command( c_strFileIDTXT, None, funcTest )
Default( c_strFileIDTXT )
