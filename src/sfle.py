#######################################################################################
# This file is provided under the Creative Commons Attribution 3.0 license.
#
# You are free to share, copy, distribute, transmit, or adapt this work
# PROVIDED THAT you attribute the work to the authors listed below.
# For more information, please see the following web page:
# http://creativecommons.org/licenses/by/3.0/
#
# This file is a component of the SflE Scientific workFLow Environment for reproducible 
# research, authored by the Huttenhower lab at the Harvard School of Public Health
# (contact Curtis Huttenhower, chuttenh@hsph.harvard.edu).
#
# If you use this environment, the included scripts, or any related code in your work,
# please let us know, sign up for the SflE user's group (sfle-users@googlegroups.com),
# pass along any issues or feedback, and we'll let you know as soon as a formal citation
# is available.
#######################################################################################
#!/usr/bin/env python

"""
.. testsetup::

	from sfle import *
"""

import collections
import csv
import fnmatch
import ftplib
import glob
import inspect
import logging
import os
import re
import subprocess
import sys
import threading
import urllib

c_strDirData			= "data/"
c_strDirDoc				= "doc/"
c_strDirEtc				= "etc/"
c_strDirSrc				= "src/"
c_strDirTmp				= "tmp/"

c_strSufBZ2				= ".bz2"
c_strSufFASTA			= ".fasta"
c_strSufGZ				= ".gz"
c_strSufHTML			= ".html"
c_strSufPCL				= ".pcl"
c_strSufPDF				= ".pdf"
c_strSufPY				= ".py"
c_strSufR				= ".R"
c_strSufRData			= ".RData"
c_strSufRST				= ".rst"
c_strSufTAR				= ".tar"
c_strSufTSV				= ".tsv"
c_strSufTXT				= ".txt"
c_strSufXML				= ".xml"

c_strProgInlinedocsR	= "#" + c_strDirSrc + "inlinedocs.R"
c_strProgTestthatR		= "#" + c_strDirSrc + "testthat.R"

c_logrSflE				= logging.getLogger( "sfle" )
lghn = logging.StreamHandler( sys.stderr )
lghn.setFormatter( logging.Formatter( '%(asctime)s %(levelname)10s %(module)s.%(funcName)s@%(lineno)d %(message)s' ) )
c_logrSflE.addHandler( lghn )
#c_logrSflE.setLevel( logging.DEBUG )

#===============================================================================
# Basic global utilities
#===============================================================================

def regs( strRE, strString, aiGroups ):

	if not iscollection( aiGroups ):
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
	for astrLine in csv.reader( fileIn, csv.excel_tab ):
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

def lc( strFile ):

	return sum( 1 for s in open( strFile ) )
""" # The following is faster, but not platform friendly
	strWC = check_output( "wc -l " + strFile )
	if strWC:
		strWC = strWC.strip( ).split( )[0]
		try:
			strWC = int(strWC)
		except ValueError:
			strWC = None
	return strWC
"""

def d( *aArgs ):
	"""
	Convenience function for joining two or more components of a path with /s.  Will
	automatically convert objects into strings before joining.  If any argument is an
	SCons environment, the return value will be a File or Dir object as appropriate.
	
	:param	aArgs:	Two or more items to be joined.
	:type	aArgs:	collection
	:returns:		string or File/Dir -- inputs joined by / characters
	
	>>> d( "a", "b", "c" )
	'a/b/c'
	
	Automatic string conversion is most useful for file objects, but will work for
	any element:
	
	>>> d( "r", 2, "d", 2 )
	'r/2/d/2'
	"""

	astrArgs = []
	pE = None
	for pArg in aArgs:
		if ( "File" in dir( pArg ) ) and ( str(type( pArg )).find( "Node" ) < 0 ):
			pE = pArg
		else:
			astrArgs.append( str(pArg) )
	strRet = apply( os.path.join, [str(p) for p in astrArgs] )
	if not pE:
		return strRet
	try:
		return pE.File( strRet )
	except TypeError:
		return pE.Dir( strRet )

def find( pPath, pFile, pE = None ):
	
	strTarget = str(pFile)
	for strPath, strDir, astrFiles in os.walk( str(pPath) ):
		for strFile in astrFiles:
			if fnmatch.fnmatch( strFile, strTarget ):
				return ( d( pE, strPath, strFile ) if pE else d( strPath, strFile ) )
	
	return None

