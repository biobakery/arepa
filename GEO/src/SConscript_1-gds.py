#!/usr/bin/env python
"""
ARepA: Automated Repository Acquisition 

ARepA is licensed under the MIT license.

Copyright (C) 2013 Yo Sup Moon, Daniela Boernigen, Levi Waldron, Eric Franzosa, Xochitl Morgan, and Curtis Huttenhower

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation 
files (the "Software"), to deal in the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons 
to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or 
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import arepa
import gzip
import os
import re
import sfle
import sys

def test( iLevel, strID, hashArgs ):
	return ( iLevel == 1 ) and ( strID.find( "GDS" ) == 0 )
if "testing" in locals( ):
	sys.exit( )

pE = DefaultEnvironment( )

c_strID				= arepa.cwd( )
c_fileIDTXT			= sfle.d( pE, c_strID + ".txt" )
c_fileIDSOFTGZ		= sfle.d( pE, c_strID + ".soft.gz" )

Import( "hashArgs" )

#===============================================================================
# Download SOFT file
#===============================================================================

sfle.download( pE, hashArgs["c_strURLGDS"] + os.path.basename( str(c_fileIDSOFTGZ) ) )

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
