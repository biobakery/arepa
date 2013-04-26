#!/usr/bin/env python 
'''
Test script for arepa. 

Usage: python test.py [scons]
'''
import arepa 
import subprocess  
import sfle
import os 
import csv 
import pickle 
import sys 

if len(sys.argv[1:]) > 0:
	f_scons = True if sys.argv[1] == "scons" else False 
else:
	f_scons = False 

#=====================================================#
#		ARepA Submodules		      			
#=====================================================#

c_strGEO 		= "GEO"
c_strRegulonDB	= "RegulonDB"
c_strMPIDB		= "MPIDB"
c_strSTRING		= "STRING"
c_strIntAct		= "IntAct"
c_strBioGrid	= "BioGrid" 

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
	pTest = parse_function( infile ) if parse_function else _read( infile, len( aFixed ) )
	
	if pTest == aFixed:
		print "test passed for", infile 
	else:
		print "pTest is", pTest
		print "aFixed is", aFixed 
		raise Exception("!test failed", infile)
	

def exec_test( strDir, fParse = None, *aCouple ):
	strCur = os.getcwd( )
	os.chdir( strDir )
	if f_scons:
		subprocess.call( "scons" )
	for strTest, strVal in aCouple:
		_test( strTest, strVal, fParse )
	os.chdir( strCur )    

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
GSE12831: E. coli

