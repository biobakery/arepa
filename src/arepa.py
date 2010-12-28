#!/usr/bin/env python

import glob
import os
import re
import subprocess
import sys
import urllib

c_strDirData	= "data/"
c_strDirEtc		= "etc/"
c_strDirSrc		= "src/"
c_strDirTmp		= "tmp/"
c_astrExclude	= [strCur[:-1] for strCur in (c_strDirEtc, c_strDirSrc, c_strDirTmp)] + [
	"ArrayExpress",
#	"IntAct",
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

def d( *astrArgs ):
	
	return "/".join( astrArgs )

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

def download( pE, strURL, strT = None, fSSL = False ):

	if not strT:
		strT = re.sub( '^.*\/', "", strURL )

	def funcDownload( target, source, env, strURL = strURL ):
		strT, astrSs = ts( target, source )
		iRet = ex( " ".join( ("curl", "--ftp-ssl -k" if fSSL else "", "-f", "-z", strT, strURL) ), strT )
# 19 is curl's document-not-found code
		return ( iRet if ( iRet != 19 ) else 0 )
	return pE.Command( strT, None, funcDownload )

def _pipeargs( aaArgs ):

	astrFiles = []
	astrArgs = []
	for aArg in aaArgs:
		fFile, strArg = aArg[0], str(aArg[1])
		if fFile:
			astrFiles.append( strArg )
			strArg = "\"" + strArg + "\""
		astrArgs.append( strArg )
	return (astrFiles, astrArgs)

def pipe( pE, strFrom, strProg, strTo, aaArgs = [] ):
	astrFiles, astrArgs = _pipeargs( aaArgs )
	def funcPipe( target, source, env, strFrom = strFrom, astrArgs = astrArgs ):
		strT, astrSs = ts( target, source )
		return ex( " ".join( [astrSs[0]] + astrArgs +
			( ["<", str(strFrom)] if strFrom else [] ) ), strT )
	return pE.Command( strTo, [strProg] + ( [strFrom] if strFrom else [] ) +
		astrFiles, funcPipe )

def cmd( pE, strProg, strTo, aaArgs = [] ):

	return pipe( pE, None, strProg, strTo, aaArgs )

def spipe( pE, strFrom, strCmd, strTo, aaArgs = [] ):
	astrFiles, astrArgs = _pipeargs( aaArgs )
	def funcPipe( target, source, env, strCmd = strCmd, strFrom = strFrom, astrArgs = astrArgs ):
		strT, astrSs = ts( target, source )
		return ex( " ".join( [strCmd] + astrArgs + ( ["<", strFrom] if strFrom else [] ) ),
			strT )
	return pE.Command( strTo, ( [strFrom] if strFrom else [] ) + astrFiles, funcPipe )

def scmd( pE, strCmd, strTo, aaArgs = [] ):

	return spipe( pE, None, strCmd, strTo, aaArgs )

#===============================================================================
# ARepA structural metadata
#===============================================================================

def dir( ):

	return os.path.basename( os.getcwd( ) )

def taxa( strTaxids, fNames = False ):
	
	setRet = set()
	if strTaxids:
		for strLine in open( strTaxids ):
			strID, strName = strLine.strip( ).split( "\t" )
			setRet.add( strName if fNames else strID )
	return setRet

def path_arepa( ):
	
	return ( os.path.abspath( os.path.dirname( __file__ ) + "/../" ) + "/" )

def path_repo( ):
	
	strRet = os.getcwd( )
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

"""
def sconstruct( pE, fileDir, fileSource = None ):

	fileDir = pE.Dir( fileDir )
	strDir = str(fileDir)
	strSConstruct = strDir + "/SConstruct"
	for fileSConstruct in pE.Glob( path_repo( pE ) + c_strDirSrc + "SConstruct*.py" ):
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
"""

def scons_child( pE, fileDir, hashExport = {}, fileSConscript = None ):

	strDir, strSConscript = (( ( os.path.abspath( f ) if ( type( f ) == str ) else f.get_abspath( ) ) if f else None )
		for f in (fileDir, fileSConscript))
	astrExport = []
	for strKey, pValue in hashExport.items( ):
		if ( strKey not in locals( ) ) and ( strKey.find( " " ) < 0 ):
			astrExport.append( strKey )
			globals( )[strKey] = pValue
	if fileSConscript:
		try:
			os.makedirs( strDir )
		except os.error:
			pass
		subprocess.call( ["ln", "-f", "-s", strSConscript, d( strDir, "SConscript" )] )
	pE.SConscript( dirs = [strDir], exports = "pE " + " ".join( astrExport ) )

def scons_children( pE, hashExport = {} ):

	for fileCur in pE.Glob( "*" ):
		if ( type( fileCur ) == type( pE.Dir( "." ) ) ) and \
			( str(fileCur) not in c_astrExclude ):
			scons_child( pE, fileCur, hashExport )

#------------------------------------------------------------------------------ 
# Helper functions for SConscript subdirectories auto-generated from a scanned
# input file during the build process.  Extremely complex; intended usage is:
# def funcScanner( target, source, env ):
#	for fileSource in source:
#		for strLine in open( str(fileSource) ):
#			if strLine.startswith( ">" ):
#				env["sconscript_child"]( target, fileSource, env, strLine[1:].strip( ) )
# arepa.sconscript_children( pE, afileIntactC, funcScanner, 1, globals( ) )
#------------------------------------------------------------------------------ 

def sconscript_child( target, source, env, strID, iLevel, hashExport = {} ):

	fileTarget = target[0] if ( type( target ) == list ) else target
	os.chdir( os.path.dirname( str(fileTarget) ) )
	strSource = source
	if type( strSource ) == list:
		strSource = source[0]
	if type( strSource ) != str:
		strSource = strSource.get_abspath( )
	for fileSConscript in glob.glob( arepa.d( arepa.c_strDirSrc, "SConscript*" ) ):
		if not subprocess.call( " ".join( [str(fileSConscript), str(iLevel), strID, strSource] ), shell = True ):
			scons_child( env, arepa.d( arepa.c_strDirData, strID ), hashExport, fileSConscript )
			break

def sconscript_scanner( target, source, env, funcScanner ):
	strDir = os.getcwd( )
	funcScanner( target, source, env )
	os.chdir( strDir )

def sconscript_children( pE, afileSources, funcScanner, iLevel, hashExport = {} ):

	pE.Append( BUILDERS = {"SConsChildren" : Builder(
		action = lambda target, source, env, funcScanner = funcScanner: sconscript_scanner( target, source, env, funcScanner ) )} )
	afileSubdirs = pE.SConsChildren( "dummy", afileSources,
		sconscript_child = lambda target, source, env, strID, iLevel = iLevel, hashExport = hashExport: sconscript_child( target, source, env, strID, iLevel, hashExport ) )
	pE.AlwaysBuild( afileSubdirs )

#===============================================================================
# Gene ID conversion
#===============================================================================

def geneid( strIn, strTaxID, strTarget = "Entrez Gene", strURLBase = "http://localhost:8183" ):
	
# BUGBUG: This is one of the worst things I've ever done
	hashTaxIDs = globals( ).get( "hashTaxIDs", {} )
	strTaxon = hashTaxIDs.get( strTaxID )
	if not strTaxon:
		strTaxIDs = d( path_arepa( ), c_strDirTmp, "taxids" )
		try:
			for strLine in open( strTaxIDs ):
				strFrom, strTo = strLine.strip( ).split( "\t" )
				if strFrom == strTaxID:
					strTaxon = " ".join( strTo.split( " " )[:2] )
					break
		except IOError:
			pass
	if not strTaxon:
		return strIn
	strTaxon = urllib.quote( strTaxon ).replace( "/", "%2F" )

	strURL = strURLBase + "/" + strTaxon + "/search/" + urllib.quote( strIn )
	astrData = urllib.urlopen( strURL ).read( ).splitlines( )
	strID = strSource = None
	for strLine in astrData:
		astrLine = strLine.strip( ).split( "\t" )
		if astrLine[0] == strIn:
			strID, strSource = astrLine
			break
	if not ( strID and strSource ):
		return strIn
	strSource = urllib.quote( strSource ).replace( "/", "%2F" )

	strURL = strURLBase + "/" + strTaxon + "/xrefs/" + strSource + "/" + urllib.quote( strID )
	astrData = urllib.urlopen( strURL ).read( ).splitlines( )
	for strLine in astrData:
		if strLine == "<html>":
			break
		strID, strSource = strLine.strip( ).split( "\t" )
		if strSource == strTarget:
			return strID

	return strIn

#===============================================================================
# CProcessor
#===============================================================================

class CProcessor:

	def __init__( self, strFrom, strTo, strID, strProcessor,
		astrArgs = [], strDir = None, fPipe = True ):

		self.m_strDir = strDir
		self.m_strFrom = strFrom
		self.m_strTo = strTo
		self.m_strID = strID
		self.m_strProcessor = strProcessor
		self.m_astrArgs = astrArgs
		self.m_fPipe = fPipe

	def in2out( self, strIn, strDir = c_strDirData, strSuffix = None ):

		if not strSuffix:
			mtch = re.search( '(\.[^.]+)$', strIn )
			strSuffix = mtch.group( 1 ) if mtch else ""
		if self.m_strDir:
			strIn = re.sub( '^.*' + self.m_strDir + '/', strDir + "/", strIn )
		return re.sub( ( self.m_strFrom + '()$' ) if self.m_strDir else
			( '_' + self.m_strFrom + '(-.*)' + strSuffix + '$' ),
			"_" + self.m_strTo + "\\1-" + self.m_strID + strSuffix, strIn )

	def out2in( self, strOut ):

		if self.m_strDir:
			strOut = re.sub( '^.*/', self.m_strDir + "/", re.sub(
				'\.[^.]+$', pSelf.m_strFrom, strOut ) )
		return re.sub( '_' + pSelf.m_strTo + '(.*)-' + pSelf.m_strID,
			( "_" + pSelf.m_strFrom + "\\1" ) if pSelf.m_strFrom else "",
			strOut )

	def ex( self, pE, strIn, strDir = c_strDirData, strSuffix = None ):
		
		strOut = self.in2out( strIn, strDir, strSuffix )
		if not strOut:
			return None
		return ( pipe( pE, strIn, self.m_strProcessor, strOut, self.m_astrArgs ) if self.m_fPipe else
			cmd( pE, self.m_strProcessor, strOut, [[True, strIn]] + self.m_astrArgs ) )

#------------------------------------------------------------------------------ 

if __name__ == "__main__":
	pass
