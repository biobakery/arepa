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
import re
import gzip

def test( iLevel, strID, hashArgs ):
	return ( iLevel == 2 ) and ( strID.find( "GDS" ) == 0 ) 
if "testing" in locals( ):
	sys.exit( )

pE = DefaultEnvironment( )

c_strID				= arepa.cwd( )
c_strGDS, c_strGPL	= c_strID.split( "-" )[:2]

c_fileInputSConscript	= sfle.d( pE, arepa.path_arepa( ), sfle.c_strDirSrc, "SConscript_pcl-dab.py" ) 
c_fileRSConscript		= sfle.d( pE, arepa.path_arepa( ), sfle.c_strDirSrc, "SConscript_rpackage.py" )
c_fileInputSOFTGZ		= sfle.d( pE, "../" + c_strGDS + ".soft.gz" )
c_fileInputManCurTXT  	= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirEtc, "manual_curation/", 
							c_strID + ".txt" )
c_filePPfun				= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirEtc, "preprocess")
c_strPPfun 				= sfle.readcomment( c_filePPfun )[0]
                    
c_fileTaxa				= sfle.d( pE, "taxa.txt" )
c_fileStatus			= sfle.d( pE, "status.txt" )
c_filePlatform			= sfle.d( pE, "platform.txt" ) 
c_fileIDMap				= sfle.d( pE, c_strID + ".map" )
c_fileIDMapRaw			= sfle.d( pE, c_strID + "_raw.map" )
c_fileIDPKL				= sfle.d( pE, c_strID + ".pkl" )
c_fileGPLTXTGZ			= sfle.d( pE, c_strGPL + ".annot.gz" )
c_fileIDRawPCL			= sfle.d( pE, c_strID + "_00raw.pcl" )
c_fileLogPackage		= sfle.d( pE, "package" )
c_fileConfigPacakge 	= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirEtc, "rpackage" )
c_fileExpTable			= sfle.d( pE, c_strID + "_exp_metadata.txt" )

c_strDirR				= "R"
c_dirR					= sfle.d( c_strDirR )
c_strDirRman			= "man"
c_strDirRdata			= "data"
c_fileRNAMESPACE		= sfle.d( c_strDirR, "NAMESPACE" )
c_fileRDESCRIPTION		= sfle.d( c_strDirR, "DESCRIPTION" )
c_fileRMaster			= sfle.d( c_strDirR, c_strDirRman, c_strID + "-package.Rd")
c_fileEset 				= sfle.d( pE, c_strDirR, c_strDirRdata, c_strID + ".RData" )
c_fileHelp				= sfle.d( pE, c_strDirR, c_strDirRman, c_strID + ".Rd" )

c_fileProgSOFT2PCL	   	   	= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "soft2pcl.py" ) 
c_fileProgSOFT2Metadata	   	= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "soft2metadata.py" ) 
c_fileProgProcessRaw   	   	= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "preprocessRaw.R" ) 
c_fileProgEset2Help	   	   	= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "eset2help.R" )
c_fileProgAnnot2Map			= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "annot2map.py" ) 	
c_fileProgGPL2TXT			= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "gpl2txt.py") 
c_fileProgMergeMapping 	   	= sfle.d( pE, arepa.path_arepa( ), sfle.c_strDirSrc, "merge_genemapping.py"      )
c_fileProgGetInfo	   	   	= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "getinfo.py" )
c_fileProgPkl2Metadata 	   	= sfle.d( pE, arepa.path_repo( ), sfle.c_strDirSrc, "pkl2metadata.py" ) 
                       
m_boolRPackage	= sfle.readcomment( c_fileConfigPacakge ) == ["True"] or False

Import( "hashArgs" )

#===============================================================================
# Convert SOFT file with platform info to TXT and PCL
#===============================================================================

#Produce taxa file 
sfle.pipe( pE, c_fileInputSOFTGZ, c_fileProgGetInfo, c_fileTaxa )

#Produce platform file
sfle.scmd( pE, "echo " + c_strGPL, c_filePlatform )

#Download annotation files: in the case for GDS, GPLid is always included in name and always exists
sfle.download( pE, hashArgs["c_strURLGPL"] + os.path.basename( str( c_fileGPLTXTGZ ) ) )

#Produce pcl files 
sfle.pipe( pE, c_fileInputSOFTGZ, c_fileProgSOFT2PCL, c_fileIDRawPCL,
	[[c_fileGPLTXTGZ]] )

#Clean microarray data -- Impute, Normalize, Gene Mapping 

exec(compile(open( str(c_fileInputSConscript) ).read(), str(c_fileInputSConscript), 'exec'))
funcPCL2DAB( pE, c_fileIDRawPCL, c_fileGPLTXTGZ, c_fileProgAnnot2Map, c_fileProgGPL2TXT, 
	c_fileProgMergeMapping, c_fileTaxa, c_filePlatform )

#Get metadata from soft file 
sfle.pipe( pE, c_fileInputSOFTGZ, c_fileProgSOFT2Metadata, c_fileIDPKL,
	[[c_fileStatus]] + 
	( [[c_fileInputManCurTXT]] if os.path.exists( str(c_fileInputManCurTXT) ) else [""] ) +
	[[c_fileGPLTXTGZ]] )

#Create Tables 
sfle.sop( pE, "python", [[c_fileProgPkl2Metadata], [c_fileIDPKL], [True, c_fileExpTable]] )

if m_boolRPackage:
	#Produce expression set file
	sfle.ssink( pE, str(c_fileProgProcessRaw), "R --no-save --args", [[c_fileIDRawPCL], [True, c_fileEset], c_strPPfun, [c_fileExpTable]])
	#Make Rd Help Page 
	sfle.ssink( pE, str(c_fileProgEset2Help), "R --no-save --args", [[c_fileEset], [True, c_fileHelp]] )
	exec(compile(open( str(c_fileRSConscript) ).read(), str(c_fileRSConscript), 'exec'))
	funcCheckRStructure( pE, c_strID, c_fileIDPKL, c_fileRNAMESPACE, c_fileRDESCRIPTION, c_fileRMaster )
	funcMakeRPackage( pE, str(c_dirR), c_fileLogPackage )
	
