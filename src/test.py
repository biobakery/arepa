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

exec_test( c_dirGEO, lambda f: {k:pickle.load(open(f,"r")).get(k) for k in c_astrMetaKeys},\
 [c_fileGSE10183PKL, c_GSE10183PKL] )
exec_test( c_dirGEO, None, [c_fileGSE10183PCL,c_GSE10183PCL] )

###GSE8126###

c_dirGSE8126base	=	sfle.d( c_dirGEOData,c_strGSE8126 )
c_dirGSE8126		= 	sfle.d( c_dirGSE8126base, c_strGSE8126 )
c_fileGSE8126PKL	= 	sfle.d( c_dirGSE8126, c_strGSE8126 + ".pkl" )
c_fileGSE8126PCL	=	sfle.d( c_dirGSE8126, c_strGSE8126 + "_00raw.pcl" ) 

c_GSE8126PKL 		= {'gloss': 'MicroRNAs are small non-coding RNAs that regulate mRNA function. Recent studies have shown that microRNA expression is altered in tumors. We studied the expression of both microRNAs and mRNAs in 60 primary prostate tumors and 16 non-tumor prostate tissues to evaluate the involvement of microRNAs in prostate cancer. Global microRNA expression was determined in RNA isolated from fresh-frozen human tissues with a custom oligonucleotide microarray chip. Expression analysis of mRNAs using Affymetrix gene chips revealed that Dicer, a key component of microRNA processing, and two microRNA host genes, MCM7 and C9orf5, were significantly up-regulated in prostate tumors. Consistent with the findings, tumors expressed at higher levels the miR-25 cluster (miR-25/miR-93/miR-106b), which maps to intron 13 of MCM7, and miR-32, which maps to intron 14 of C9orf5, than non-tumor prostate tissues. Other microRNAs that were overexpressed included miR-26a, miR-31, miR-182, miR-196a, and miR-200c, among others, and homologues of the miR-25 cluster, such as miR-92 and miR-106a. Among the down-regulated microRNAs in tumors were the miR-1/miR-133a cluster, miR-490, miR-494 and miR-520h. Differences in microRNA expression were also observed between high and low Gleason score and between tumors that either showed or did not show extraprostatic extension. A 37-probeset signature, representing 23 different mature microRNAs, correctly classified all non-tumor tissues and 80% of the tumors. In summary, our data indicate that alterations in microRNA expression occur in the development and progression of human prostate cancer. Such changes may prove useful in the development of novel diagnostic and prognostic markers.\nKeywords: Marcodissected tissues', 'taxid': '9606', 'channels': 1, 'platform': 'GPL5180', 'pmid': '18676839', 'conditions': 76}

