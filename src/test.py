#!/usr/bin/env python 
'''
This is the test module for arepa. 
'''
import arepa 
import subprocess  
import sfle
import os 
import csv 
import pickle 


c_astrInclude = ["GEO", "RegulonDB", "MPIDP", "STRING", "IntAct"]

#=====================================================#
#		General Helper Functions 
#=====================================================#

def _readstr( instr ):
	return map(lambda x: x.split("\t"),instr.strip().split("\n"))

def _read( infile, iRange = None, strDelim = None ):
	if not strDelim:
		strDelim = "\t"
	dummy = [line for line in csv.reader( open( infile ), delimiter= strDelim )]
	return ( dummy[:iRange] if iRange else dummy )

def _test( infile, aFixed, parse_function = None ):
	pTest = parse_function( infile ) if parse_function else\
		_read( infile, len( aFixed ) )
	if pTest == aFixed:
		print "test passed for", infile 
	else:
		raise Exception("!test failed", infile)

def exec_test( strDir, fParse = None, *aCouple ):
	strCur = os.getcwd( )
	os.chdir( strDir )
	subprocess.call( "scons" )
	for strTest, strVal in aCouple:
		_test( strTest, strVal, fParse )
	os.chdir( strCur )    

def runall( ):
	return None 
#=====================================================#
#			GEO
#=====================================================#
''' 
instead of testing for python pkl files, which are huge, 
test for tab delimited printed text files
'''
#constants for GEO testing 
'''
<GSEs>
manual curation - GSE8126 
multiple platforms - GSE10645, GSE16560, GSE8402 
multiple files, one platform - GSE10183
no curated file - GSE10183 

<GDSs> 
bacterial data - GDS1849, GDS3421, GDS3421. GDS3572, 
GDS3174
'''

c_strGSE8126		= 	"GSE8126"
c_strGSE10645		=	"GSE10645"
c_strGSE16560		= 	"GSE16560"
c_strGSE8402		=	"GSE8402"
c_strGSE10183		=	"GSE10183"
c_strGDS1849		=	"GDS1849"
c_strGDS3421		=	"GDS3421"
c_strGDS3572		=	"GDS3572"
c_strGDS3174		=	"GDS3174"

c_astrMetaKeys		= 	["taxid","pmid","platform","gloss","channels","conditions"]

c_dirGEO		=	sfle.d( arepa.path_arepa( ), "GEO")
c_dirGEOData		= 	sfle.d( c_dirGEO, sfle.c_strDirData )

###GSE10183###
 
c_dirGSE10183base	=	sfle.d( c_dirGEOData,c_strGSE10183 )
c_dirGSE10183		=	sfle.d( c_dirGSE10183base, c_strGSE10183 )
c_fileGSE10183PKL	= 	sfle.d( c_dirGSE10183, c_strGSE10183 + ".pkl" )
c_fileGSE10183PCL	=	sfle.d( c_dirGSE10183, c_strGSE10183 + "_00raw.pcl" ) 

'''
{k:hMeta.get(k) for k in ["taxid", "pmid", "platform", "gloss", "channels", "conditions"]} 
'''

c_GSE10183PKL		= {'gloss': 'Cancer cells were MACS sorted from tumor tissue specimem 05-179. Self replicates of CD26+ cancer cells were generated and the expression profiles were determined using Affymetrix U133 Plus 2.0 arrays. These data represent cancer cell type specific transcriptome.\nKeywords: disease state analysis', 'taxid': '9606', 'channels': 1, 'platform': 'GPL570', 'pmid': None, 'conditions': 2}

c_GSE10183PCL		= 	[['GID', 'NAME', 'GWEIGHT', 
				'GSM257248: CD26+ cancer cell, replicate 1', \
				'GSM257249: CD26+ cancer cell, replicate 2'], 
				['EWEIGHT', '', '', '1', '1'],
				['1007_s_at', 'U48705', '1', '10.34880883', '10.25328334'],
				['1053_at', 'M87338', '1', '7.096953279', '7.16038339'],
				['117_at', 'X51757', '1', '10.89463506', '10.85675361'],
				['121_at', 'X69699', '1', '8.020897183', '7.84238035']]

#exec_test( c_dirGEO, lambda f: {k:pickle.load(open(f,"r")).get(k) for k in c_astrMetaKeys},\
#[c_fileGSE10183PKL, c_GSE10183PKL] )
exec_test( c_dirGEO, None, [c_fileGSE10183PCL,c_GSE10183PCL] )

###GSE8126###

c_dirGSE8126base	=	sfle.d( c_dirGEOData,c_strGSE8126 )
c_dirGSE8126		= 	sfle.d( c_dirGSE8126base, c_strGSE8126 )
c_fileGSE8126PKL	= 	sfle.d( c_dirGSE8126, c_strGSE8126 + ".pkl" )
c_fileGSE8126PCL	=	sfle.d( c_dirGSE8126, c_strGSE8126 + "_00raw.pcl" ) 

