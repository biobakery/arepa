#!/usr/bin/env python

import arepa
import sfle
import sys
import csv
import os 

def test( iLevel, strID, hashArgs ):
	return ( iLevel == 2 ) and ( strID.find( "GSE" ) == 0 ) 
if locals( ).has_key( "testing" ):
	sys.exit( )

c_strID					= arepa.cwd( )
c_fileInputSConscript		= File( sfle.d( arepa.path_arepa( ), sfle.c_strDirSrc, "SConscript_pcl-dab.py" ) )
c_fileInputGSER				= File( sfle.d( arepa.path_repo( ), sfle.c_strDirSrc, "gse.R" ) )
c_fileInputManCurTXT		= File( sfle.d( arepa.path_repo( ), sfle.c_strDirEtc, "manual_curation/",
								c_strID + "_curated_pdata.txt" ) )

c_fileIDPKL					= File( c_strID + ".pkl" )
c_fileTXTGSM					= File( "GSM.txt" )
c_fileIDSeriesTXTGZ			= File( c_strID + "_series_matrix.txt.gz" )
c_fileRDataTXT				= File( c_strID + "_rdata.txt" )
c_fileRMetadataTXT			= File( c_strID + "_rmetadata.txt" )
c_fileRPlatformTXT			= File( c_strID + "_rplatform.txt" )
c_fileIDRawPCL				= File( c_strID + "_00raw.pcl" )

c_fileProgSeries2PCL		= File( sfle.d( arepa.path_repo( ), sfle.c_strDirSrc, "series2pcl.py" ) )
c_fileProgSeries2Metadata	= File( sfle.d( arepa.path_repo( ), sfle.c_strDirSrc, "series2metadata.py" ) )
c_fileProgSeries2GSM		= File( sfle.d( arepa.path_repo( ), sfle.c_strDirSrc, "series2gsm.py" ) )

pE = DefaultEnvironment( )
Import( "hashArgs" )

#===============================================================================
# Download series matrix file, Convert SERIES file with 
# platform info to PKL and PCL
#===============================================================================

def funcGSER( target, source, env ):
	astrTs, astrSs = ([f.get_abspath( ) for f in a] for a in (target, source))
	strSeriesGZ, strData, strMetadata, strPlatform = astrTs[:4]
	strIn = astrSs[0]
	return sfle.ex( (sfle.cat( strIn ), " | R --no-save --args", strSeriesGZ, strPlatform, strMetadata, strData) )

Command( [c_fileIDSeriesTXTGZ, c_fileRDataTXT, c_fileRMetadataTXT, c_fileRPlatformTXT],
	[c_fileInputGSER], funcGSER )

sfle.pipe( pE, c_fileIDSeriesTXTGZ, c_fileProgSeries2Metadata, c_fileIDPKL,
	[[False, c_strID]] + ( [[True, c_fileInputManCurTXT]] if os.path.exists( str(c_fileInputManCurTXT) ) else [] ) )

sfle.pipe( pE, c_fileRDataTXT, c_fileProgSeries2PCL, c_fileIDRawPCL,
	[[True, f] for f in (c_fileRMetadataTXT, c_fileRPlatformTXT)] )

#Get list of GSMs
afileIDsTXT = sfle.pipe( pE, c_fileIDSeriesTXTGZ, c_fileProgSeries2GSM, c_fileTXTGSM ) 

# Sleipnir features  
#execfile( str(c_fileInputSConscript) )

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


afileIDsRaw = sfle.sconscript_children( pE, afileIDsTXT , scanner( ), 3, arepa.c_strProgSConstruct, hashArgs )