<GDSs> 
GDS2250-GPL570: Homo sapiens 
'''


c_strGDS2250		=	"GDS2250-GPL570"
c_strGSE12831		= 	"GSE12831"

c_astrMetaKeys		= 	["taxid","pmid","platform","gloss","channels","conditions"]

c_dirGEO			=	sfle.d( arepa.path_arepa( ), "GEO")
c_dirGEOData		= 	sfle.d( c_dirGEO, sfle.c_strDirData )

###GDS2250-GPL570###
 
c_dirGDS2250base	=	sfle.d( c_dirGEOData, c_strGDS2250.split("-")[0] )
c_dirGDS2250		=	sfle.d( c_dirGSE10183base, c_strGSE10183 )
c_fileGDS2250PKL	= 	sfle.d( c_dirGSE10183, c_strGSE10183 + ".pkl" )
c_fileGDS2250PCL	=	sfle.d( c_dirGSE10183, c_strGSE10183 + ".pcl" ) 


c_GSE10183PKL		=	{'channels': '1',
						 'conditions': '47',
						 'gloss': 'Analysis of sporadic basal-like cancer (BLC), BRCA-associated breast cancer, and non-BLC tumors. Sporadic BLC are phenotypically similar to BRCA1-associated cancers. Results provide insight into the molecular pathogenesis of BLC and BRCA1-associated breast cancer.',
						 'mapped': 'True',
						 'platform': 'GPL570',
						 'pmid': '20400965',
						 'taxid': '9606',
						 'title': 'Basal-like breast cancer tumors',
						 'type': 'expression profiling'}

c_GSE10183PCL		= 	[['GID',
					  'NAME',
					  'GWEIGHT',
					  'Value for GSM85513: NB42 U133p2; src: NB42',
					  'Value for GSM85514: NB58 U133p2; src: NB58',
					  'Value for GSM85515: NB60 U133p2; src: NB60',
					  'Value for GSM85516: NB64 U133p2; src: NB64',
					  'Value for GSM85517: NB69 U133p2; src: NB69',
					  'Value for GSM85518: NB83 U133p2; src: NB83',
					  'Value for GSM85519: NB87 U133p2; src: NB87',
					  'Value for GSM85493: T37 U133p2; src: T37',
					  'Value for GSM85494: T183 U133p2; src: T183',
					  'Value for GSM85495: T117 U133p2; src: T117',
					  'Value for GSM85496: T161 U133p2; src: T161',
					  'Value for GSM85497: T30 U133p2; src: T30',
					  'Value for GSM85498: T84 U133p2; src: T84',
					  'Value for GSM85499: T115 U133p2; src: T115',
					  'Value for GSM85500: T44 U133p2; src: T44',
					  'Value for GSM85501: T81 U133p2; src: T81',
					  'Value for GSM85502: T50 U133p2; src: T50',
					  'Value for GSM85503: T4 U133p2; src: T4',
					  'Value for GSM85504: T175 U133p2; src: T175',
					  'Value for GSM85505: T178 U133p2; src: T178',
					  'Value for GSM85506: T41 U133p2; src: T41',
					  'Value for GSM85507: T73 U133p2; src: T73',
					  'Value for GSM85508: T92 U133p2; src: T92',
					  'Value for GSM85509: T74 U133p2; src: T74',
					  'Value for GSM85510: T162 U133p2; src: T162',
					  'Value for GSM85511: T145 U133p2; src: T145',
					  'Value for GSM85512: T119 U133p2; src: T119',
					  'Value for GSM85491: T151 U133p2; src: T151',
					  'Value for GSM85492: T152 U133p2; src: T152',
					  'Value for GSM85473: T118 U133p2; src: T118',
					  'Value for GSM85474: T134 U133p2; src: T134',
					  'Value for GSM85475: T140 U133p2; src: T140',
					  'Value for GSM85476: T141 U133p2; src: T141',
					  'Value for GSM85477: T146 U133p2; src: T146',
					  'Value for GSM85478: T147 U133p2; src: T147',
					  'Value for GSM85479: T149 U133p2; src: T149',
					  'Value for GSM85480: T133 U133p2; src: T133',
					  'Value for GSM85481: T21 U133p2; src: T21',
					  'Value for GSM85482: T56 U133p2; src: T56',
					  'Value for GSM85483: T116 U133p2; src: T116',
					  'Value for GSM85484: T144 U133p2; src: T144',
					  'Value for GSM85485: T129 U133p2; src: T129',
					  'Value for GSM85486: T143 U133p2; src: T143',
					  'Value for GSM85487: T38 U133p2; src: T38',
					  'Value for GSM85488: T123 U133p2; src: T123',
					  'Value for GSM85489: T137 U133p2; src: T137',
					  'Value for GSM85490: T130 U133p2; src: T130'],
					 ['UniRef100_Q96A05',
					  'ATP6V1E2',
					  '1',
					  '6.75015',
					  '6.19041',
					  '5.6977',
					  '5.63133',
					  '5.30341',
					  '6.11459',
					  '5.48167',
					  '5.99393',
					  '5.15695',
					  '4.85291',
					  '5.601',
					  '4.43027',
					  '6.19689',
					  '5.10544',
					  '5.68613',
					  '6.48017',
					  '5.09168',
					  '5.40445',
					  '5.60285',
					  '5.70085',
					  '6.38746',
					  '5.49871',
					  '6.63357',
					  '6.17916',
					  '6.29545',
					  '5.97648',
					  '5.76136',
					  '5.97864',
					  '7.02679',
					  '6.14417',
					  '7.23492',
					  '5.94107',
					  '8.10206',
					  '6.9611',
					  '6.73666',
					  '5.43139',
					  '5.3201',
					  '6.44781',
					  '6.81138',
					  '5.06902',
					  '7.0775',
					  '6.96432',
					  '6.1142',
					  '5.63252',
					  '6.13578',
					  '7.21813',
					  '7.17629'],
					 ['UniRef100_Q8NFU0',
					  'BEST4',
					  '1',
					  '2.54652',
					  '2.61974',
					  '2.53332',
					  '3.40082',
					  '2.55686',
					  '2.97739',
					  '2.54538',
					  '2.56575',
					  '2.77181',
					  '2.58881',
					  '2.60539',
					  '2.59489',
					  '2.60808',
					  '2.57312',
					  '2.58828',
					  '2.59499',
					  '2.7405',
					  '2.67495',
					  '2.55782',
					  '2.54596',
					  '3.26481',
					  '3.17183',
					  '2.58556',
					  '2.57986',
					  '2.57817',
					  '2.57348',
					  '2.59008',
					  '2.77253',
					  '2.56383',
					  '2.55468',
					  '2.64729',
					  '2.57003',
					  '2.51453',
					  '2.56383',
					  '2.58135',
					  '2.61224',
					  '2.59577',
					  '2.62195',
					  '4.96757',
					  '3.90375',
					  '2.63889',
					  '2.53397',
					  '2.69276',
					  '2.62064',
					  '2.64648',
					  '2.61878',
					  '2.54237'],
					 ['UniRef100_Q8WUR7',
					  'C15orf40',
					  '1',
					  '7.51158',
					  '7.30972',
					  '7.42084',
					  '7.08052',
					  '6.82374',
					  '7.25321',
					  '7.41467',
					  '6.21804',
					  '5.28595',
					  '4.27739',
					  '7.95915',
					  '6.4645',
					  '5.4844',
					  '5.27566',
					  '6.58525',
					  '7.62432',
					  '7.46162',
					  '7.31939',
					  '6.02395',
					  '5.54192',
					  '7.61163',
					  '6.27444',
					  '6.89701',
					  '5.84107',
					  '7.16801',
					  '6.72312',
					  '5.3655',
					  '6.83601',
					  '8.08747',
					  '6.08215',
					  '5.72894',
					  '6.93638',
					  '7.77051',
					  '6.33952',
					  '6.67708',
					  '6.62915',
					  '6.02168',
					  '7.69325',
					  '5.84057',
					  '6.68234',
					  '5.5305',
					  '6.6871',
					  '4.99014',
					  '4.02215',
					  '5.92098',
					  '4.78835',
					  '6.59179'],
					 ['UniRef100_Q96IS3',
					  'RAX2',
					  '1',
					  '3.03289',
					  '3.38406',
					  '3.11076',
					  '3.06687',
					  '3.12627',
					  '3.12428',
					  '3.9134',
					  '3.1256',
					  '3.29821',
					  '3.17047',
					  '3.36152',
					  '3.52685',
					  '4.95887',
					  '3.96967',
					  '3.21461',
					  '3.10371',
					  '3.16528',
					  '3.13314',
					  '3.10928',
					  '3.14432',
					  '3.46965',
					  '3.46398',
					  '3.23681',
					  '3.31994',
					  '4.21173',
					  '3.20175',
					  '3.21701',
					  '3.47599',
					  '3.15254',
					  '3.5021',
					  '3.43075',
					  '3.632',
					  '3.36308',
					  '3.14997',
					  '3.17922',
					  '3.19109',
					  '3.2069',
					  '3.25185',
					  '4.35932',
					  '3.21649',
					  '3.66005',
					  '3.39357',
					  '3.24814',
					  '3.1682',
					  '3.03673',
					  '3.03669',
					  '3.21298'],
					 ['UniRef100_P09016',
					  'HOXD4',
					  '1',
					  '2.11698',
					  '2.11811',
					  '2.11154',
					  '3.06275',
					  '2.1127',
					  '2.11579',
					  '2.99589',
					  '2.11017',
					  '3.94992',
					  '2.16318',
					  '2.10414',
					  '3.06643',
					  '3.05948',
					  '3.0262',
					  '3.75225',
					  '3.38559',
					  '2.13409',
					  '3.18378',
					  '2.02047',
					  '2.12576',
					  '2.99805',
					  '2.19295',
					  '2.13512',
					  '2.13151',
					  '2.53349',
					  '2.14399',
					  '2.16238',
					  '2.18931',
					  '2.1363',
					  '2.67654',
					  '3.10607',
					  '3.00956',
					  '2.05793',
					  '2.13949',
					  '2.15329',
					  '2.16506',
					  '2.17566',
					  '3.08369',
					  '2.17189',
					  '2.73119',
					  '2.21889',
					  '2.16253',
					  '2.25648',
					  '3.06982',
					  '3.10576',
					  '3.07942',
					  '2.12523']]



###GSE12831###

c_dirGSE8126base	=	sfle.d( c_dirGEOData,c_strGSE12831 )
c_dirGSE8126		= 	sfle.d( c_dirGSE8126base, c_strGSE8126 )
c_fileGSE8126EXP	= 	sfle.d( c_dirGSE8126, c_strGSE8126 + "_exp_metadata.txt" )
c_fileGSE8126PCL	=	sfle.d( c_dirGSE8126, c_strGSE8126 + ".pcl" ) 

c_GSE8126PCL		=	


###GDS1849### 

c_dirGDS1849base	=	sfle.d( c_dirGEOData, c_strGDS1849 )
c_dirGDS1849		=	sfle.d( c_dirGDS1849base, "GDS1849-GPL1821" )
c_fileGDS1849PKL	=	sfle.d( c_dirGDS1849, "GDS1849-GPL1821.pkl" )
c_fileGDS1849EXP	=	sfle.d( c_dirGDS1849, "GDS1849-GPL1821_exp_metadata.txt")
c_fileGDS1849PCL	=	sfle.d( c_dirGDS1849, "GDS1849-GPL1821_00raw.pcl" ) 

c_GDS1849PKL		= 	{'channels': '1',
 'conditions': '42',
 'gloss': 'Analysis of Bacteroides thetaiotaomicron (BT) from the ceca of mice on polysaccharide or simple sugar diets. BT is involved in the breakdown of plant polysaccharides. BT-colonized mice is a human gut ecosystem model. Results identify genes that may endow flexibility in adapting to dietary changes.',
 'platform': 'GPL1821',
 'pmid': '16735464',
 'taxid': '818',
 'title': 'Intestine-adapted bacterial symbiont response to polysaccharide and simple sugar diets',
 'type': 'expression profiling'}



###GSE8402###

c_dirGSE8402base	=	sfle.d( c_dirGEOData, c_strGSE8402 )
c_dirGSE8402		= 	sfle.d( c_dirGSE8402base, c_strGSE8402 )
c_fileGSE8402PCL	=	sfle.d( c_dirGSE8402, c_strGSE8402 + "_00raw.pcl" )

c_GSE8402PCL		=	['DAP1_0003',
 				'NM_000405',	
	 			'1',
 				'0.3345',
 				'0.6069',
 				'0.301',
 				'-0.2263',
 				'-0.0335',
 				'0.4686',
				'0.5545',
 				'0.539',
 				'0.8853',
 				'-0.3253',
 				'0.8535',
 				'0.3553',
 				'0.6095',
 				'0.4287',
 				'0.2953',
 				'-0.8379',
 				'0.614',
 				'0.5594',
 				'-0.3064',
 				'0.0301',
 				'0.2157',
 				'0.7615',
 				'-0.83',
 				'0.8972',
 				'-0.0167',
 				'0.6985',
 				'0.3632']


## Execute 

# test data 

#exec_test( c_dirGEO, None, [c_fileGSE10183PCL,c_GSE10183PCL] )

#exec_test( c_dirGEO, None, [c_fileGSE8126PCL,c_GSE8126PCL] )

exec_test( c_dirGEO, lambda f: [a for a in csv.reader(open(f,"r"),csv.excel_tab)][2][:30], [ c_fileGSE8402PCL, c_GSE8402PCL ] )

# test metadata 

#exec_test( c_dirGEO, lambda f: pickle.load(open(f,"r")), [c_fileGDS1849PKL, c_GDS1849PKL] ) 


#=====================================================#
#               	Bacteriome
#=====================================================#
#single dataset 

c_dirBacteriome		= 	sfle.d( arepa.path_arepa( ), "Bacteriome" )
c_dirBacteriomeData	=	sfle.d( c_dirBacteriome, sfle.c_strDirData )
c_fileBacteriomeDat	= 	sfle.d( c_dirBacteriomeData, "bacteriome.dat" )
c_fileBacteriomePKL	= 	sfle.d( c_dirBacteriomeData, "bacteriome.pkl")

c_BacteriomeDatLst	= [["UniRef90_P00561", "UniRef90_A7ZH92", "0.408408"],
							["UniRef90_P00561", "UniRef90_P00934", "0.408408"],
							["UniRef90_P00561", "UniRef90_P0A9R0", "0.408408"],
							["UniRef90_A7ZH92", "UniRef90_P00934", "0.408408"],
							["UniRef90_P00934", "UniRef90_Q0T7R6", "0.31006"]]

c_BacteriomePKL 	= {'conditions': '3888',
						 'gloss': 'Bacterial Protein Interaction Database',
						 'mapped': 'True',
						 'taxid': '83333',
						 'title': 'Bacteriome',
						 'type': 'protein interaction',
						 'url': 'http://www.compsysbio.org/bacteriome/dataset/combined_interactions.txt'}

## Execute 

# test data 
exec_test( c_dirBacteriome, None, [ c_fileBacteriomeDat, c_BacteriomeDatLst ] )

# test metadata
exec_test( c_dirBacteriome, lambda f: pickle.load( open(f) ), [c_fileBacteriomePKL, c_BacteriomePKL] ) 
 	
#=====================================================#
#                       BioGrid
#=====================================================#
#single dataset 

c_strBioGrid		= "BioGrid_taxid_224308"
c_dirBioGrid		= sfle.d( arepa.path_arepa( ), "BioGrid" )
c_dirBioGridData	= sfle.d( c_dirBioGrid, sfle.c_strDirData, c_strBioGrid )
c_fileBioGridPKL	= sfle.d( c_dirBioGridData, "BioGrid_" + "taxid_224308.pkl" )
c_fileBioGridDat	= sfle.d( c_dirBioGridData, "BioGrid_" + "taxid_224308.dat" )

c_BioGridDat		= [["UniRef90_P17903", "UniRef90_P17904", "1"]] 
c_BioGridPKL		= {'platform': 'Co-purification', 'pmid': '8144446', 'type': 'physical', 'taxid': '224308', 'mapped': True}

## Execute 

exec_test( c_dirBioGrid, None, [c_fileBioGridDat, c_BioGridDat] )
exec_test( c_dirBioGrid, lambda f: pickle.load( open(f, "r") ), [c_fileBioGridPKL, c_BioGridPKL] )

#=====================================================#
#                       IntAct
#=====================================================#
#multiple datasets

c_astrIntActIDs		= 	["IntAct_taxid_224308_pmid_16796675", "IntAct_taxid_559292_pmid_14565975", "IntAct_taxid_83333_pmid_15004283" ]
c_dirIntAct			=	sfle.d( arepa.path_arepa( ), "IntAct" ) 
c_dirIntActData		=	sfle.d( c_dirIntAct, sfle.c_strDirData )

f_dirIntActData		=	lambda x: sfle.d( c_dirIntActData, x )
f_fileIntActDAT		= 	lambda x: sfle.d( f_dirIntActData( x ), x + ".dat" )
f_fileIntActQUANT	=	lambda x: sfle.d( f_dirIntActData( x ), x + ".quant" )
f_fileIntActPKL		=	lambda x: sfle.d( f_dirIntActData( x ), x + ".pkl" ) 

c_fileIntActData1DAT	=	f_fileIntActDAT( c_astrIntActIDs[0] )
c_fileIntActData1QUANT	=	f_fileIntActQUANT( c_astrIntActIDs[0] )
c_fileIntActData1PKL	=	f_fileIntActPKL( c_astrIntActIDs[0] )

c_fileIntActData2DAT	=	f_fileIntActDAT( c_astrIntActIDs[1] )
c_fileIntActData2QUANT	=	f_fileIntActQUANT( c_astrIntActIDs[1] )
c_fileIntActData2PKL	=	f_fileIntActPKL( c_astrIntActIDs[1] )

c_fileIntActData3DAT	=	f_fileIntActDAT( c_astrIntActIDs[2] )
c_fileIntActData3QUANT	=	f_fileIntActQUANT( c_astrIntActIDs[2] )
c_fileIntActData3PKL	=	f_fileIntActPKL( c_astrIntActIDs[2] )

c_IntActData1DAT	=	[["UniRef90_A7Z4F9", "UniRef90_O34894", "1"],
						["UniRef90_P24327", "UniRef90_P37469", "1"],
						["UniRef90_P06567", "UniRef90_P37469", "1"],
						["UniRef90_P37469", "UniRef90_P45694", "1"],
						["UniRef90_O34894", "UniRef90_P17865", "1"]]

c_IntActData1PKL	=	{'mapped': True,
						 'platform': 'pull down',
						 'pmid': '16796675',
						 'taxid': '224308',
						 'type': 'physical association'}

c_IntActData2DAT	=	[["UniRef100_P53148", "UniRef100_Q12143", "1"],
						["UniRef100_P39731", "UniRef100_P40014", "1"],
						["UniRef100_P39731", "UniRef100_Q04477", "1"],
						["UniRef100_P40460", "UniRef100_P40568", "1"],
						["UniRef100_P33895", "UniRef100_P40568", "1"]]

c_IntActData2PKL	=	{'mapped': True,
						 'platform': set(['anti tag coimmunoprecipitation',
						      'tandem affinity purification']),
						 'pmid': '14565975',
						 'taxid': '559292',
						 'type': set(['physical association', 'association'])}

c_IntActData3DAT	=  [["UniRef90_A8A779", "UniRef90_P0AA27", "1"],
						["UniRef90_P0AA27", "UniRef90_P69784", "1"],
						["UniRef90_P08200", "UniRef90_P0AA27", "1"],
						["UniRef90_P0AA27", "UniRef90_A8ACN8", "1"],
						["UniRef90_A7ZUQ8", "UniRef90_P0AA27", "1"]]

c_IntActData3PKL	=	{'mapped': True,
						 'platform': 'tandem affinity purification',
						 'pmid': '15004283',
						 'taxid': '83333',
						 'type': 'association'}

#Test data 
exec_test( c_dirIntAct, None, [c_fileIntActData1DAT, c_IntActData1DAT], 
		[c_fileIntActData2DAT, c_IntActData2DAT], 
		[c_fileIntActData3DAT, c_IntActData3DAT], ) 

#Test metadata 
exec_test( c_dirIntAct, lambda f: pickle.load(open(f, "r")), 
		[c_fileIntActData1PKL, c_IntActData1PKL], 
		[c_fileIntActData2PKL, c_IntActData2PKL], 
		[c_fileIntActData3PKL, c_IntActData3PKL] )

#=====================================================#
#                       MPIDB
#=====================================================#
#multiple datasets

c_astrMPIDBIDs		= ["MPIDB_" + s for s in ["taxid_1423", "taxid_287", "taxid_562"]]

c_dirMPIDB		= sfle.d( arepa.path_arepa( ), c_strMPIDB )
c_dirMPIDBData		= sfle.d( c_dirMPIDB, sfle.c_strDirData )

c_fileMPIDBData1DAT	= sfle.d( c_dirMPIDBData,c_astrMPIDBIDs[0],c_astrMPIDBIDs[0] + ".dat" )
c_fileMPIDBData1QUANT	= sfle.d( c_dirMPIDBData,c_astrMPIDBIDs[0],c_astrMPIDBIDs[0] + ".quant" )
c_fileMPIDBData1PKL	= sfle.d( c_dirMPIDBData,c_astrMPIDBIDs[0],c_astrMPIDBIDs[0] + ".pkl" )

c_fileMPIDBData2DAT	= sfle.d( c_dirMPIDBData,c_astrMPIDBIDs[1],c_astrMPIDBIDs[1] + ".dat" )
c_fileMPIDBData2QUANT	= sfle.d( c_dirMPIDBData,c_astrMPIDBIDs[1],c_astrMPIDBIDs[1] + ".quant" )
c_fileMPIDBData2PKL	= sfle.d( c_dirMPIDBData,c_astrMPIDBIDs[1],c_astrMPIDBIDs[1] + ".pkl" )

c_fileMPIDBData3DAT	= sfle.d( c_dirMPIDBData,c_astrMPIDBIDs[2],c_astrMPIDBIDs[2] + ".dat" )
c_fileMPIDBData3QUANT	= sfle.d( c_dirMPIDBData,c_astrMPIDBIDs[2],c_astrMPIDBIDs[2] + ".quant" )
c_fileMPIDBData3PKL	= sfle.d( c_dirMPIDBData,c_astrMPIDBIDs[2],c_astrMPIDBIDs[2] + ".pkl" )

c_MPIDBData1DAT		= [["UniRef90_A7Z7A9", "UniRef90_A7Z0Q3", "1"],
						["UniRef90_O34894", "UniRef90_P54166", "1"],
						["UniRef90_P35154", "UniRef90_P35155", "1"],
						["UniRef90_P06535", "UniRef90_P06628", "1"],
						["UniRef90_A7Z7A9", "UniRef90_A7Z0M5", "1"]]

c_MPIDBData1PKL		= {'mapped': True,
					 'platform': 'two hybrid',
					 'pmid': '14993308',
					 'taxid': '1423',
					 'type': 'physical association'}

c_MPIDBData2DAT		= [["UniRef90_P35818", "UniRef90_Q51575", "1"],
						["UniRef90_Q59692", "UniRef90_Q9HZJ8", "1"],
						["UniRef90_P15275", "UniRef90_P26480", "1"],
						["UniRef90_P38107", "UniRef90_A5JJ05", "1"],
						["UniRef90_P52002", "UniRef90_P52477", "1"]]

c_MPIDBData2PKL		= {'mapped': True,
					 'platform': 'two hybrid',
					 'pmid': '11673434',
					 'taxid': '287',
					 'type': 'physical association'}

c_MPIDBData3DAT		= [["P10484",  "P10486",  "1"],
						["Q47070",  "Q47071",  "1"],
						["O52124",  "Q47184",  "1"],
						["P10485",  "P10486",  "1"],
						["P42217",  "Q47404",  "1"]]

c_MPIDBData3PKL		= {'mapped': False,
					 'platform': 'x-ray crystallography',
					 'pmid': set(['1992160', '10446231', '8491171', '9367757']),
					 'taxid': '562',
					 'type': 'physical association'}

## Execute 

#test data 
exec_test( c_dirMPIDB, None, [c_fileMPIDBData1DAT, c_MPIDBData1DAT],
		[c_fileMPIDBData2DAT, c_MPIDBData2DAT],
		[c_fileMPIDBData3DAT, c_MPIDBData3DAT] )

#test metadata 
exec_test( c_dirMPIDB, lambda f: pickle.load( open(f,"r") ), 
		[c_fileMPIDBData1PKL, c_MPIDBData1PKL],\
		[c_fileMPIDBData2PKL, c_MPIDBData2PKL],\
		[c_fileMPIDBData3PKL, c_MPIDBData3PKL] )

#=====================================================#
#                       RegulonDB 
#=====================================================#
#single dataset  

c_dirRegulon		= sfle.d( arepa.path_arepa( ), "RegulonDB" )
c_dirRegulonData	= sfle.d( c_dirRegulon, sfle.c_strDirData ) 

c_RegulonDatLst 	= [["UniRef90_P0ACK0", "UniRef90_A8AN29", "1"],
						["UniRef90_P0ACK0", "UniRef90_P50466", "1"],
						["UniRef90_P0ACK0", "UniRef90_P19926", "1"],
						["UniRef90_P0ACK0", "UniRef90_A7ZNW5", "1"],
						["UniRef90_P0ACK0", "UniRef90_P69784", "1"]]

c_RegulonPKL 		= {'title': 'RegulonDB', 'url': 'http://regulondb.ccg.unam.mx/data/network_tf_gene.txt', 
					'conditions': '4005', 'gloss': 'Escherichia coli K12 Transcriptional Network', 
					'taxid': '83333', 'mapped': 'True', 'type': 'regulatory network interaction'}

c_fileRegulonDat	= sfle.d( c_dirRegulonData, "regulondb.dat" ) 
c_fileRegulonPKL	= sfle.d( c_dirRegulonData, "regulondb.pkl")

## Execute 

#test data  
exec_test( c_dirRegulon, None, [c_fileRegulonDat, c_RegulonDatLst] ) 

#test metadata 
exec_test( c_dirRegulon, lambda f: pickle.load( open(f) ), [c_fileRegulonPKL, c_RegulonPKL] )

#=====================================================#
#                       STRING
#=====================================================#
#multiple datasets 

c_strSTRINGtaxid			= "STRING_taxid_189918_mode"
c_strSTRINGtaxidBinding		= c_strSTRINGtaxid + "_binding" 
c_strSTRINGtaxidExpression	= c_strSTRINGtaxid + "_expression"
c_strSTRINGtaxidPtmod		= c_strSTRINGtaxid + "_ptmod"

c_dirSTRING			= sfle.d( arepa.path_arepa( ), "STRING" )
c_dirSTRINGData		= sfle.d( c_dirSTRING, sfle.c_strDirData )

c_dirSTRINGtaxidBinding 	= sfle.d( c_dirSTRINGData, c_strSTRINGtaxidBinding )
c_fileSTRINGtaxidBindingDat	= sfle.d( c_dirSTRINGtaxidBinding, c_strSTRINGtaxidBinding + ".dat" )

c_dirSTRINGtaxidExpression  	= sfle.d( c_dirSTRINGData, c_strSTRINGtaxidExpression )
c_fileSTRINGtaxidExpressionDat	= sfle.d( c_dirSTRINGtaxidExpression, c_strSTRINGtaxidExpression + ".dat" )

c_dirSTRINGtaxidPtmod		= sfle.d( c_dirSTRINGData, c_strSTRINGtaxidPtmod )
c_fileSTRINGtaxidPtmodDat	= sfle.d( c_dirSTRINGtaxidPtmod, c_strSTRINGtaxidPtmod + ".dat" )

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

## Execute 

#exec_test( c_dirSTRING, None,
#		[c_fileSTRINGtaxidBindingDat, c_STRINGtaxidBindingDat],
#		[c_fileSTRINGtaxidExpressionDat, c_STRINGtaxidExpressionDat],
#		[c_fileSTRINGtaxidPtmodDat, c_STRINGtaxidPtmodDat] )