def rebase( pPath, strFrom = None, strTo = "" ):
	"""
	Convenience function for extracting the base name of a file path, and optionally
	removing or replacing its type extension.
	
	:param	pPath:		Path from which base name is extracted.
	:param	strFrom:	File extension to be removed if present.
	:type	strFrom:	string
	:param	strTo:		File extension to be optionally re-added.
	:type	strTo:		string
	:returns:			string -- path basename with optional extension replacement
	
	>>> rebase( "a/b/c.dee" )
	'c.dee'
	
	>>> rebase( "a/b/c.dee", ".dee" )
	'c'
	
	>>> rebase( "a/b/c.dee", ".dee", ".eff" )
	'c.eff'
	
	Automatic string conversion is most useful for file objects, but will work for
	any element:
	
	>>> rebase( 1, "", ".two" )
	'1.two'
	"""
	
	strRet = os.path.basename( str(pPath) )
	if strFrom:
		if strFrom == True:
			strRet = re.sub( r'\.[^.]*$', "", strRet )
		else:
			strRet = strRet.replace( strFrom, "" )
	if strTo:
		strRet += strTo
	return strRet

def redir( pPath ):
	
	return os.path.dirname( str(pPath) )

def iscollection( pValue ):
	
	return ( ( type(pValue) != str ) and isinstance( pValue, collections.Iterable ) )

def current_file( ):
	
	frme = inspect.currentframe( )
	if frme:
		frme = frme.f_back
	return ( frme and os.path.abspath( inspect.getfile( frme ) ) )

def isempty( strFile ):
	
	return ( not os.stat( strFile )[6] )

#===============================================================================
# SCons utilities
#===============================================================================

def ex( pCmd, strOut = None, strErr = None ):
	
	strCmd = pCmd if isinstance( pCmd, str ) else " ".join( str(p) for p in pCmd )
	sys.stdout.write( "%s" % strCmd )
	sys.stdout.write( ( ( " > %s" % quote( strOut ) ) if strOut else "" ) )
	sys.stdout.write( ( ( " 2> %s" % quote( strErr ) ) if strErr else "" ) + "\n" )
	if not ( strOut or strErr ):
		return subprocess.call( strCmd, shell = True )
	pProc = subprocess.Popen( strCmd, shell = True,
		stdout = ( subprocess.PIPE if strOut else None ),
		stderr = ( open( strErr, "w" ) if strErr else None ) )
	if not pProc:
		return 1
	if strOut:
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

	return (afileTargets[0].get_abspath( ), [f.get_abspath( ) for f in afileSources])

def tss( afileTargets, afileSources ):

	return ([f.get_abspath( ) for f in a] for a in (afileTargets, afileSources))

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

def download( pE, strURL, strT = None, fSSL = False, fGlob = True, fImmediate = False ):

	if not strT:
		strT = re.sub( r'^.*\/', "", strURL )

	def funcDownload( target, source, env, strURL = strURL ):
		strT, astrSs = ts( target, source )
		iRet = ex( " ".join( ("curl", "--ftp-ssl -k" if fSSL else "",
			"" if fGlob else "-g", "-f", "-z", strT, "'" + strURL + "'") ), strT )
# 19 is curl's document-not-found code
		return ( iRet if ( iRet != 19 ) else 0 )
	afileRet = ( funcDownload( [strT], [], pE ) if fImmediate else
		pE.Command( strT, None, funcDownload ) )
	pE.NoClean( afileRet )
	return afileRet

def ftpls( strHost, strPath ):

	ftp = ftplib.FTP( strHost )
	ftp.login( "anonymous" )
	ftp.cwd( strPath )
	astrRet = []
	ftp.retrlines( "NLST", astrRet.append )
	return astrRet

def _pipefile( pFile ):
	
	return ( ( pFile.get_abspath( ) if ( "get_abspath" in dir( pFile ) ) else str(pFile) )
		if pFile else None )

def quote( p ):

	return ( "\"" + str(p) + "\"" )

def cat( strFrom ):
	
	return " ".join( (( "gunzip -c" if re.search( r'\.gz$', strFrom ) else "cat" ), quote( strFrom )) )

def _pipeargs( strFrom, strTo, aArgs, strErr ):

	astrIns, astrOuts, astrArgs = ([] for i in range( 3 ))
	if strFrom:
		astrIns.append( strFrom )
	if strTo:
		astrOuts.append( strTo )
	for pArg in aArgs:
		if iscollection( pArg ):
			if len( pArg ) < 2:
				pArg = [False] + pArg
			fOut, pArg = pArg[0], _pipefile( pArg[1] )
			( astrOuts if fOut else astrIns ).append( pArg )
		astrArgs.append( quote( pArg ) )
	if strErr:
		astrOuts.append( strErr )
	return ( [_pipefile( s ) for s in (strFrom, strTo, strErr)] + [astrIns, astrOuts, astrArgs] )