c_GSE8126EXP		=	_readstr( "Series_platform_taxid\tSeries_contact_department\tSeries_contact_name\tSeries_status\tgloss\tSeries_relation\tSeries_contact_state\tSeries_contact_address\tSeries_contact_city\tplatform\tSeries_contact_laboratory\tSeries_overall_design\tSeries_contributor\tSeries_contact_country\tSeries_contact_zip/postal_code\tSeries_supplementary_file\tSeries_geo_accession\tSeries_sample_id\ttaxid\tSeries_contact_institute\tSeries_submission_date\tSeries_last_update_date\r\n9606\tGenetics, USP Medical School at Ribeirao Preto\tRicardo,Z.N.,V\xc3\xaancio\tPublic on Jan 14 2009\tCancer cells were MACS sorted from tumor tissue specimem 05-179. Self replicates of CD26+ cancer cells were generated and the expression profiles were determined using Affymetrix U133 Plus 2.0 arrays. These data represent cancer cell type specific transcriptome. Keywords: disease state analysis\tBioProject: http://www.ncbi.nlm.nih.gov/bioproject/108397\tSP\tAv. Bandeirantes, 3900\tRibeirao Preto\tGPL570\thttp://labpib.fmrp.usp.br\tSelf replicates of the sorted were done.\tAlvin,,Liu\tBrazil\t14049-900\tftp://ftp.ncbi.nlm.nih.gov/pub/geo/DATA/supplementary/series/GSE10183/GSE10183_RAW.tar\tGSE10183\tGSM257248 GSM257249 \t9606\tUniversidade de S\xc3\xa3o Paulo\tJan 15 2008\tJun 06 2012\r\n" )	 

#exec_test( c_dirGEO, lambda f: {k:pickle.load(open(f,"r")).get(k) for k in c_astrMetaKeys},\
# [c_fileGSE8126PKL, c_GSE8126PKL] )
#exec_test( c_dirGEO, None, [c_fileGSE8126PCL,c_GSE8126PCL] )
 
#=====================================================#
#               	Bacteriome
#=====================================================#
#single dataset 

c_dirBacteriome		= 	sfle.d( arepa.path_arepa( ), "Bacteriome" )
c_dirBacteriomeData	=	sfle.d( c_dirBacteriome, sfle.c_strDirData )
c_fileBacteriomeDat	= 	sfle.d( c_dirBacteriomeData, "bacteriome.dat" )
c_fileBacteriomeQuant	=	sfle.d( c_dirBacteriomeData, "bacteriome.quant")

c_BacteriomeQuantLst	=	[["0.5","1.5"]]
c_BacteriomeDatLst	= 	[["b0002","b0003","0.408408"],["b0002","b0004","0.408408"]]

exec_test( c_dirBacteriome, None, [c_fileBacteriomeQuant, c_BacteriomeQuantLst], \
	[ c_fileBacteriomeDat, c_BacteriomeDatLst ] )
 	
#=====================================================#
#                       BioGrid
#=====================================================#
#single dataset 

c_strBioGrid		= "taxid_224308"
c_dirBioGrid		= sfle.d( arepa.path_arepa( ), "BioGrid" )
c_dirBioGridData	= sfle.d( c_dirBioGrid, sfle.c_strDirData, c_strBioGrid )
c_fileBioGridPKL	= sfle.d( c_dirBioGridData, "taxid_224308.pkl" )
c_fileBioGridDat	= sfle.d( c_dirBioGridData, "taxid_224308.dat" )
c_fileBioGridQuant	= sfle.d( c_dirBioGridData, "taxid_224308.quant" )

c_BioGridDat		= [['rsbV', 'rsbW', '1']] 
c_BioGridPKL		= {'platform': 'Co-purification', 'pmid': '8144446', 'type': '857505', 'taxid': '855787'}
c_BioGridQuant		= [["0.5", "1.5"]]

exec_test( c_dirBioGrid, None, [c_fileBioGridDat, c_BioGridDat], [c_fileBioGridQuant, c_BioGridQuant] )
exec_test( c_dirBioGrid, lambda f: pickle.load( open(f, "r") ), [c_fileBioGridPKL, c_BioGridPKL] )

#=====================================================#
#                       IntAct
#=====================================================#
#multiple datasets

#=====================================================#
#                       MPIDB
#=====================================================#
#multiple datasets


#=====================================================#
#                       RegulonDB 
#=====================================================#
#single dataset  

c_dirRegulon		= sfle.d( arepa.path_arepa( ), "RegulonDB" )
c_dirRegulonData	= sfle.d( c_dirRegulon, sfle.c_strDirData ) 

c_RegulonDatLst		= [['AccB', 'accB', '1'], ['AccB', 'accC', '1'], ['AcrR', 'acrA', '1'], ['AcrR', 'acrB', '1']]
c_RegulonQuantLst	= [["0.5", "1.5"]]

c_fileRegulonDat	= sfle.d( c_dirRegulonData, "regulondb.dat" )
c_fileRegulonQuant	= sfle.d( c_dirRegulonData, "regulondb.quant" ) 

