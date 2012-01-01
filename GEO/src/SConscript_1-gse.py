#!/usr/bin/env python

import arepa
import re
import sfle
import sys

def test( iLevel, strID, hashArgs ):
	return ( iLevel == 1 ) and ( strID.find( "GSE" ) == 0 )
if locals( ).has_key( "testing" ):
	sys.exit( )

c_strID						= arepa.cwd( )
c_strHost					= "ftp.ncbi.nih.gov"
c_strPath					= "pub/geo/DATA/SeriesMatrix/"

c_fileIDTXT					= File( c_strID + ".txt" )

pE = DefaultEnvironment( )
Import( "hashArgs" )

#==============================================================================
# Fetch platform count and recurse
#==============================================================================

def funcIDsTXT( target, source, env ):
	strT, astrSs = sfle.ts( target, source )
	astrFiles = sfle.ftpls( c_strHost, sfle.d( c_strPath, c_strID ) )
	astrFiles = [mtch.group( 1 ) for mtch in 
		filter( None, (re.search( r'(GSE\d+(?:-GPL\d+)?)', s ) for s in astrFiles) )]
	with open( strT, "w" ) as fileOut:
		fileOut.write( "%s\n" % "\n".join( astrFiles ) )
	return None 
afileIDsTXT = Command( c_fileIDTXT, None, funcIDsTXT )

sfle.sconscript_children( pE, afileIDsTXT, sfle.scanner( ), 2, arepa.c_strProgSConstruct, hashArgs )