def pipe( pE, strFrom, strProg, strTo, aArgs = [], strErr = None ):
	
	strFrom, strTo, strErr, astrIns, astrOuts, astrArgs = _pipeargs( strFrom, strTo, aArgs, strErr )
	def funcPipe( target, source, env, strTo = strTo, strFrom = strFrom, astrArgs = astrArgs, strErr = strErr ):
		astrTs, astrSs = tss( target, source )
		return ex( ( [cat( strFrom ), "|"] if strFrom else [] ) + [astrSs[0]] + astrArgs, strTo, strErr )
	return pE.Command( astrOuts, [strProg] + astrIns, funcPipe )

def cmd( pE, strProg, strTo, aArgs = [], strErr = None ):

	return pipe( pE, None, strProg, strTo, aArgs, strErr )

def sink( pE, strFrom, strProg, aArgs = [], strErr = None ):

	return pipe( pE, strFrom, strProg, None, aArgs, strErr )

def op( pE, strProg, aArgs = [], strErr = None ):

	return pipe( pE, None, strProg, None, aArgs, strErr )

def spipe( pE, strFrom, strCmd, strTo, aArgs = [], strErr = None ):
	
	strFrom, strTo, strErr, astrIns, astrOuts, astrArgs = _pipeargs( strFrom, strTo, aArgs, strErr )
	def funcPipe( target, source, env, strCmd = strCmd, strTo = strTo, strFrom = strFrom, astrArgs = astrArgs, strErr = strErr ):
		return ex( ( [cat( strFrom ), "|"] if strFrom else [] ) + [strCmd] + astrArgs, strTo, strErr )
	return pE.Command( astrOuts, astrIns, funcPipe )

def scmd( pE, strCmd, strTo, aArgs = [], strErr = None ):

	return spipe( pE, None, strCmd, strTo, aArgs, strErr )

def ssink( pE, strFrom, strCmd, aArgs = [], strErr = None ):

	return spipe( pE, strFrom, strCmd, None, aArgs, strErr )

def sop( pE, strCmd, aArgs = [], strErr = None ):

	return spipe( pE, None, strCmd, None, aArgs, strErr )

#===============================================================================
# Sphinx reporting utilities
#===============================================================================

def _sphinx( fDoctest = False ):
	def funcRet( target, source, env, fDoctest = fDoctest ):
		strT, astrSs = ts( target, source )
		strRST, strPY = astrSs[:2]
		return ex( ("sphinx-build -W", "-b doctest" if fDoctest else "",
			"-c", os.path.dirname( strPY ), os.path.dirname( strRST ), os.path.dirname( strT )) )
	return funcRet

def sphinx( pE, fileIndexRST, fileConfPY, fileDirOutput, afilePYs = None, afileRSTs = None ):
	# Sphinx automatically names this file output.txt, for reasons that are inscrutable to me
	fileSphinxTXT = d( pE, fileDirOutput, "output.txt" )
	fileIndexHTML = d( pE, fileDirOutput, rebase( fileIndexRST, c_strSufRST, c_strSufHTML ) )
	afileRet = []
	for fileOut, fDoctest in ((fileIndexHTML, False), (fileSphinxTXT, True)):
		afileRet = pE.Command( fileOut, [fileIndexRST, fileConfPY] +
			( afileRSTs or [] ) + ( afilePYs or [] ), _sphinx( fDoctest ) ) + afileRet
		if ( len( afileRet ) > 1 ):
			pE.Requires( afileRet[0], afileRet[1] )
	return afileRet

def _sphinx_conf( pE, strConfPY ):
	
	def funcConfPY( target, source, env ):
		strT, astrSs = ts( target, source )
		with open( strT, "w" ) as ostm:
			ostm.write( "master_doc = 'index'\n" )
		return None
	return pE.Command( strConfPY, None, funcConfPY )

def report( pE, strFrom, strProg, strTo, aArgs = [] ):
	
	strRST = str(strTo).replace( c_strSufHTML, c_strSufRST )
	pipe( pE, strFrom, strProg, strRST, aArgs )
	strConfPY = d( os.path.dirname( strRST ), "conf.py" )
	_sphinx_conf( pE, strConfPY )
	return pE.Command( strTo, [strRST, strConfPY], _sphinx( ) )

