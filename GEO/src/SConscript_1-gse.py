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
import re
import sfle
import sys

def test( iLevel, strID, hashArgs ):
	return ( iLevel == 1 ) and ( strID.find( "GSE" ) == 0 )
if "testing" in locals( ):
	sys.exit( )
pE = DefaultEnvironment( )

c_strID						= arepa.cwd( )
c_strHost					= "ftp.ncbi.nih.gov"
c_strPath					= "pub/geo/DATA/SeriesMatrix/"

c_fileIDTXT					= sfle.d( pE, c_strID + ".txt" )

Import( "hashArgs" )

#==============================================================================
# Fetch platform count and recurse
#==============================================================================

def funcIDsTXT( target, source, env ):
	strT, astrSs = sfle.ts( target, source )
	astrFiles = sfle.ftpls( c_strHost, sfle.d( c_strPath, c_strID ) )
	astrFiles = [mtch.group( 1 ) for mtch in 
		[_f for _f in (re.search( r'(GSE\d+(?:-GPL\d+)?)', s ) for s in astrFiles) if _f]]
	with open( strT, "w" ) as fileOut:
		fileOut.write( "%s\n" % "\n".join( astrFiles ) )
	return None
		 
afileIDsTXT = Command( c_fileIDTXT, None, funcIDsTXT )

sfle.sconscript_children( pE, afileIDsTXT, sfle.scanner( ), 2, arepa.c_strProgSConstruct, hashArgs )

