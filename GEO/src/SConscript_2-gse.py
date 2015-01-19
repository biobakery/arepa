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
import csv
import os 
import gzip
import metadata 
import re 

def test( iLevel, strID, hashArgs ):
	return ( iLevel == 2 ) and ( strID.find( "GSE" ) == 0 ) 
if "testing" in locals( ):
	sys.exit( )

pE = DefaultEnvironment( )

c_strID               	= arepa.cwd( )
c_strSufRPackage      	= "_rpackage" 
c_fileGPL             	= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirTmp, "gpl.txt" ) 
c_fileAnnot           	= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirTmp, "annot.txt" ) 
c_fileInputSConscript 	= sfle.d( pE, arepa.path_arepa( ), sfle.c_strDirSrc, "SConscript_pcl-dab.py" ) 
c_fileRSConscript		= sfle.d( pE, arepa.path_arepa( ), sfle.c_strDirSrc, "SConscript_rpackage.py" )
c_fileProgUnpickle    	= sfle.d( pE, arepa.path_arepa( ), sfle.c_strDirSrc, "unpickle.py" ) 
c_fileInputGSER       	= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "gse.R" ) 
c_fileInputManCurTXT  	= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirEtc, "manual_curation/", 
							c_strID + ".txt" )

c_filePPfun         	= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirEtc, "preprocess")
c_fileRunRaw        	= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirEtc,  "raw")

c_fileIDPKL    			= sfle.d( pE, c_strID + ".pkl" )
c_strURLGPL    			= hashArgs["c_strURLGPL"]
c_strHost      			= "ftp.ncbi.nih.gov"
c_strPath      			= "pub/geo/DATA/annotation/platforms/"
c_strGPLPath			= r"http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?view=data&acc="

c_strDirR				= "R"
c_dirR					= sfle.d( c_strDirR )
c_strDirRman			= "man"
c_strDirRdata			= "data"
c_fileRNAMESPACE		= sfle.d( c_strDirR, "NAMESPACE" )
c_fileRDESCRIPTION		= sfle.d( c_strDirR, "DESCRIPTION" )
c_fileRMaster			= sfle.d( c_strDirR, c_strDirRman, c_strID + "-package.Rd")

c_fileIDAnnot  			= sfle.d( pE, c_strID + ".annot.gz" )
c_fileIDMapRaw 			= sfle.d( pE, c_strID + "_raw.map" )
c_fileIDMap    			= sfle.d( pE, c_strID + ".map" )

c_fileTaxa          	= sfle.d( pE, "taxa.txt" )
c_fileStatus        	= sfle.d( pE, "status.txt" )
c_filePlatform			= sfle.d( pE, "platform.txt")
c_fileTXTGSM        	= sfle.d( pE, "GSM.txt" )
c_fileIDSeriesTXTGZ 	= sfle.d( pE, c_strID + "_series_matrix.txt.gz" )
c_fileRDataTXT     		= sfle.d( pE, c_strID + "_rdata.txt" )
c_fileRMetadataTXT  	= sfle.d( pE, c_strID + "_rmetadata.txt" )
c_fileRPlatformTXT  	= sfle.d( pE, c_strID + "_rplatform.txt" )
c_fileIDRawPCL     	 	= sfle.d( pE, c_strID + "_00raw.pcl" )
c_fileIDMappedPCL   	= sfle.d( pE, c_strID + "_00mapped.pcl")
c_fileIDPCL         	= sfle.d( pE, c_strID + ".pcl" )
c_fileEset          	= sfle.d( pE, c_strDirR, c_strDirRdata, c_strID + ".RData" )
c_folderQC            	= sfle.d( pE, c_strID + "_QC" )
c_fileHelp          	= sfle.d( pE, c_strDirR, c_strDirRman, c_strID + ".Rd" )
c_fileLogPackage    	= sfle.d( pE, "package" )
c_fileConfigPacakge 	= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirEtc, "rpackage" )
c_fileExpTable      	= sfle.d( pE, c_strID + "_exp_metadata.txt" )
c_fileCondTable     	= sfle.d( pE, c_strID + "_cond_metadata.txt" )

c_fileProgSeries2PCL      	= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "series2pcl.py" ) 
c_fileProgSeries2Metadata 	= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "series2metadata.py" ) 
c_fileProgPkl2Metadata    	= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "pkl2metadata.py" ) 
c_fileProgSeries2GSM      	= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "series2gsm.py" ) 
c_fileProgProcessRaw      	= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "preprocessRaw.R" ) 
c_fileProgAnnot2Map      	= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "annot2map.py" )
c_fileProgGPL2TXT			= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "gpl2txt.py") 
c_fileProgMergeMapping    	= sfle.d( pE, arepa.path_arepa( ), sfle.c_strDirSrc, "merge_genemapping.py" )
c_fileProgGetInfo         	= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "getinfo.py" )
c_fileProgEset2Help       	= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "eset2help.R" )
c_fileProgArrayQualMetrics 	= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "ArrayQualityMetrics.R" )

m_strGPLID		= None 
m_strPPfun   	= (sfle.readcomment( c_filePPfun ) or ["affy::rma"])[0]
m_boolRunRaw 	= sfle.readcomment( c_fileRunRaw ) == ["True"] or False 
m_boolRPackage	= sfle.readcomment( c_fileConfigPacakge ) == ["True"] or False