def rst_text( strText, ostm ):
	
	ostm.write( "%s\n\n" % strText )
	return True

def _rst_section( strTitle, ostm, strChar ):

	return rst_text( "%s\n%s" % (strTitle, strChar * len(strTitle)), ostm )

def rst_section( strTitle, ostm ):
	
	return _rst_section( strTitle, ostm, "=" )

def rst_subsection( strTitle, ostm ):
	
	return _rst_section( strTitle, ostm, "-" )

def rst_subsubsection( strTitle, ostm ):
	
	return _rst_section( strTitle, ostm, "~" )

def rst_table( aaTable, ostm, fHeader = True ):

	if not ( aaTable and aaTable[0] ):
		return False
	
	iWidth = max( (max( (len( str(p) ) for p in a) ) for a in aaTable) )
	astrHeader = ["=" * iWidth] * len( aaTable[0] )
	aaOutput = [astrHeader] + [a for a in aaTable] + [astrHeader]
	if fHeader:
		aaOutput.insert( 2, astrHeader )
	for aOutput in aaOutput:
		astrOutput = [str(p) for p in aOutput]
		for i in range( len( astrOutput ) ):
			if len(astrOutput[i]) < iWidth:
				astrOutput[i] += " " * ( iWidth - len(astrOutput[i]) )
		ostm.write( "%s\n" % "  ".join( astrOutput ) )
	ostm.write( "\n" )
	return True

#===============================================================================
# R inlinedocs utilities
#===============================================================================

def inlinedocs( pE, fileIn, fileOut, fileDirTmp = None ):

	# Default to the same intermediate directory as the output file.	
	if not fileDirTmp:
		fileDirTmp = os.path.dirname( str(fileOut) )
	# But the inlinedocs intermediate output is actually a whole nested directory.
	fileDirTmp = pE.Dir( d( fileDirTmp, os.path.basename( str(fileIn) ) ) )
	
	def funcID( target, source, env ):
		strT, astrSs = ts( target, source )
		strProg, strIn = astrSs[:2]
		return ex( (cat( strIn ), "|", strProg, os.path.dirname( strT )) )
	# Use the guaranteed DESCRIPTION file as a marker for the entire
	# inlinedocs generated directory.
	fileDesc = d( fileDirTmp, "DESCRIPTION" )
	pE.Command( fileDesc, [c_strProgInlinedocsR, fileIn], funcID )
	
	def funcPDF( target, source, env ):
		strT, astrSs = ts( target, source )
		# We want every file from the "man" subdirectory of the intermediate package.
		strDir = d( os.path.dirname( astrSs[0] ), "man" )
		# --force overwrites output PDF if present.
		# --no-preview prevents the output PDF from being automatically opened.
		# I honestly don't know what --batch does.
		# *.Rd is a bit clunky, but we have no way to know beforehand what files
		# will actually be generated during the R documentation process.
		return ex( ("R CMD Rd2pdf --batch --force --no-preview %s/*.Rd" % strDir, "-o", strT) )
	return pE.Command( fileOut, fileDesc, funcPDF )

#===============================================================================
# Python doctest and R testthat utilities
#===============================================================================

def doctest( pE, afileProgs, fileOut ):
	
	if not iscollection( afileProgs ):
		afileProgs = (afileProgs,)
	return scmd( pE, "python -m doctest -v", fileOut, [[False, f] for f in afileProgs] )

def testthat( pE, fileProg, fileDir, fileOut ):
	"""
	Uses the ``testthat`` R library to run unit tests on an R script.  Executes
	all test files from the requested directory and deposits a report in the
	given output file.
	
	.. warning::
	
		Test script file names in ``fileDir`` *must* begin with the string "test-"
		in order to be executed.
	
	:param	pE:			SCons environment in which rules are created
	:type	pE:			Environment
	:param	fileProg:	Input R script to be tested
	:type	fileProg:	File
	:param	fileDir:	Input directory of R script unit tests
	:type	fileDir:	Dir
	:param	fileOut:	Output text file containing test report
	:type	fileOut:	File
	:returns:			File list -- Output report file
	
	.. note::
	
		``Glob`` is used to assign all R files in the requested directory as
		dependencies for the output file.
	
	>>> testthat( DefaultEnvironment( ), "testme.R", "src/test_testme", "testreport.txt" ) #doctest: +SKIP
	[<File testreport.txt>]
	"""
	
	def funcTT( target, source, env, fileDir = fileDir ):
		strT, astrSs = ts( target, source )
		strProg, strIn = astrSs[:2]
		return ex( (strProg, strIn, fileDir), strT )
	return pE.Command( fileOut, [c_strProgTestthatR, fileProg] +
		pE.Glob( d( fileDir, "*" + c_strSufR ) ), funcTT )

