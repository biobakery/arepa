#!/usr/bin/env python

import os
import re
import subprocess
import sys

c_strData		= "data/"
c_strEtc		= "etc/"
c_strSource		= "src/"
c_strTmp		= "tmp/"
c_strFileTaxids	= c_strTmp + "taxids"
c_astrExclude	= [strCur[:-1] for strCur in (c_strEtc, c_strSource, c_strTmp)] + [
#	"ArrayExpress"
#	"IntAct"
]

#===============================================================================
# Basic global utilities
#===============================================================================

def regs( strRE, strString, aiGroups ):

	try:
		iter( aiGroups )
	except TypeError:
		aiGroups = (aiGroups,)
	mtch = re.search( strRE, strString )
	astrRet = [mtch.group( i ) for i in aiGroups] if mtch else \
		( [""] * len( aiGroups ) )
	return ( astrRet if ( not aiGroups or ( len( aiGroups ) > 1 ) ) else astrRet[0] )

def aset( a, i, p, fSet = True ):
	
	if len( a ) <= i:
		a.extend( [None] * ( 1 + i - len( a ) ) )
	if fSet:
		a[i] = p
	return a[i]

def entable( fileIn, afuncCols ):
	
	aiCols = [None] * len( afuncCols )
	aastrRet = []
	for strLine in fileIn:
		astrLine = [strCur.strip( ) for strCur in strLine.split( "\t" )]
		if all( ( i != None ) for i in aiCols ):
			if len( astrLine ) > max( aiCols ):
				aastrRet.append( [astrLine[i] for i in aiCols] )
		for i in range( len( astrLine ) ):
			for j in range( len( afuncCols ) ):
				if afuncCols[j]( astrLine[i] ):
					aiCols[j] = i
	return aastrRet

def readcomment( fileIn ):
	
	astrRet = []
	for strLine in fileIn:
		strLine = strLine.strip( )
		if ( not strLine ) or ( strLine[0] == "#" ):
			continue
		astrRet.append( strLine )

	return astrRet

def check_output( strCmd ):
	
	proc = subprocess.Popen( strCmd, shell = True, stdout = subprocess.PIPE )
	return proc.communicate( )[0]

#===============================================================================
# SCons utilities
#===============================================================================

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
		pProc.communicate( )
		return pProc.wait( )
	with open( strOut, "w" ) as fileOut:
		fileOut.write( strLine )
		for strLine in pProc.stdout:
			fileOut.write( strLine )
	return pProc.wait( )

def ts( afileTargets, afileSources ):

	return (str(afileTargets[0]), [fileCur.get_abspath( ) for fileCur in afileSources])

#===============================================================================
# Command execution
#===============================================================================

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

def spipe( pE, strFrom, strCmd, strTo ):
	def funcPipe( target, source, env, strCmd = strCmd ):
		strT, astrSs = ts( target, source )
		return ex( " ".join( [strCmd] + ( ["<", strFrom] if strFrom else [] ) ),
			strT )
	return pE.Command( strTo, strFrom if strFrom else None, funcPipe )

#===============================================================================
# ARepA structural metadata
#===============================================================================

def dir( pE, fBase = True ):

	strRet = pE.Dir( "." ).get_abspath( )
	if fBase:
		strRet = os.path.basename( strRet )
		return strRet

def taxa( strTaxids, fNames = False ):
	
	setRet = set()
	if strTaxids:
		for strLine in open( strTaxids ):
			strID, strName = strLine.strip( ).split( "\t" )
			setRet.add( strName if fNames else strID )
	return setRet

def path_arepa( ):
	
	return ( os.path.abspath( os.path.dirname( __file__ ) + "/../" ) + "/" )

def path_repo( pE ):
	
	strRet = os.path.abspath( pE.Dir( "." ).get_abspath( ) )
	strRet = strRet[len( path_arepa( ) ):]
	while True:
		strHead, strTail = os.path.split( strRet )
		if not strHead:
			strRet = path_arepa( ) + strRet
			break
		strRet = strHead
	return ( strRet + "/" )

def level( pE, fileDir ):
	
	strPath = path_repo( pE )
	strPath = fileDir.get_abspath( )[len( strPath ):]
	iRet = 0
	while True:
		strHead, strTail = os.path.split( strPath )
		if not strHead:
			break
		iRet += 1
		strPath = strHead
	return iRet

#===============================================================================
# SConstruct helper functions
#===============================================================================

def scons_args( astrArgs ):
	
	iLevel = 0 if ( len( astrArgs ) <= 1 ) else int(astrArgs[1])
	strTo = "" if ( len( astrArgs ) <= 2 ) else astrArgs[2]
	strFrom = "" if ( len( astrArgs ) <= 3 ) else astrArgs[3]
	
	return (iLevel, strTo, strFrom)

def sconstruct( pE, fileDir, fileSource = None ):

	fileDir = pE.Dir( fileDir )
	strDir = str(fileDir)
	strSConstruct = strDir + "/SConstruct"
	for fileSConstruct in pE.Glob( path_repo( pE ) + c_strSource + "SConstruct*.py" ):
		astrArgs = [str(p) for p in ( [level( pE, fileDir ), fileDir] + \
			( [fileSource] if fileSource else [] ) )]
		if subprocess.call( " ".join( [str(fileSConstruct)] + astrArgs ),
			shell = True ):
			continue 
		def funcDir( target, source, env ):
			strT, astrSs = ts( target, source )
			return ex( "ln -fs " + astrSs[0] + " " + strT )
		pE.Command( strSConstruct, fileSConstruct, funcDir )

	def funcSConstruct( target, source, env, strDir = strDir ):
		return ex( "scons -C " + strDir )
	pE.Default( pE.Command( strDir + ".tmp", strSConstruct, funcSConstruct ) )

if __name__ == "__main__":
	pass