#execute 
exec_test( c_dirRegulon, None, [c_fileRegulonDat, c_RegulonDatLst], [c_fileRegulonQuant, c_RegulonQuantLst] ) 

#=====================================================#
#                       STRING
#=====================================================#
#multiple datasets 

c_strSTRINGtaxid		= "taxid_189918_mode"
c_strSTRINGtaxidBinding		= c_strSTRINGtaxid + "_binding" 
c_strSTRINGtaxidExpression	= c_strSTRINGtaxid + "_expression"
c_strSTRINGtaxidPtmod		= c_strSTRINGtaxid + "_ptmod"

c_dirSTRING		= sfle.d( arepa.path_arepa( ), "STRING" )
c_dirSTRINGData		= sfle.d( c_dirSTRING, sfle.c_strDirData )

c_dirSTRINGtaxidBinding 	= sfle.d( c_dirSTRINGData, c_strSTRINGtaxidBinding )
c_fileSTRINGtaxidBindingDat	= sfle.d( c_dirSTRINGtaxidBinding, c_strSTRINGtaxidBinding + ".dat" )
c_fileSTRINGtaxidBindingQuant	= sfle.d( c_dirSTRINGtaxidBinding, c_strSTRINGtaxidBinding + ".quant")

c_dirSTRINGtaxidExpression  	= sfle.d( c_dirSTRINGData, c_strSTRINGtaxidExpression )
c_fileSTRINGtaxidExpressionDat	= sfle.d( c_dirSTRINGtaxidExpression, c_strSTRINGtaxidExpression + \
					".dat" )
c_fileSTRINGtaxidExpressionQuant= sfle.d( c_dirSTRINGtaxidExpression, c_strSTRINGtaxidExpression + \
					".quant" )

c_dirSTRINGtaxidPtmod		= sfle.d( c_dirSTRINGData, c_strSTRINGtaxidPtmod )
c_fileSTRINGtaxidPtmodDat	= sfle.d( c_dirSTRINGtaxidExpression, c_strSTRINGtaxidPtmod + \
					".dat" )
c_fileSTRINGtaxidPtmodQuant	= sfle.d( c_dirSTRINGtaxidExpression, c_strSTRINGtaxidPtmod + \
					".quant" )

c_STRINGtaxidBindingDat		= [['Mkms_5492', 'Mkms_2727', '0.322'],
				['Mkms_5492', 'Mkms_2193', '0.322'],
				['Mkms_5492', 'Mkms_3950', '0.306'],
				['Mkms_5492', 'Mkms_3510', '0.298'],
				['Mkms_5492', 'Mkms_2005', '0.272'],
				['Mkms_5492', 'Mkms_1151', '0.28'],
				['Mkms_5492', 'Mkms_1004', '0.264'],
				['Mkms_5492', 'Mkms_4326', '0.322'],
				['Mkms_5492', 'Mkms_0514', '0.292'],
				['Mkms_5492', 'Mkms_0939', '0.3']]
c_STRINGtaxidBindingQuant	= [["0.5","1.5"]]

c_STRINGtaxidExpressionDat	= [['Mkms_1995', 'Mkms_2223', '0.346'],
				['Mkms_2223', 'Mkms_4068', '0.35'],
				['Mkms_2223', 'Mkms_2460', '0.181'],
				['Mkms_2223', 'Mkms_5148', '0.359'],
				['Mkms_2223', 'Mkms_1397', '0.272'],
				['Mkms_3390', 'Mkms_0476', '0.21'],
				['Mkms_0476', 'Mkms_0473', '0.714'],
				['Mkms_1345', 'Mkms_4126', '0.197'],
				['Mkms_4068', 'Mkms_5011', '0.181'],
				['Mkms_4068', 'Mkms_1397', '0.357'],
				['Mkms_3160', 'Mkms_3147', '0.265']] 
c_STRINGtaxidExpressionQuant	= [["0.5","1.5"]]

c_STRINGtaxidPtmodDat		= [['Mkms_0391', 'Mkms_0470', '0.173'],
				['Mkms_0391', 'Mkms_2458', '0.316'],
				['Mkms_1218', 'Mkms_5095', '0.226'],
				['Mkms_0025', 'Mkms_0023', '0.445'],
				['Mkms_3334', 'Mkms_3333', '0.365'],
				['Mkms_2004', 'Mkms_2003', '0.204']]
c_STRINGtaxidPtmodQuant 	= [["0.5","1.5"]]

exec_test( c_dirSTRING, None, [c_fileSTRINGtaxidBindingQuant, c_STRINGtaxidBindingQuant],\
		[c_fileSTRINGtaxidBindingDat, c_STRINGtaxidBindingDat],\
		[c_fileSTRINGtaxidExpressionQuant, c_STRINGtaxidExpressionQuant],\
		[c_fileSTRINGtaxidExpressionDat, c_STRINGtaxidExpressionDat],\
		[c_fileSTRINGtaxidPtmodQuant, c_STRINGtaxidPtmodQuant],\
		[c_fileSTRINGtaxidPtmodDat, c_STRINGtaxidPtmodDat] )