Import( "hashArgs" )

#===============================================================================
# Download series matrix file, Convert SERIES file with 
# platform info to PKL and PCL
#===============================================================================

#Run gse.R
sfle.ssink( pE, str(c_fileInputGSER), "R --no-save --args", [[True, c_fileIDSeriesTXTGZ], [True, c_fileRPlatformTXT], 
	[True, c_fileRMetadataTXT], [True, c_fileRDataTXT]] )

#Series2Metadata 
sfle.pipe( pE, c_fileIDSeriesTXTGZ, c_fileProgSeries2Metadata, c_fileIDPKL,
	[c_strID, [c_fileStatus]] +
	( [[c_fileInputManCurTXT]] if os.path.exists( str(c_fileInputManCurTXT) ) else [] ) )

#Create metadata tables 
sfle.sop( pE, "python", [[c_fileProgPkl2Metadata], [c_fileIDPKL], [True, c_fileExpTable], [True, c_fileCondTable]] )


#Series2PCL
sfle.pipe( pE, c_fileRDataTXT, c_fileProgSeries2PCL, c_fileIDRawPCL,
	[[c_fileRMetadataTXT], [c_fileRPlatformTXT]] )

if m_boolRPackage:
	#Make Eset containing all pertinent data
	sfle.ssink( pE, str(c_fileProgProcessRaw), "R --no-save --args", [[c_fileIDPCL], [True, c_fileEset], m_strPPfun, 
	[c_fileExpTable], [c_fileCondTable]] )
	#Make QC report
	sfle.ssink( pE, str(c_fileProgArrayQualMetrics), "R --no-save --args", [[c_fileEset], [True, c_folderQC]] )
	#Make Rd Help Page 
	sfle.ssink( pE, str(c_fileProgEset2Help), "R --no-save --args", [[c_fileEset], [True, c_fileHelp]] )	
	exec(compile(open( str(c_fileRSConscript) ).read(), str(c_fileRSConscript), 'exec'))
	funcCheckRStructure( pE, c_strID, c_fileIDPKL, c_fileRNAMESPACE, c_fileRDESCRIPTION, c_fileRMaster )
	funcMakeRPackage( pE, str(c_dirR), c_fileLogPackage )
	

# Download annotation files for specific platform, if they exist 
def getGPL( target, source, env ):
	astrTs, astrSs = ([f.get_abspath( ) for f in a] for a in (target, source))
	strAnnot, strPlatform	= astrTs[:2]
	strRMeta				= astrSs[0]
	pid = [row for row in csv.DictReader(open( strRMeta ))][0]["platform_id"] 
	strGPLID = c_strID.split("-")[1] if len( c_strID.split("-") ) == 2 else pid
	listGPL = [v.replace(".annot.gz", "") for v in sfle.readcomment( c_fileAnnot )]
	if strGPLID in listGPL:
		#Annotation file exist, download
		sfle.ex( ["wget", sfle.d( c_strURLGPL, strGPLID + ".annot.gz" ), "-O", strAnnot ] )	
	else:
		#Annotation file does not exist, skip download 
		sfle.ex( ["touch", strAnnot] )
	#Make platform file containing gpl identifier 
	with open( strPlatform, "w" ) as outputf:
		outputf.write( strGPLID )


fileAnnot = Command( [c_fileIDAnnot, c_filePlatform], c_fileRMetadataTXT, getGPL ) 


#Produce Taxa file 
sfle.pipe( pE, c_fileIDSeriesTXTGZ, c_fileProgGetInfo, c_fileTaxa )

# Clean Microarray Data -- Imputation, Normalization, Gene Mapping
# This only executes if the sleipnir configuration file in the etc directory is set to "True"
exec(compile(open( str( c_fileInputSConscript ) ).read(), str( c_fileInputSConscript ), 'exec'))
funcPCL2DAB( pE, c_fileIDRawPCL, c_fileIDAnnot, c_fileProgAnnot2Map, c_fileProgGPL2TXT, 
	c_fileProgMergeMapping, c_fileTaxa, c_filePlatform )


def scanner( fileExclude = None, fileInclude = None ):
	setstrExclude = set(readcomment( fileExclude ) if fileExclude else [])
	setstrInclude = set(readcomment( fileInclude ) if fileInclude else [])
	def funcRet( target, source, env, setstrInclude = setstrInclude, setstrExclude = setstrExclude ):
		strT, astrSs = sfle.ts( target, source )
		for strS in astrSs:
			for astrLine in csv.reader( open( strS ), csv.excel_tab ):
				if not ( astrLine and astrLine[0] ):
					continue
				strID = astrLine[0]
				if ( setstrInclude and ( strID not in setstrInclude ) ) or ( strID in setstrExclude ):
					continue
				env["sconscript_child"]( target, source[0], env, c_strID + "-RAW" )
	return funcRet

#Run RAW pipeline
if m_boolRunRaw:
	#Get list of GSM ids for processing raw files in the next step 
	afileIDsTXT = sfle.pipe( pE, c_fileIDSeriesTXTGZ, c_fileProgSeries2GSM, c_fileTXTGSM ) 
	afileIDsRaw = sfle.sconscript_children( pE, afileIDsTXT, scanner( ), 3, arepa.c_strProgSConstruct, hashArgs )
