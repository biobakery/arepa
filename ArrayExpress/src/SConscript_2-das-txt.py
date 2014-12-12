#!/usr/bin/env python

import arepa
import sys

def test( iLevel, strID, hashArgs ):
	return ( iLevel == 2 )
if "testing" in locals( ):
	sys.exit( )

#Import( "pE" )
#Import( "hashArgs" )
c_strID					= arepa.cwd( )
c_strInputIDSDRF		= hashArgs["strFileIDSDRF"]
c_strInputIDIDF			= hashArgs["strFileIDIDF"]
c_astrInputADFs			= hashArgs["astrFileADFs"]
c_strFileIDTXT			= c_strID + ".txt"
c_strProgIDF2Metadata	= arepa.d( arepa.path_repo( ), arepa.c_strDirSrc, "idf2metadata.py" )

arepa.pipe( pE, c_strInputIDIDF, c_strProgIDF2Metadata, c_strFileIDTXT,
	[[True, s] for s in ( [c_strInputIDSDRF] + c_astrInputADFs )] )
Default( c_strFileIDTXT )
