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
import os
import sfle
import sys
import metadata
import glob


def test( iLevel, strID, hashArgs ):
	return ( iLevel == 1 )
if locals( ).has_key( "testing" ):
	sys.exit( )

pE = DefaultEnvironment( )

c_strID					= arepa.cwd( )
c_fileInputC				= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirTmp, "mpidbc" ) 
c_fileIDPKL				= sfle.d( pE, c_strID + ".pkl" )
c_fileIDDAB				= sfle.d( pE, c_strID + ".dab" )
c_fileIDQUANT			 	= sfle.d( c_strID + ".quant" )
c_fileIDRawDAT			 	= sfle.d( pE, c_strID + "_00raw.dat" )
c_fileIDDAT					= sfle.d( pE, c_strID + ".dat")

c_fileProgUnpickle			= sfle.d( pE, arepa.path_arepa( ), sfle.c_strDirSrc, "unpickle.py" )
c_fileProgC2Metadata			= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "c2metadata.py" ) 
c_fileProgC2DAT				= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "c2dat.py" ) 
c_fileInputManCurTXT		= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirEtc, "manual_curation/", c_strID + sfle.c_strSufTXT )

c_fileInputSConscriptGM		= sfle.d( pE, arepa.path_arepa(),sfle.c_strDirSrc,"SConscript_genemapping.py")
c_fileInputSConscriptDAB	= sfle.d( pE, arepa.path_arepa(), sfle.c_strDirSrc, "SConscript_dat-dab.py" )
c_fileStatus			= sfle.d(pE, "status.txt")

afileIDDAT = sfle.pipe( pE, c_fileInputC, c_fileProgC2DAT, c_fileIDRawDAT, [c_strID] )

##############################################
#- Gene id mapping from Uniprot to Genesymbols
##############################################

#Launch gene mapping 
execfile(str(c_fileInputSConscriptGM))
astrMapped = funcGeneIDMapping( pE, c_fileIDRawDAT, arepa.genemap_uniref( ), c_fileStatus )

#Make identifiers unique 
astrUnique = funcMakeUnique( pE, astrMapped[0] )

afileIDTXT = sfle.pipe( pE, c_fileInputC, c_fileProgC2Metadata, c_fileIDPKL,[c_strID,[c_fileStatus]] + ([[c_fileInputManCurTXT]] if os.path.exists(str(c_fileInputManCurTXT)) else []))

execfile(str(c_fileInputSConscriptDAB))

#DAT to DAB
astrDAB = funcDAB( pE, c_fileIDDAB, [c_fileIDRawDAT, astrUnique[0]] )
funcPCL( pE, c_fileIDDAT, astrUnique[0] )
funcQUANT( pE, c_fileIDQUANT )
