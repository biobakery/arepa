#!/usr/bin/env python

import arepa
import sfle
import sys 
import ftplib

def test( iLevel, strID, hashArgs ):
	return ( iLevel == 3 ) and ( strID.find( "GSE" ) == 0 )
if locals( ).has_key( "testing" ):
	sys.exit( )

c_strURLGEO					= 'ftp.ncbi.nih.gov'
c_strURLGEOsupp					= 'pub/geo/DATA/supplementary/samples/'
c_strURLSupp 					= 'ftp://' + c_strURLGEO + '/' + c_strURLGEOsupp 
c_strFileGSM					= "../GSM.txt"
c_strFileCEL                                    = "CEL.txt"

pE = DefaultEnvironment( )
Import( "hashArgs" )

def nnnModify( strID ):
	return strID[0:len(strID)-3] + "nnn/"

def funcGetListRAW( GSMfile, dummylist = None ):
	if not dummylist:
		dummylist = []
	listGSM = sfle.readcomment( GSMfile )
	for GSMid in listGSM:
			c_strURLGSM		= nnnModify( GSMid ) + GSMid
			c_strURLGSMftpbase	= c_strURLGEOsupp + c_strURLGSM
			c_listFiles		= sfle.ftpls( c_strURLGEO, c_strURLGSMftpbase ) 
			dummylist += filter( ( lambda str: 'CEL' in str ), c_listFiles )
	return dummylist

#def funcWriteListRAW( target, source, env, dummylist = None ):
#	if not dummylist:
#		dummylist = []
#	CELfile, GSMfile = target[0], source[0] 
#	listGSM = sfle.readcomment( GSMfile )
#	for GSMid in listGSM:
#		c_strURLGSM		= nnnModify( GSMid ) + GSMid
#		c_strURLGSMftpbase	= c_strURLGEOsupp + c_strURLGSM
#		c_listFiles		= sfle.ftpls( c_strURLGEO, c_strURLGSMftpbase ) 
#		dummylist += filter( ( lambda str: 'CEL' in str ), c_listFiles )
#	with open( str( CELfile ), "w" ) as outputf:
#		outputf.write( "\n".join( dummylist ) )

#def funcEnvDownloadRAW( target, source, env ):
#	alistTs = target  
#	for GSMCEL in alistTs:
#		GSMid = str( GSMCEL ).split(".")[0]
#		sfle.download( pE, c_strURLSupp + nnnModify( GSMid ) + GSMid + "/" + str( GSMCEL ) )

def funcDownloadRAW( target ):
	alistTs = target  
	for GSMCEL in alistTs:
		GSMid = str( GSMCEL ).split(".")[0]
		sfle.download( pE, c_strURLSupp + nnnModify( GSMid ) + GSMid + "/" + str( GSMCEL ) )


listCEL = funcGetListRAW( c_strFileGSM )
print listCEL
alistRAWfiles = funcDownloadRAW( listCEL )


# Insert RAW pipeline

			

