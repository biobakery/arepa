#!/usr/bin/env python

import os
import re
import subprocess
import sys

c_strEtc		= "etc/"
c_strSource		= "src/"
c_strTmp		= "tmp/"
c_astrExclude	= [strCur[:-1] for strCur in (c_strEtc, c_strSource, c_strTmp)] + [
#	"ArrayExpress"
	"IntAct"
]

def ex( strCmd, strOut = None ):
	
	sys.stdout.write( "%s" % strCmd )
	sys.stdout.write( ( ( " > %s" % strOut ) if strOut else "" ) + "\n" )
	if not strOut:
		return subprocess.call( strCmd, shell = True )
	pProc = subprocess.Popen( strCmd, shell = True, stdout = subprocess.PIPE )
	if not pProc:
		return 1
	strLine = pProc.stdout.readline( )
	if not strLine:
		return 1
	with open( strOut, "w" ) as fileOut:
		fileOut.write( strLine )
		for strLine in pProc.stdout:
			fileOut.write( strLine )
	return pProc.wait( )

def ts( astrTargets, astrSources ):

	return (str(astrTargets[0]), [pF.get_abspath( ) for pF in astrSources])

def download( pE, strT, strURL ):
	def funcDownload( target, source, env, strURL = strURL ):
		strT, astrSs = ts( target, source )
		iRet = ex( " ".join( ("curl", "-f", "-z", strT, strURL) ), strT )
# 19 is curl's document-not-found code
		return ( iRet if ( iRet != 19 ) else 0 )
	return pE.Command( strT, None, funcDownload )

def pipe( pE, strFrom, strProg, strTo, aaArgs = [] ):
	astrFiles = []
	astrArgs = []
	for aArg in aaArgs:
		fFile, strArg = aArg[0], str(aArg[1])
		if fFile:
			astrFiles.append( strArg )
		astrArgs.append( strArg )
	def funcPipe( target, source, env, strFrom = strFrom, astrArgs = astrArgs ):
		strT, astrSs = ts( target, source )
		return ex( " ".join( [astrSs[0]] + astrArgs +
			( ["<", strFrom] if strFrom else [] ) ), strT )
	return pE.Command( strTo, [strProg] + ( [strFrom] if strFrom else [] ) +
		astrFiles, funcPipe )

def cmd( pE, strProg, strTo, aaArgs = [] ):
	return pipe( pE, None, strProg, strTo, aaArgs )

def regs( strRE, strString, aiGroups ):

	try:
		iter( aiGroups )
	except TypeError:
		aiGroups = (aiGroups,)
	mtch = re.search( strRE, strString )
	astrRet = [mtch.group( i ) for i in aiGroups] if mtch else \
		( [""] * len( aiGroups ) )
	return ( astrRet if ( not aiGroups or ( len( aiGroups ) > 1 ) ) else astrRet[0] )

def dir( pE, fBase = True ):
	
	strRet = pE.Dir( "." ).get_abspath( )
	if fBase:
		strRet = os.path.basename( strRet )
	return strRet

def aset( a, i, p, fSet = True ):
	
	if len( a ) <= i:
		a.extend( [None] * ( 1 + i - len( a ) ) )
	if fSet:
		a[i] = p
	return a[i]

def taxa( strTaxids, fNames = False ):
	
	setRet = set()
	if strTaxids:
		for strLine in open( strTaxids ):
			strID, strName = strLine.strip( ).split( "\t" )
			setRet.add( strName if fNames else strID )
	return setRet