#===============================================================================
# SConstruct helper functions
#===============================================================================

def scons_child( pE, fileDir, hashArgs = None, fileSConstruct = None, afileDeps = None, afileOuts = None ):

	def funcTmp( target, source, env, fileDir = fileDir, fileSConstruct = fileSConstruct ):
		strDir, strSConstruct = (( ( os.path.abspath( f ) if ( type( f ) == str ) else f.get_abspath( ) ) if f else None )
			for f in (fileDir, fileSConstruct))
		#if os.path.commonprefix( (pE.GetLaunchDir( ), strDir) ) not in [strDir, pE.GetLaunchDir( )]:
		#	return
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
	return pE.Command( ["dummy:" + os.path.basename( str(fileDir) )] + ( afileOuts or [] ),
		afileDeps, funcTmp )

def scons_children( pE, strDir = ".", afileDeps = None, astrExclude = [] ):

	afileRet = []
	for fileCur in pE.Glob( d( strDir, "*" ) ):
		if ( type( fileCur ) == type( pE.Dir( "." ) ) ) and \
			( os.path.basename( str(fileCur) ) not in astrExclude ) and \
			os.path.exists( d( str(fileCur), "SConstruct" ) ):
			afileRet += scons_child( pE, fileCur, None, None, afileDeps )
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

def sconscript_child( target, source, env, strID, fileSConstruct,
	hashArgs = None, afileDeps = None, iLevel = 1, strDir = "." ):

	fileTarget = target[0] if ( type( target ) == list ) else target
	strDir = strDir if ( type( strDir ) == str ) else strDir.get_abspath( )
	strDir = d( strDir, c_strDirData if ( iLevel == 1 ) else "", strID )
	return scons_child( env, strDir, hashArgs, fileSConstruct, afileDeps )

def sconscript_children( pE, afileSources, funcScanner, iLevel, fileSConstruct, hashArgs = None, funcAction = None ):
	
	if not iscollection( afileSources ):
		afileSources = [afileSources]
	def funcTmp( target, source, env, strID, hashArgs = hashArgs, afileDeps = None, iLevel = iLevel, strDir = pE.Dir( "." ) ):
		return sconscript_child( target, source, env, strID, fileSConstruct, hashArgs, afileDeps, iLevel, strDir )
	if not funcAction:
		funcAction = funcTmp
	
	strID = ":".join( ["dummy", str(iLevel)] + [os.path.basename( str(f) ) for f in afileSources] )
	pBuilder = pE.Builder( action = funcScanner )
	pE.Append( BUILDERS = {strID : pBuilder} )
	afileSubdirs = getattr( pE, strID )( strID, afileSources, sconscript_child = funcAction )
	pE.AlwaysBuild( afileSubdirs )
	return afileSubdirs

def scanner( fileExclude = None, fileInclude = None ):

	setstrExclude = set(readcomment( fileExclude ) if fileExclude else [])
	setstrInclude = set(readcomment( fileInclude ) if fileInclude else [])
	def funcRet( target, source, env, setstrInclude = setstrInclude, setstrExclude = setstrExclude ):
		strT, astrSs = ts( target, source )
		for strS in astrSs:
			for astrLine in csv.reader( open( strS ), csv.excel_tab ):
				if not ( astrLine and astrLine[0] ):
					continue
				strID = astrLine[0]
				if ( setstrInclude and ( strID not in setstrInclude ) ) or ( strID in setstrExclude ):
					continue
				env["sconscript_child"]( target, source[0], env, strID )
	return funcRet

#===============================================================================
# CProcessor
#===============================================================================

class CCommand:
	
	def __init__( self, strCommand, aArgs = [], fPipe = True, fStatic = False ):
		
		self.m_strCommand = strCommand
		self.m_aArgs = aArgs or []
		self.m_fPipe = fPipe
		self.m_fStatic = fStatic

	def ex( self, pE, fileIn, fileOut ):
		
		if self.m_fPipe:
			funcPipe = spipe if self.m_fStatic else pipe
			return funcPipe( pE, fileIn, self.m_strCommand, fileOut, self.m_aArgs )
		funcCmd = scmd if self.m_fStatic else cmd
		return funcCmd( pE, self.m_strCommand, fileOut, [[False, fileIn]] + self.m_aArgs )