c_GSE8126PCL		=	[['GID', 'NAME', 'GWEIGHT', 'GSM201402: Prostate tumor patient 1', 'GSM201403: Prostate tumor patient 2', 'GSM201404: Prostate tumor patient 4', 'GSM201405: Prostate tumor patient 5', 'GSM201406: Prostate tumor patient 6', 'GSM201407: Prostate tumor patient 7', 'GSM201408: Prostate tumor patient 8', 'GSM201409: Prostate tumor patient 9', 'GSM201410: Prostate tumor patient 10', 'GSM201411: Prostate tumor patient 12', 'GSM201412: Prostate tumor patient 13', 'GSM201413: Prostate tumor patient 14', 'GSM201414: Prostate tumor patient 15', 'GSM201415: Prostate tumor patient 16', 'GSM201416: Prostate tumor patient 17', 'GSM201417: Prostate tumor patient 18', 'GSM201418: Prostate tumor patient 20', 'GSM201419: Prostate tumor patient 21', 'GSM201420: Prostate tumor patient 22', 'GSM201421: Prostate tumor patient 23', 'GSM201422: Prostate tumor patient 26', 'GSM201423: Prostate tumor patient 27', 'GSM201424: Prostate tumor patient 28', 'GSM201425: Prostate tumor patient 29', 'GSM201426: Prostate tumor patient 30', 'GSM201427: Prostate tumor patient 33', 'GSM201428: Prostate tumor patient 34', 'GSM201429: Prostate tumor patient 35', 'GSM201430: Prostate tumor patient 36', 'GSM201431: Prostate tumor patient 37', 'GSM201432: Prostate tumor patient 38', 'GSM201433: Prostate tumor patient 39', 'GSM201434: Prostate tumor patient 40', 'GSM201435: Prostate tumor patient 41', 'GSM201436: Prostate tumor patient 42', 'GSM201437: Prostate tumor patient 43', 'GSM201438: Prostate tumor patient 44', 'GSM201439: Prostate tumor patient 45', 'GSM201440: Prostate tumor patient 47', 'GSM201441: Prostate tumor patient 48', 'GSM201442: Prostate tumor patient 49', 'GSM201443: Prostate tumor patient 51', 'GSM201444: Prostate tumor patient 52', 'GSM201445: Prostate tumor patient 53', 'GSM201446: Prostate tumor patient 54', 'GSM201447: Prostate tumor patient 55', 'GSM201448: Prostate tumor patient 56', 'GSM201449: Prostate tumor patient 57', 'GSM201450: Prostate tumor patient 58', 'GSM201451: Prostate tumor patient 59', 'GSM201452: Prostate tumor patient 60', 'GSM201453: Prostate tumor patient 61', 'GSM201454: Surrounding normal prostate tissue patient 63', 'GSM201455: Surrounding normal prostate tissue patient 65', 'GSM201456: Prostate tumor patient 65', 'GSM201457: Surrounding normal prostate tissue patient 68', 'GSM201458: Prostate tumor patient 68', 'GSM201459: Surrounding normal prostate tissue patient 70', 'GSM201460: Prostate tumor patient 70', 'GSM201461: Surrounding normal prostate tissue patient 72', 'GSM201462: Prostate tumor patient 72', 'GSM201463: Prostate tumor patient 73', 'GSM201464: Prostate tumor patient 74', 'GSM201465: Surrounding normal prostate tissue patient 76', 'GSM201466: Prostate tumor patient 76', 'GSM201467: Prostate tumor patient 77', 'GSM201468: Surrounding normal prostate tissue protate cancer patient A', 'GSM201469: Surrounding normal prostate tissue protate cancer patient B', 'GSM201470: Surrounding normal prostate tissue protate cancer patient C', 'GSM201471: Surrounding normal prostate tissue patient 31', 'GSM201472: Surrounding normal prostate tissue patient 45', 'GSM201473: Surrounding normal prostate tissue patient 16', 'GSM201474: Surrounding normal prostate tissue patient 21', 'GSM201475: Surrounding normal prostate tissue patient D', 'GSM201476: Surrounding normal prostate tissue patient 4', 'GSM201477: Surrounding normal prostate tissue patient 57'],
['EWEIGHT', '', '', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
['1-1-1', 'hsa-mir-034', '1', '7.454572201', '7.929065228', '8.781358719', '8.264443398', '7.599515438', '8.012377739', '8.393390656', '8.40087986', '7.911969185', '8.05437851', '8.600532532', '7.9410882', '8.285172462', '8.407489777', '8.274128914', '8.211891174', '8.364419937', '8.26709938', '8.512517929', '7.558802605', '8.188314438', '8.401195526', '7.893549442', '8.62727356', '8.285500526', '8.743163109', '8.076814651', '8.589333534', '8.463033676', '8.545368195', '8.456708908', '8.223172188', '8.589561462', '8.527477264', '8.364340782', '8.131261826', '8.211044312', '8.178192139', '7.813139915', '8.091988564', '8.479288101', '7.391807556', '8.144738197', '7.299207687', '7.082748413', '7.238315582', '7.792229176', '6.860268593', '7.51306963', '7.839384079', '7.152135849', '7.98261404', '7.879654408', '8.147205353', '8.589183807', '7.834626198', '8.277675629', '8.089708328', '7.83637619', '8.468889236', '7.952532768', '8.398460388', '8.820554733', '8.489021301', '8.440450668', '8.117786407', '7.985947609', '8.260835648', '8.782951355', '8.651992798', '7.488026142', '8.201763153', '7.666116238', '8.174925804', '7.867964745', '8.425005913'],
['1-1-10', '', '1', '5.086596966', '5.895345211', '4.922320366', '5.888743401', '4.960614204', '5.672527313', '6.430452347', '5.67242527', '5.534448624', '6.026544571', '6.026062012', '6.29898119', '5.222162724', '6.97008419', '5.739539623', '5.717574596', '6.007819653', '5.248721123', '8.011533737', '6.751447678', '5.781808376', '6.181750298', '5.384890079', '5.865070343', '5.228468895', '5.077827454', '5.69538641', '5.585997581', '5.275007248', '2.975512266', '5.361551285', '5.161396027', '5.415424347', '5.209453583', '5.527839661', '4.604715824', '6.073540211', '5.271301746', '5.285402298', '5.378293037', '4.397138596', '6.272508621', '5.247185707', '4.584962845', '6.23886776', '6.375819206', '6.207266808', '4.931352615', '5.70043993', '5.303330898', '5.590256691', '5.424026489', '5.231366158', '4.527477264', '5.718818188', '5.097660542', '5.029747486', '5.57644701', '4.763128281', '6.047425747', '5.450033188', '5.365712166', '4.57787323', '8.119551659', '4.894482613', '5.239465714', '5.466311455', '5.344220161', '4.983156681', '6.696074009', '4.524551868', '6.695067883', '7.575918674', '5.754887581', '4.775518894', '6.961160183']]

exec_test( c_dirGEO, lambda f: {k:pickle.load(open(f,"r")).get(k) for k in c_astrMetaKeys},\
 [c_fileGSE8126PKL, c_GSE8126PKL] )
exec_test( c_dirGEO, None, [c_fileGSE8126PCL,c_GSE8126PCL] )
 
#=====================================================#
#               	ArrayExpress
#=====================================================#
#Test module for ArrayExpress does not exist

#=====================================================#
#               	Bacteriome
#=====================================================#
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
#                       MPIDP
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

c_dirSTRING		= sfle.d( arepa.path_arepa( ), "STRING" )
c_dirSTRINGData		= sfle.d( c_dirSTRING, sfle.c_strDirData )




