#!/usr/bin/env python

import arepa
import sfle
import sys 
import ftplib

def test( iLevel, strID, hashArgs ):
	return ( iLevel == 3 ) and ( strID.find( "GSE" ) == 0 )
if locals( ).has_key( "testing" ):
	sys.exit( )

c_strID				= arepa.cwd().replace("-RAW","")
c_strURLGEO			= 'ftp.ncbi.nih.gov'
c_strURLGEOsupp			= 'pub/geo/DATA/supplementary/samples/'
c_strURLSupp 			= 'ftp://' + c_strURLGEO + '/' + c_strURLGEOsupp 
c_strFileGSM			= "../GSM.txt"
c_strFilePCL			= "../" + c_strID + "_00mapped.pcl" 

c_listTs			= sfle.readcomment( c_strFileGSM )
c_fileProgReadCel		= File( sfle.d( arepa.path_repo( ), sfle.c_strDirSrc, "readCel.R" ) )
c_fileProgProcessRaw		= File( sfle.d( arepa.path_repo( ), sfle.c_strDirSrc, "preprocessRaw.R" ) )
c_strInputRData			= arepa.cwd() + ".RData"
c_strOutputRData		= c_strInputRData.replace("-RAW", "") 

c_filePPfun            		= File( sfle.d( arepa.path_repo( ), sfle.c_strDirEtc, "preprocess"))
c_strPPfun			= sfle.readcomment( c_filePPfun )[0] if \
				sfle.readcomment( c_filePPfun ) else "affy::rma"

c_fileExpTable			= File( "../" + c_strID + "_exp_metadata.txt" )
c_fileCondTable			= File( "../" + c_strID + "_cond_metadata.txt" )
 
pE = DefaultEnvironment( )
Import( "hashArgs" )

#Download CEL files (if they exist)

def funcDownloadRAW( alistTs ):
	def nnnModify( strID ):
        	return strID[0:len(strID)-3] + "nnn/"
	for GSMCEL in alistTs:
		GSMid = str( GSMCEL ).split(".")[0]
		sfle.download( pE, c_strURLSupp + nnnModify( GSMid ) + GSMid + "/" + str( GSMCEL ) )
	
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
        return sfle.ex( (sfle.cat( strIn ), " | R --no-save --args", strRData, strT, \
		c_strPPfun, strExpMetadata, strCondMetadata ) )

#Execute

#if RAW files exist, process
if c_listTs:
	funcDownloadRAW( c_listTs )
	Command( c_strInputRData, [c_fileProgReadCel] + c_listTs , funcRawMap )
	Command( c_strOutputRData, [c_fileProgProcessRaw,c_strInputRData, c_fileExpTable, c_fileCondTable],\
		 funcRawProcess )
#else use vanilla pcl
else:
	Command( c_strOutputRData, [c_fileProgProcessRaw,c_strFilePCL], funcRawProcess )	