class CTarget:
	
	def __init__( self, strSuffix = None, fileDir = None, strTag = None ):
		
		self.m_strTag = strTag
		self.m_strSuffix = strSuffix
		self.m_fileDir = fileDir
		
	def in2out( self, fileIn, pTo, strName = None ):
		"""
		>>> pFrom = CTarget( None, "input" )
		>>> pTo = CTarget( None, "output" )
		>>> pFrom.in2out( "input/data.txt", pTo )
		'output/data.txt'

		>>> pFrom = CTarget( ".pcl" )
		>>> pTo = CTarget( ".tsv" )
		>>> pFrom.in2out( "tmp/data.pcl", pTo )
		'tmp/data.tsv'
		
		>>> pFrom.in2out( "tmp/data.tsv", pTo )
		
		>>> pFrom = CTarget( )
		>>> pTo = CTarget( None, None, "01" )
		>>> pFrom.in2out( "tmp/data.txt", pTo, "test" )
		'tmp/data_01-test.txt'
		
		>>> pFrom = CTarget( None, None, "00" )
		>>> pFrom.in2out( "tmp/data.txt", pTo, "test" )

		>>> pFrom.in2out( "tmp/data_00.txt", pTo )
		'tmp/data_01.txt'
		"""

		strRet = str(fileIn)
		strBase = os.path.basename( strRet )
		c_logrSflE.debug( "Initial ret/base: %s" % [strRet, strBase] )

		if self.m_strSuffix:
			if not strBase.endswith( self.m_strSuffix ):
				return None
			strBase = strBase[:-len( self.m_strSuffix )]
		if self.m_strTag:
			mtch = re.search( r'^(.*)_(' + re.escape( self.m_strTag ) + r')(-.*)?(\.\S+)?$', strBase )
			if not mtch:
				return None
			strBase = mtch.group( 1 ) + mtch.group( 4 )
		c_logrSflE.debug( "Stripped ret/base: %s" % [strRet, strBase] )

		strRet = d( pTo.m_fileDir or os.path.dirname( strRet ), strBase )
		strSuffix = pTo.m_strSuffix
		if not self.m_strSuffix:
			mtch = re.search( r'(\.\S+)$', strRet )
			if mtch:
				strSuffix = strSuffix or mtch.group( 1 )
				strRet = strRet[:-len( mtch.group( 1 ) )]
		c_logrSflE.debug( "Suffixed ret/suf: %s" % [strRet, strSuffix] )
		if pTo.m_strTag or strName:
			strRet += "_"
			if pTo.m_strTag:
				strRet += pTo.m_strTag
				if strName:
					strRet += "-"
			if strName:
				strRet += strName
		if strSuffix:
			strRet += strSuffix
		c_logrSflE.debug( "Returning: %s" % strRet )
		return strRet

class CProcessor:

	@staticmethod
	def pipeline( pE, apPipeline, afileIn ):

		afileIn = afileIn or []
		apPipeline, afileIn = (( p if iscollection( p ) else (p,) ) for p in (apPipeline, afileIn))
		for apProc in apPipeline:
			if not iscollection( apProc ):
				apProc = (apProc,)
			afileOut = []
			for pProc in apProc:
				for fileIn in afileIn:
					afileOut += pProc.ex( pE, fileIn ) or []
			afileIn = afileOut
		return afileIn

	def __init__( self, strID, pFrom, pCommand, pTo = None ):

		self.m_strID = strID
		self.m_pFrom = pFrom or CTarget( )
		self.m_pCommand = pCommand
		self.m_pTo = pTo or CTarget( )

	def in2out( self, fileIn ):
		
		return self.m_pFrom.in2out( fileIn, self.m_pTo, self.m_strID )

	"""
	def out2in( self, strOut ):

		if self.m_strDir:
			strOut = re.sub( '^.*/', self.m_strDir + "/", re.sub(
				'\.[^.]+$', pSelf.m_strFrom, strOut ) )
		return re.sub( '_' + pSelf.m_strTo + '(.*)-' + pSelf.m_strID,
			( "_" + pSelf.m_strFrom + "\\1" ) if pSelf.m_strFrom else "",
			strOut )
	"""

	def ex( self, pE, fileIn ):
		
		fileOut = self.in2out( fileIn )
		return ( self.m_pCommand.ex( pE, fileIn, fileOut ) if fileOut else None )

#------------------------------------------------------------------------------ 

if __name__ == "__main__":
	pass
