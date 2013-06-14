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
import sfle
import sys 
import ftplib
import re 

def test( iLevel, strID, hashArgs ):
	return ( iLevel == 3 ) and ( strID.find( "GSE" ) == 0 )
if locals( ).has_key( "testing" ):
	sys.exit( )

pE = DefaultEnvironment( )

c_strID				= arepa.cwd().replace("-RAW","")
c_strURLGEO			= 'ftp.ncbi.nih.gov'
c_strURLGEOsupp			= 'pub/geo/DATA/supplementary/samples/'
c_strURLSupp 			= 'ftp://' + c_strURLGEO + '/' + c_strURLGEOsupp 
c_strFileGSM			= "../GSM.txt"
c_strFilePCL			= "../" + c_strID + ".pcl" 

c_listTs			= sfle.readcomment( c_strFileGSM )
c_fileProgReadCel		= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "readCel.R" ) 
c_fileProgProcessRaw		= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "preprocessRaw.R" ) 
c_strInputRData			= arepa.cwd() + ".RData"
c_strOutputRData		= c_strInputRData.replace("-RAW", "") 

c_filePPfun			= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirEtc, "preprocess")
c_strPPfun			= sfle.readcomment( c_filePPfun )[0] if \
					sfle.readcomment( c_filePPfun ) else "affy::rma"

c_fileExpTable			= sfle.d( pE,  "../" + c_strID + "_exp_metadata.txt" )
c_fileCondTable			= sfle.d( pE, "../" + c_strID + "_cond_metadata.txt" )
 
Import( "hashArgs" )

#Download CEL files (if they exist)

def funcDownloadRAW( alistTs ):
	def _nnnModify( strID ):
		strStrip = re.findall(r'GSM\d+', strID )[0]	
		strNNN = strStrip[0:len(strStrip)-3] + "nnn/"
		return strNNN, strStrip 
	for GSMCEL in alistTs:
		GSMid = str( GSMCEL ).split(".")[0]
		sfle.download( pE, sfle.d( c_strURLSupp, _nnnModify( GSMid )[0] ,\
			_nnnModify( GSMid )[1], str(GSMCEL) ) )

#Get a single RData input file from the CEL files
def funcRawMap( target, source, env ):
	astrTs, astrSs = ([f.get_abspath( ) for f in a] for a in (target, source))
	strOutputRData = astrTs[0]
	strIn, astrCel = astrSs[0], astrSs[1:]
	return sfle.ex( [sfle.cat( strIn ), " | R --no-save --args", strOutputRData] + astrCel)
	
#Take the RData file produced by funcRawMap and process

def funcRawProcess( target, source, env ):
	strT, astrSs = sfle.ts(target, source)
	strIn, strRData, strExpMetadata, strCondMetadata = astrSs[:4]
	iRet = sfle.ex( (sfle.cat(strIn), "| R --no-save", "--args", strRData, strT, c_strPPfun, strExpMetadata, strCondMetadata) )
	if iRet:
		iRet = sfle.ex( (sfle.cat( strIn ), " | R --no-save --args", c_strFilePCL, strT, c_strPPfun, strExpMetadata, strCondMetadata ) )
	return iRet

#if RAW files exist, process
if c_listTs:
	funcDownloadRAW( c_listTs )
	Command( c_strInputRData, [c_fileProgReadCel] + c_listTs , funcRawMap )
	Command( c_strOutputRData, [c_fileProgProcessRaw,c_strInputRData, c_fileExpTable, c_fileCondTable],\
		 funcRawProcess )
#else use vanilla pcl
else:
	Command( c_strOutputRData, [c_fileProgProcessRaw,c_strFilePCL, c_fileExpTable, c_fileCondTable],\
		 funcRawProcess )	
