#!/usr/bin/env python

import arepa
import gzip
import os
import re
import sfle
import sys

def test( iLevel, strID, hashArgs ):
	return ( iLevel == 1 ) and ( strID.find( "GDS" ) == 0 )
if locals( ).has_key( "testing" ):
	sys.exit( )

c_strID					= arepa.cwd( )
c_fileIDTXT				= File( c_strID + ".txt" )
c_fileIDSOFTGZ			= File( c_strID + ".soft.gz" )

pE = DefaultEnvironment( )
Import( "hashArgs" )

#===============================================================================
# Download SOFT file
#===============================================================================

sfle.download( pE, hashArgs["c_strURLGDS"] + os.path.basename( str(c_fileIDSOFTGZ) ) )
NoClean( c_fileIDSOFTGZ )

def funcGPLsTXT( target, source, env ):
	strT, astrSs = sfle.ts( target, source )
	setstrGPLs = set()
	for strLine in gzip.open( astrSs[0] ):
		mtch = re.search( r'^!dataset_platform\s*=\s*(\S+)', strLine )
		if mtch:
			setstrGPLs.add( mtch.group( 1 ) )
	with open( strT, "w" ) as fileOut:
		fileOut.write( "%s\n" % "\n".join( ("-".join( (c_strID, s) ) for s in setstrGPLs) ) )
	return None
afileGPLsTXT = Command( c_fileIDTXT, c_fileIDSOFTGZ, funcGPLsTXT )

sfle.sconscript_children( pE, afileGPLsTXT, sfle.scanner( ), 2, arepa.c_strProgSConstruct, hashArgs )
