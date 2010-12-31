#!/usr/bin/env python

import glob
import os
import re
import subprocess
import sys
import threading
import urllib

c_strDirData	= "data/"
c_strDirDoc		= "doc/"
c_strDirEtc		= "etc/"
c_strDirSrc		= "src/"
c_strDirTmp		= "tmp/"
c_astrExclude	= [strCur[:-1] for strCur in (c_strDirEtc, c_strDirSrc, c_strDirTmp, c_strDirDoc)] + [
#	"ArrayExpress",
#	"GEO",
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
		if any( ( i != None ) for i in aiCols ):
			if len( astrLine ) > max( aiCols ):
				aastrRet.append( [( None if ( i == None ) else astrLine[i] ) for i in aiCols] )
			continue
		if len( astrLine ) < len( afuncCols ):
			continue
		for i in range( len( astrLine ) ):
			for j in range( len( afuncCols ) ):
				if ( aiCols[j] == None ) and afuncCols[j]( astrLine[i] ):
					aiCols[j] = i
					break
	return aastrRet

def readcomment( fileIn ):
	
	if not isinstance( fileIn, file ):
		try:
			fileIn = open( str(fileIn) )
		except IOError:
			return []
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

def override( pE, pFile ):

# This is so not kosher, but I can't find any other way to allow multiple rules for
# the same target or over types of overrides.  The SCons interface allows _adding_
# children, but not removing or resetting them except directly like this
# (_children_reset doesn't actually remove the list of children!)
	pFile = pE.File( pFile )
	pFile._children_reset( )
	pFile.sources = []
	pFile.depends = []
	pFile.implicit = []
	pFile.sources_set = set()
	pFile.depends_set = set()
	pFile.implicit_set = set()
	pFile.env = None

#===============================================================================
# Command execution
#===============================================================================

def download( pE, strURL, strT = None, fSSL = False, fGlob = True ):

	if not strT:
		strT = re.sub( '^.*\/', "", strURL )

	def funcDownload( target, source, env, strURL = strURL ):
		strT, astrSs = ts( target, source )
		iRet = ex( " ".join( ("curl", "--ftp-ssl -k" if fSSL else "",
			"" if fGlob else "-g", "-f", "-z", strT, "'" + strURL + "'") ), strT )
# 19 is curl's document-not-found code
		return ( iRet if ( iRet != 19 ) else 0 )
	return pE.Command( strT, None, funcDownload )

def _pipefile( pFile ):
	
	return ( ( pFile.get_abspath( ) if ( "get_abspath" in dir( pFile ) ) else str(pFile) )
		if pFile else None )

def _pipeargs( strFrom, strTo, aaArgs ):

	astrFiles = []
	astrArgs = []
	for aArg in aaArgs:
		fFile, strArg = aArg[0], aArg[1]
		if fFile:
			strArg = _pipefile( strArg )
			astrFiles.append( strArg )
			strArg = "\"" + strArg + "\""
		astrArgs.append( str(strArg) )
	return ( [_pipefile( s ) for s in (strFrom, strTo)] + [astrFiles, astrArgs] )

def pipe( pE, strFrom, strProg, strTo, aaArgs = [] ):
	strFrom, strTo, astrFiles, astrArgs = _pipeargs( strFrom, strTo, aaArgs )
	def funcPipe( target, source, env, strFrom = strFrom, astrArgs = astrArgs ):
		strT, astrSs = ts( target, source )
		return ex( " ".join( [astrSs[0]] + astrArgs +
			( ["<", str(strFrom)] if strFrom else [] ) ), strT )
	return pE.Command( strTo, [strProg] + ( [strFrom] if strFrom else [] ) +
		astrFiles, funcPipe )

def cmd( pE, strProg, strTo, aaArgs = [] ):

	return pipe( pE, None, strProg, strTo, aaArgs )

def spipe( pE, strFrom, strCmd, strTo, aaArgs = [] ):
	strFrom, strTo, astrFiles, astrArgs = _pipeargs( strFrom, strTo, aaArgs )
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

def cwd( ):

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

def level( ):

	strPath = path_repo( )
	strPath = os.getcwd( )[len( strPath ):]
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

def scons_child( pE, fileDir, hashArgs = None, fileSConstruct = None, afileDeps = None ):

	def funcTmp( target, source, env, fileDir = fileDir, fileSConstruct = fileSConstruct ):
		strDir, strSConstruct = (( ( os.path.abspath( f ) if ( type( f ) == str ) else f.get_abspath( ) ) if f else None )
			for f in (fileDir, fileSConstruct))
		if os.path.commonprefix( (pE.GetLaunchDir( ), strDir) ) not in [strDir, pE.GetLaunchDir( )]:
			return
		if fileSConstruct:
			try:
				os.makedirs( strDir )
			except os.error:
				pass
			subprocess.call( ["ln", "-f", "-s", strSConstruct, d( strDir, "SConstruct" )] )
		if hashArgs:
			with open( d( strDir, "SConscript" ), "w" ) as fileOut:
				fileOut.write( "hashArgs = {\n" )
				for strKey, strValue in hashArgs.items( ):
					fileOut.write( "	\"%s\"	: %s,\n" % (strKey, repr( strValue )) )
				fileOut.write( "}\nExport( \"hashArgs\" )\n" )
		return subprocess.call( ["scons"] + sys.argv[1:] + ["-C", strDir] )
	return pE.Command( "dummy:" + os.path.basename( str(fileDir) ), afileDeps, funcTmp )

def scons_children( pE ):

	afileRet = []
	for fileCur in pE.Glob( "*" ):
		if ( type( fileCur ) == type( pE.Dir( "." ) ) ) and \
			( os.path.basename( str(fileCur) ) not in c_astrExclude ):
			afileRet.extend( scons_child( pE, fileCur ) )
	return afileRet

#------------------------------------------------------------------------------ 
# Helper functions for SConscript subdirectories auto-generated from a scanned
# input file during the build process.  Extremely complex; intended usage is:
#
# def funcScanner( target, source, env ):
# 	for strLine in open( str(source[0]) ):
# 		if strLine.startswith( ">" ):
# 			env["sconscript_child"]( target, source[0], env, strLine[1:].strip( ) )
# arepa.sconscript_children( pE, afileIntactC, funcScanner, 1 )
#
# Based on documentation at:
# http://www.scons.org/wiki/DynamicSourceGenerator
#------------------------------------------------------------------------------ 

def sconscript_child( target, source, env, strID, hashArgs = None, afileDeps = None, iLevel = 1, strDir = "." ):

	fileTarget = target[0] if ( type( target ) == list ) else target
	strDir = strDir if ( type( strDir ) == str ) else strDir.get_abspath( )
	strDir = d( strDir, c_strDirData if ( iLevel == 1 ) else "", strID )
	return scons_child( env, strDir, hashArgs, d( path_arepa( ), c_strDirSrc, "SConstruct.py" ), afileDeps )

def sconscript_children( pE, afileSources, funcScanner, iLevel, funcAction = None ):
	
	if not getattr( afileSources, "__iter__", False ):
		afileSources = [afileSources]
	def funcTmp( target, source, env, strID, hashArgs = None, afileDeps = None, iLevel = iLevel, strDir = pE.Dir( "." ) ):
		return sconscript_child( target, source, env, strID, hashArgs, afileDeps, iLevel, strDir )
	if not funcAction:
		funcAction = funcTmp
	
	strID = ":".join( ["dummy", str(iLevel)] + [os.path.basename( str(f) ) for f in afileSources] )
	pBuilder = pE.Builder( action = funcScanner )
	pE.Append( BUILDERS = {strID : pBuilder} )
	afileSubdirs = getattr( pE, strID )( strID, afileSources, sconscript_child = funcAction )
	pE.AlwaysBuild( afileSubdirs )
	return afileSubdirs

#===============================================================================
# Gene ID conversion
#===============================================================================

s_lockTaxdump	= threading.Lock( )
s_hashTaxID2Org	= None
s_hashOrg2TaxID	= None
def _taxdump( ):
	global	s_lockTaxdump, s_hashTaxID2Org, s_hashOrg2TaxID

	s_lockTaxdump.acquire( )
	if ( s_hashTaxID2Org == None ) or ( s_hashOrg2TaxID == None ):
		s_hashTaxID2Org = {}
		s_hashOrg2TaxID = {}
		strTaxIDs = d( path_arepa( ), c_strDirTmp, "taxdump.txt" )
		try:
			for strLine in open( strTaxIDs ):
				strOrg, strID = strLine.strip( ).split( "\t" )
				s_hashTaxID2Org[strID] = strOrg
				s_hashOrg2TaxID[strOrg] = strID
		except IOError:
			pass
	s_lockTaxdump.release( )
	
	return (s_hashTaxID2Org, s_hashOrg2TaxID)

def taxid2org( strTaxID ):

	hashTaxID2Org, hashOrg2TaxID = _taxdump( )
	return hashTaxID2Org.get( strTaxID )

def org2taxid( strOrg ):

	hashTaxID2Org, hashOrg2TaxID = _taxdump( )
	return hashOrg2TaxID.get( strOrg )

def geneid( strIn, strTaxID, strTarget = "Entrez Gene", strURLBase = "http://localhost:8183" ):
	
# BUGBUG: Currently disabled due to BridgeDB's inadequate coverage and performance
# It's way-crazy slow, and it doesn't have sufficient DB coverage when it does work
	return None
# BUGBUG: This is one of the worst things I've ever done
	strTaxon = taxid2org( strTaxID )
	if not strTaxon:
		return None
	strTaxon = " ".join( strTaxon.split( " " )[:2] )
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
		return None
	strSource = urllib.quote( strSource ).replace( "/", "%2F" )

	strURL = strURLBase + "/" + strTaxon + "/xrefs/" + strSource + "/" + urllib.quote( strID )
	astrData = urllib.urlopen( strURL ).read( ).splitlines( )
	for strLine in astrData:
		if strLine == "<html>":
			break
		strID, strSource = strLine.strip( ).split( "\t" )
		if strSource == strTarget:
			return strID
	return None

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
