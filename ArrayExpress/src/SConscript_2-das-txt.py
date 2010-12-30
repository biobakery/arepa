#!/usr/bin/env python

import arepa
import sys

def test( iLevel, strID, hashArgs ):
	return ( iLevel == 2 )
if locals( ).has_key( "testing" ):
	sys.exit( )

Import( "pE" )
Import( "hashArgs" )
c_strID					= arepa.cwd( )
c_strType				= c_strID[2:6]
c_strInputIDSDRF		= hashArgs["strFileIDSDRF"]
c_strInputIDIDF			= hashArgs["strFileIDIDF"]
c_strInputTaxdumpTXT	= arepa.d( arepa.path_arepa( ), arepa.c_strDirTmp, "taxdump.txt" )
c_astrInputADFs			= hashArgs["astrFileADFs"]
c_strFileIDTXT			= c_strID + ".txt"
c_strProgIDF2TXT		= arepa.d( arepa.path_repo( ), arepa.c_strDirSrc, "idf2txt.py" )

arepa.pipe( pE, c_strInputIDIDF, c_strProgIDF2TXT, c_strFileIDTXT,
	[[True, s] for s in ( [c_strInputTaxdumpTXT, c_strInputIDSDRF] + c_astrInputADFs )] )
Default( c_strFileIDTXT )
