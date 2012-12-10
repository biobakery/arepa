#!/usr/bin/env python

import arepa
import sfle
import sys
import csv
import os 
import metadata 

def test( iLevel, strID, hashArgs ):
	return ( iLevel == 2 ) and ( strID.find( "GSE" ) == 0 ) 
if locals( ).has_key( "testing" ):
	sys.exit( )

pE = DefaultEnvironment( )

c_strID                 = arepa.cwd( )
c_fileGPL               = sfle.d( pE, arepa.path_repo( ), sfle.c_strDirTmp, "gpl.txt" ) 
c_fileAnnot             = sfle.d( pE, arepa.path_repo( ), sfle.c_strDirTmp, "annot.txt" ) 
c_fileInputSConscript   = sfle.d( pE, arepa.path_arepa( ), sfle.c_strDirSrc, 
                                 "SConscript_pcl-dab.py" ) 
c_fileProgUnpickle      = sfle.d( pE, arepa.path_arepa( ), sfle.c_strDirSrc, "unpickle.py" ) 
c_fileInputGSER         = sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "gse.R" ) 
c_fileInputManCurTXT    = sfle.d( pE, arepa.path_repo( ), sfle.c_strDirEtc,   
                                 "manual_curation/", c_strID + "_curated_pdata.txt" )

c_filePPfun             = sfle.d( pE, arepa.path_repo( ), sfle.c_strDirEtc, "preprocess")
c_strPPfun              = sfle.readcomment( c_filePPfun )[0]
c_fileIDPKL             = sfle.d( pE, c_strID + ".pkl" )
c_strURLGPL             = hashArgs["c_strURLGPL"]
c_strHost               = "ftp.ncbi.nih.gov"
c_strPath               = "pub/geo/DATA/annotation/platforms/"
c_fileIDAnnot           = sfle.d( pE, c_strID + ".annot.gz" )
c_fileIDMap             = sfle.d( pE, c_strID + ".map" )

c_fileStatus		= sfle.d( pE, "status.txt" )
c_fileTXTGSM		= sfle.d( pE, "GSM.txt" )
c_fileIDSeriesTXTGZ	= sfle.d( pE, c_strID + "_series_matrix.txt.gz" )
c_fileRDataTXT		= sfle.d( pE, c_strID + "_rdata.txt" )
c_fileRMetadataTXT	= sfle.d( pE, c_strID + "_rmetadata.txt" )
c_fileRPlatformTXT	= sfle.d( pE, c_strID + "_rplatform.txt" )
c_fileIDRawPCL		= sfle.d( pE, c_strID + "_00raw.pcl" )
c_fileIDMappedPCL	= sfle.d( pE, c_strID + "_00mapped.pcl")
c_fileIDPCL             = sfle.d( pE, c_strID + ".pcl" )
c_fileEset              = sfle.d( pE, c_strID + ".RData" )
c_fileExpTable          = sfle.d( pE, c_strID + "_exp_metadata.txt" )
c_fileCondTable         = sfle.d( pE, c_strID + "_cond_metadata.txt" )

c_fileProgSeries2PCL        	= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "series2pcl.py" ) 
c_fileProgSeries2Metadata   	= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "series2metadata.py" ) 
c_fileProgPkl2Metadata      	= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "pkl2metadata.py" ) 
c_fileProgSeries2GSM		= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "series2gsm.py" ) 
c_fileProgProcessRaw		= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "preprocessRaw.R" ) 
c_fileProgAnnot2Map		= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "annot2map.py" ) 

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

#Make Eset containing all pertinent data
sfle.ssink( pE, str(c_fileProgProcessRaw), "R --no-save --args", [[c_fileIDPCL], [True, c_fileEset], c_strPPfun, 
	[c_fileExpTable], [c_fileCondTable]] )

# Download annotation files for specific platform, if they exist 
def getGPL( target, source, env ):
	astrTs, astrSs = ([f.get_abspath( ) for f in a] for a in (target,source))
	strAnnot		= astrTs[0]
	strRMeta		= astrSs[0]
	pid = [row for row in csv.DictReader(open( strRMeta ))]\
		[0]["platform_id"] 
	strGPLID = c_strID.split("-")[1] if len( c_strID.split("-") ) == 2 else pid
	listGPL = map( lambda v: v.replace(".annot.gz",""), \
		sfle.readcomment( c_fileAnnot ) )
	if strGPLID in listGPL:
		#Annotation file exist, download
		sfle.ex( ["wget", sfle.d( c_strURLGPL, strGPLID + ".annot.gz" ), "-O", \
			strAnnot ] )	
	else:
		#Annotation file does not exist, skip download 
		with open( strGPLID + ".annot.gz", "w") as outputf:
			outputf.write(" ")

fileAnnot = Command( c_fileIDAnnot, c_fileRMetadataTXT, getGPL ) 

#Produce mapping files for gene mapping; if does not exist, then nothing. 
fileGeneMap = sfle.pipe( pE, c_fileIDAnnot, c_fileProgAnnot2Map, c_fileIDMap ) 

#Clean Microarray Data -- Imputation, Normalization, Gene Mapping    
execfile( str( c_fileInputSConscript ) )
funcPCL2DAB( pE, c_fileIDRawPCL )

def scanner( fileExclude = None, fileInclude = None ):
	setstrExclude = set(readcomment( fileExclude ) if fileExclude else [])
	setstrInclude = set(readcomment( fileInclude ) if fileInclude else [])
	def funcRet( target, source, env, setstrInclude = setstrInclude, \
		setstrExclude = setstrExclude ):
		strT, astrSs = sfle.ts( target, source )
		for strS in astrSs:
			for astrLine in csv.reader( open( strS ), csv.excel_tab ):
				if not ( astrLine and astrLine[0] ):
					continue
				strID = astrLine[0]
				if ( setstrInclude and ( strID not in setstrInclude ) ) or \
					( strID in setstrExclude ):
					continue
				env["sconscript_child"]( target, source[0], env, c_strID + "-RAW" )
	return funcRet

#Get list of GSM ids for processing raw files in the next step 
afileIDsTXT = sfle.pipe( pE, c_fileIDSeriesTXTGZ, c_fileProgSeries2GSM, c_fileTXTGSM ) 

#Run RAW pipeline
#ADDITION: run when configuration file says to  

afileIDsRaw = sfle.sconscript_children( pE, afileIDsTXT , scanner( ), 3, arepa.c_strProgSConstruct, hashArgs )
