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

test.py: 

Test script for arepa. 

Usage: python test.py [scons]

Optional flag "scons" ensures that targets are built prior to testing. 
This method of testing is not recommended. 

See the user manual for more details. 

Recommended usage: 

$ python test.py 

"""
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

print __doc__

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
GSE30000: Bascillus subtilis 

<GDSs> 
GDS2250-GPL570: Homo sapiens 
'''


c_strGDS2250		=	"GDS2250-GPL570"
c_strGSE12831		= 	"GSE12831"
c_strGSE30000		= 	"GSE30000"

c_astrMetaKeys		= 	["taxid","pmid","platform","gloss","channels","conditions"]

c_dirGEO			=	sfle.d( arepa.path_arepa( ), "GEO")
c_dirGEOData		= 	sfle.d( c_dirGEO, sfle.c_strDirData )

###GDS2250-GPL570###
 
c_dirGDS2250base	=	sfle.d( c_dirGEOData, c_strGDS2250.split("-")[0] )
c_dirGDS2250		=	sfle.d( c_dirGDS2250base, c_strGDS2250 )
c_fileGDS2250PKL	= 	sfle.d( c_dirGDS2250, c_strGDS2250 + ".pkl" )
c_fileGDS2250PCL	=	sfle.d( c_dirGDS2250, c_strGDS2250 + ".pcl" ) 


c_GDS2250PKL		=	{'channels': '1',
						 'conditions': '47',
						 'gloss': 'Analysis of sporadic basal-like cancer (BLC), BRCA-associated breast cancer, and non-BLC tumors. Sporadic BLC are phenotypically similar to BRCA1-associated cancers. Results provide insight into the molecular pathogenesis of BLC and BRCA1-associated breast cancer.',
						 'mapped': 'True',
						 'platform': 'GPL570',
						 'pmid': '20400965',
						 'taxid': '9606',
						 'title': 'Basal-like breast cancer tumors',
						 'type': 'expression profiling'}

c_GDS2250PCL		= 	[['GID',
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

c_dirGSE12831base	=	sfle.d( c_dirGEOData,c_strGSE12831 )
c_dirGSE12831		= 	sfle.d( c_dirGSE12831base, c_strGSE12831 )
c_fileGSE12831PKL	= 	sfle.d( c_dirGSE12831, c_strGSE12831 + ".pkl" )
c_fileGSE12831PCL	=	sfle.d( c_dirGSE12831, c_strGSE12831 + ".pcl" ) 

c_GSE12831PKL		=	{'Series_contact_address': '801 W. Baltimore Street, Room 619',
						 'Series_contact_city': 'Baltimore',
						 'Series_contact_country': 'USA',
						 'Series_contact_department': 'Istitute for Genome Sciences/Microbiology and Immunology',
						 'Series_contact_email': 'drasko@som.umaryland.edu',
						 'Series_contact_institute': 'University of Maryland School of Medicine',
						 'Series_contact_name': 'David,A,Rasko',
						 'Series_contact_phone': '410 706 6774',
						 'Series_contact_state': 'MD',
						 'Series_contact_zip/postal_code': '21201',
						 'Series_contributor': 'Nicola,C,Reading\nDavid,A,Rasko\nVanessa,,Sperandio',
						 'Series_geo_accession': 'GSE12831',
						 'Series_last_update_date': 'Sep 20 2012',
						 'Series_overall_design': 'Escherichia coli 8624 and the isogenic mutants in qseE, qseF and qseG are compared to determine the role that each of the genes play in regulation of the transcriptome. Single Affymetrix E. coli 2.0 Arrays are used as a starting point for this study and these results are further verified by qRT-PCR. ',
						 'Series_platform_taxid': '562',
						 'Series_relation': 'BioProject: http://www.ncbi.nlm.nih.gov/bioproject/PRJNA111139',
						 'Series_sample_id': 'GSM322121 GSM322122 GSM322123 GSM322124 ',
						 'Series_status': 'Public on Apr 05 2010',
						 'Series_submission_date': 'Sep 17 2008',
						 'Series_supplementary_file': 'ftp://ftp.ncbi.nlm.nih.gov/pub/geo/DATA/supplementary/series/GSE12831/GSE12831_RAW.tar',
						 'channels': 1,
						 'conditions': 4,
						 'curated': ['sample_name',
						  'sample_title',
						  'sample_geo_accession',
						  'sample_status',
						  'sample_submission_date',
						  'sample_last_update_date',
						  'sample_type',
						  'sample_channel_count',
						  'sample_source_name_ch1',
						  'sample_organism_ch1',
						  'sample_characteristics_ch1',
						  'sample_growth_protocol_ch1',
						  'sample_molecule_ch1',
						  'sample_extract_protocol_ch1',
						  'sample_label_ch1',
						  'sample_label_protocol_ch1',
						  'sample_label_protocol_ch1.1',
						  'sample_taxid_ch1',
						  'sample_hyb_protocol',
						  'sample_hyb_protocol.1',
						  'sample_scan_protocol',
						  'sample_scan_protocol.1',
						  'sample_description',
						  'sample_description.1',
						  'sample_data_processing',
						  'sample_platform_id',
						  'sample_contact_name',
						  'sample_contact_email',
						  'sample_contact_phone',
						  'sample_contact_department',
						  'sample_contact_institute',
						  'sample_contact_address',
						  'sample_contact_city',
						  'sample_contact_state',
						  'sample_contact_zip/postal_code',
						  'sample_contact_country',
						  'sample_supplementary_file',
						  'sample_supplementary_file.1',
						  'sample_data_row_count'],
						 'gloss': 'Escherichia coli 8624 and the isogenic mutants in qseE, qseF and qseG are compared to determine the role that each of the genes play in regulation of the transcriptome.  These results are verified by qRT-PCR and reveal the important role of this three-component signaling system.',
						 'mapped': 'True',
						 'platform': 'GPL3154',
						 'pmid': '19289831\n20056703',
						 'sample_channel_count': ['1', '1', '1', '1'],
						 'sample_characteristics_ch1': ['Escherichia coli 8624 qseE deletion mutant grown in DMEM',
						  'strain: Escherichia coli 8624',
						  'Escherichia coli 8624 qseG deletion mutant grown in DMEM',
						  'Escherichia coli 8624 grown in DMEM'],
						 'sample_contact_address': ['801 W. Baltimore Street, Room 619',
						  '801 W. Baltimore Street, Room 619',
						  '801 W. Baltimore Street, Room 619',
						  '801 W. Baltimore Street, Room 619'],
						 'sample_contact_city': ['Baltimore', 'Baltimore', 'Baltimore', 'Baltimore'],
						 'sample_contact_country': ['USA', 'USA', 'USA', 'USA'],
						 'sample_contact_department': ['Istitute for Genome Sciences/Microbiology and Immunology',
						  'Istitute for Genome Sciences/Microbiology and Immunology',
						  'Istitute for Genome Sciences/Microbiology and Immunology',
						  'Istitute for Genome Sciences/Microbiology and Immunology'],
						 'sample_contact_email': ['drasko@som.umaryland.edu',
						  'drasko@som.umaryland.edu',
						  'drasko@som.umaryland.edu',
						  'drasko@som.umaryland.edu'],
						 'sample_contact_institute': ['University of Maryland School of Medicine',
						  'University of Maryland School of Medicine',
						  'University of Maryland School of Medicine',
						  'University of Maryland School of Medicine'],
						 'sample_contact_name': ['David,A,Rasko',
						  'David,A,Rasko',
						  'David,A,Rasko',
						  'David,A,Rasko'],
						 'sample_contact_phone': ['410 706 6774',
						  '410 706 6774',
						  '410 706 6774',
						  '410 706 6774'],
						 'sample_contact_state': ['MD', 'MD', 'MD', 'MD'],
						 'sample_contact_zip/postal_code': ['21201', '21201', '21201', '21201'],
						 'sample_data_processing': ['Data has not been processed other than those protocols within GCOSv1.4',
						  'Data has not been processed other than those protocols within GCOSv1.4',
						  'Data has not been processed other than those protocols within GCOSv1.4',
						  'Data has not been processed other than those protocols within GCOSv1.4'],
						 'sample_data_row_count': ['10208', '10208', '10208', '10208'],
						 'sample_description': ['All protocols were done according to manufacturers specifications:',
						  'All protocols were done according to manufacturers specifications:',
						  'All protocols were done according to manufacturers specifications:',
						  "All protocols were done according to manufacturer's specifications:"],
						 'sample_description.1': ['http://www.affymetrix.com/support/technical/manual/expression_manual.affx',
						  'http://www.affymetrix.com/support/technical/manual/expression_manual.affx',
						  'http://www.affymetrix.com/support/technical/manual/expression_manual.affx',
						  'http://www.affymetrix.com/support/technical/manual/expression_manual.affx'],
						 'sample_extract_protocol_ch1': ['Ambion RiboPure RNA Isolation ',
						  'Ambion RiboPure RNA Isolation ',
						  'Ambion RiboPure RNA Isolation ',
						  'Ambion RiboPure RNA Isolation'],
						 'sample_geo_accession': ['GSM322121', 'GSM322122', 'GSM322123', 'GSM322124'],
						 'sample_growth_protocol_ch1': ['Escherichia coli 8624 qseE deletion mutant grown in DMEM media',
						  'Escherichia coli 8624 qseF deletion mutant grown in DMEM media',
						  'Escherichia coli 8624 qseG deletion mutant grown in DMEM media',
						  'Escherichia coli 8624 grown in DMEM'],
						 'sample_hyb_protocol': ['All protocols were done according to manufacturers specifications:',
						  'All protocols were done according to manufacturers specifications:',
						  'All protocols were done according to manufacturers specifications:',
						  "All protocols were done according to manufacturer's specifications:"],
						 'sample_hyb_protocol.1': ['http://www.affymetrix.com/support/technical/manual/expression_manual.affx',
						  'http://www.affymetrix.com/support/technical/manual/expression_manual.affx',
						  'http://www.affymetrix.com/support/technical/manual/expression_manual.affx',
						  'http://www.affymetrix.com/support/technical/manual/expression_manual.affx'],
						 'sample_label_ch1': ['biotin', 'biotin', 'biotin', 'biotin'],
						 'sample_label_protocol_ch1': ['All protocols were done according to manufacturers specifications:',
						  'All protocols were done according to manufacturers specifications:',
						  'All protocols were done according to manufacturers specifications:',
						  "All protocols were done according to manufacturer's specifications:"],
						 'sample_label_protocol_ch1.1': ['http://www.affymetrix.com/support/technical/manual/expression_manual.affx',
						  'http://www.affymetrix.com/support/technical/manual/expression_manual.affx',
						  'http://www.affymetrix.com/support/technical/manual/expression_manual.affx',
						  'http://www.affymetrix.com/support/technical/manual/expression_manual.affx'],
						 'sample_last_update_date': ['Apr 05 2010',
						  'Sep 15 2009',
						  'Apr 05 2010',
						  'Nov 02 2009'],
						 'sample_molecule_ch1': ['total RNA', 'total RNA', 'total RNA', 'total RNA'],
						 'sample_name': ['GSM322121', 'GSM322122', 'GSM322123', 'GSM322124'],
						 'sample_organism_ch1': ['Escherichia coli',
						  'Escherichia coli',
						  'Escherichia coli',
						  'Escherichia coli'],
						 'sample_platform_id': ['GPL3154', 'GPL3154', 'GPL3154', 'GPL3154'],
						 'sample_scan_protocol': ['All protocols were done according to manufacturers specifications:',
						  'All protocols were done according to manufacturers specifications:',
						  'All protocols were done according to manufacturers specifications:',
						  "All protocols were done according to manufacturer's specifications:"],
						 'sample_scan_protocol.1': ['http://www.affymetrix.com/support/technical/manual/expression_manual.affx',
						  'http://www.affymetrix.com/support/technical/manual/expression_manual.affx',
						  'http://www.affymetrix.com/support/technical/manual/expression_manual.affx',
						  'http://www.affymetrix.com/support/technical/manual/expression_manual.affx'],
						 'sample_source_name_ch1': ['Escherichia coli 8624 qseE deletion mutant',
						  'Escherichia coli 8624 qseF deletion mutant',
						  'Escherichia coli 8624 qseG deletion mutant grown in DMEM',
						  'E. coli 8624'],
						 'sample_status': ['Public on Apr 05 2010',
						  'Public on Sep 15 2009',
						  'Public on Apr 05 2010',
						  'Public on Nov 02 2009'],
						 'sample_submission_date': ['Sep 17 2008',
						  'Sep 17 2008',
						  'Sep 17 2008',
						  'Sep 17 2008'],
						 'sample_supplementary_file': ['ftp://ftp.ncbi.nlm.nih.gov/pub/geo/DATA/supplementary/samples/GSM322nnn/GSM322121/GSM322121.CEL.gz',
						  'ftp://ftp.ncbi.nlm.nih.gov/pub/geo/DATA/supplementary/samples/GSM322nnn/GSM322122/GSM322122.CEL.gz',
						  'ftp://ftp.ncbi.nlm.nih.gov/pub/geo/DATA/supplementary/samples/GSM322nnn/GSM322123/GSM322123.CEL.gz',
						  'ftp://ftp.ncbi.nlm.nih.gov/pub/geo/DATA/supplementary/samples/GSM322nnn/GSM322124/GSM322124.CEL.gz'],
						 'sample_supplementary_file.1': ['ftp://ftp.ncbi.nlm.nih.gov/pub/geo/DATA/supplementary/samples/GSM322nnn/GSM322121/GSM322121.CHP.gz',
						  'ftp://ftp.ncbi.nlm.nih.gov/pub/geo/DATA/supplementary/samples/GSM322nnn/GSM322122/GSM322122.CHP.gz',
						  'ftp://ftp.ncbi.nlm.nih.gov/pub/geo/DATA/supplementary/samples/GSM322nnn/GSM322123/GSM322123.CHP.gz',
						  'ftp://ftp.ncbi.nlm.nih.gov/pub/geo/DATA/supplementary/samples/GSM322nnn/GSM322124/GSM322124.CHP.gz'],
						 'sample_taxid_ch1': ['562', '562', '562', '562'],
						 'sample_title': ['E. coli 8624 qseE deletion mutant',
						  'E. coli 8624 qseF deletion mutant',
						  'E. coli 8624 qseG deletion mutant',
						  'E. coli 8624 WT'],
						 'sample_type': ['RNA', 'RNA', 'RNA', 'RNA'],
						 'taxid': '562',
						 'title': 'The role of qseE, qseF and qseG in the regulation of EHEC virulence',
						 'type': 'Expression profiling by array'}

c_GSE12831PCL = [['GID',
				  'NAME',
				  'GWEIGHT',
				  'GSM322121: E. coli 8624 qseE deletion mutant',
				  'GSM322122: E. coli 8624 qseF deletion mutant',
				  'GSM322123: E. coli 8624 qseG deletion mutant',
				  'GSM322124: E. coli 8624 WT'],
				 ['UniRef90_P24202',
				  'b4351',
				  '1',
				  '0.341610085413718',
				  '4.89218699400604',
				  '5.19074521832963',
				  '3.74250211943652'],
				 ['UniRef90_P21865',
				  'c0780',
				  '1',
				  '6.25025482843215',
				  '5.29922267426246',
				  '5.58226394211173',
				  '6.12090760937409'],
				 ['UniRef90_P36938',
				  'c0775',
				  '1',
				  '8.71106120698501',
				  '8.46242865339581',
				  '7.21965256510381',
				  '7.88277753161446'],
				 ['UniRef90_P41052',
				  'c3255',
				  '1',
				  '7.97116989928161',
				  '7.72564573700983',
				  '7.79291390210949',
				  '7.21004786742918'],
				 ['UniRef90_C4ZQX0',
				  'c3801',
				  '1',
				  '4.44660031794549',
				  '6.83009049617508',
				  '5.1816472362885',
				  '6.8120489175958']]

###GSE30000### 

c_dirGSE30000base	=	sfle.d( c_dirGEOData, c_strGSE30000 )
c_dirGSE30000		=	sfle.d( c_dirGSE30000base, c_strGSE30000 )
c_fileGSE30000PKL	=	sfle.d( c_dirGSE30000, c_strGSE30000 + ".pkl" )
c_fileGSE30000PCL	=	sfle.d( c_dirGSE30000, c_strGSE30000 + ".pcl" ) 

c_GSE30000PKL		=	{'Series_contact_address': '372 Wing Hall',
						 'Series_contact_city': 'Ithaca',
						 'Series_contact_country': 'USA',
						 'Series_contact_department': 'Microbiology',
						 'Series_contact_email': 'jdh9@cornell.edu',
						 'Series_contact_fax': '607 255 3904',
						 'Series_contact_institute': 'Cornell University',
						 'Series_contact_name': 'John,D.,Helmann',
						 'Series_contact_phone': '607 255 6570',
						 'Series_contact_state': 'NY',
						 'Series_contact_zip/postal_code': '14853',
						 'Series_contributor': 'Anna-Barbara,,Hachmann\nJohn,D,Helmann',
						 'Series_geo_accession': 'GSE30000',
						 'Series_last_update_date': 'Mar 23 2012',
						 'Series_overall_design': 'Bacillus subtilis 168, WT (-DAP) vs. DapR1 (-DAP), WT (+DAP) vs. DapR1 (+DAP), DapR1 (+DAP) vs. DapR1 (-DAP). Each experiment was conducted at least twice using two independent total RNA preparations. For daptomycin untreated comparison between 168 WT and DapR1 mutant, DapR1 was labeled with Alexa Fluor 647 and WT was labeled with Alexa Fluor 555. For daptomycin treated experiments between WT and DapR1, DapR1 was labeled with Alexa Fluor 647 and WT  with Alexa Fluor 555. For treated vs. untreated DapR1, the DAP treated samples were labeled with Alexa Fluor 647 and the untreated with Alexa Fluor 555. For dye swap, untreated DapR1 was labeled with Alexa Fluor 647 and DAP treated with Alexa Fluor 555.',
						 'Series_platform_taxid': '1423',
						 'Series_relation': 'BioProject: http://www.ncbi.nlm.nih.gov/bioproject/PRJNA140751',
						 'Series_sample_id': 'GSM742494 GSM742495 GSM742496 GSM742497 GSM742498 GSM742499 GSM742500 GSM742501 ',
						 'Series_status': 'Public on Jun 16 2011',
						 'Series_submission_date': 'Jun 15 2011',
						 'Series_supplementary_file': 'ftp://ftp.ncbi.nlm.nih.gov/pub/geo/DATA/supplementary/series/GSE30000/GSE30000_RAW.tar',
						 'channels': 2,
						 'conditions': 8,
						 'curated': ['sample_name',
						  'sample_title',
						  'sample_geo_accession',
						  'sample_status',
						  'sample_submission_date',
						  'sample_last_update_date',
						  'sample_type',
						  'sample_channel_count',
						  'sample_source_name_ch1',
						  'sample_organism_ch1',
						  'sample_characteristics_ch1',
						  'sample_characteristics_ch1.1',
						  'sample_molecule_ch1',
						  'sample_extract_protocol_ch1',
						  'sample_label_ch1',
						  'sample_label_protocol_ch1',
						  'sample_taxid_ch1',
						  'sample_source_name_ch2',
						  'sample_organism_ch2',
						  'sample_characteristics_ch2',
						  'sample_characteristics_ch2.1',
						  'sample_molecule_ch2',
						  'sample_extract_protocol_ch2',
						  'sample_label_ch2',
						  'sample_label_protocol_ch2',
						  'sample_taxid_ch2',
						  'sample_hyb_protocol',
						  'sample_scan_protocol',
						  'sample_scan_protocol.1',
						  'sample_description',
						  'sample_data_processing',
						  'sample_platform_id',
						  'sample_contact_name',
						  'sample_contact_email',
						  'sample_contact_phone',
						  'sample_contact_fax',
						  'sample_contact_department',
						  'sample_contact_institute',
						  'sample_contact_address',
						  'sample_contact_city',
						  'sample_contact_state',
						  'sample_contact_zip/postal_code',
						  'sample_contact_country',
						  'sample_supplementary_file',
						  'sample_data_row_count'],
						 'gloss': 'Transcriptional response of Bacillus subtilis to daptomycin in wild-type and in a daptomycin resistant mutant.',
						 'mapped': 'True',
						 'platform': 'GPL7420',
						 'pmid': '21709092',
						 'sample_channel_count': ['2', '2', '2', '2', '2', '2', '2', '2'],
						 'sample_characteristics_ch1': ['strain: 168',
						  'strain: 168',
						  'strain: 168',
						  'strain: 168',
						  'strain: 168',
						  'strain: 168',
						  'strain: 168',
						  'strain: 168'],
						 'sample_characteristics_ch1.1': ['genotype/variation: wild-type',
						  'genotype/variation: wild-type',
						  'genotype/variation: wild-type',
						  'genotype/variation: wild-type',
						  'genotype/variation: DapR1 (daptomycin resistant mutant)',
						  'genotype/variation: DapR1 (daptomycin resistant mutant)',
						  'genotype/variation: DapR1 (daptomycin resistant mutant)',
						  'genotype/variation: DapR1 (daptomycin resistant mutant)'],
						 'sample_characteristics_ch2': ['strain: 168',
						  'strain: 168',
						  'strain: 168',
						  'strain: 168',
						  'strain: 168',
						  'strain: 168',
						  'strain: 168',
						  'strain: 168'],
						 'sample_characteristics_ch2.1': ['genotype/variation: DapR1 (daptomycin resistant mutant)',
						  'genotype/variation: DapR1 (daptomycin resistant mutant)',
						  'genotype/variation: DapR1 (daptomycin resistant mutant)',
						  'genotype/variation: DapR1 (daptomycin resistant mutant)',
						  'genotype/variation: DapR1 (daptomycin resistant mutant)',
						  'genotype/variation: DapR1 (daptomycin resistant mutant)',
						  'genotype/variation: DapR1 (daptomycin resistant mutant)',
						  'genotype/variation: DapR1 (daptomycin resistant mutant)'],
						 'sample_contact_address': ['372 Wing Hall',
						  '372 Wing Hall',
						  '372 Wing Hall',
						  '372 Wing Hall',
						  '372 Wing Hall',
						  '372 Wing Hall',
						  '372 Wing Hall',
						  '372 Wing Hall'],
						 'sample_contact_city': ['Ithaca',
						  'Ithaca',
						  'Ithaca',
						  'Ithaca',
						  'Ithaca',
						  'Ithaca',
						  'Ithaca',
						  'Ithaca'],
						 'sample_contact_country': ['USA',
						  'USA',
						  'USA',
						  'USA',
						  'USA',
						  'USA',
						  'USA',
						  'USA'],
						 'sample_contact_department': ['Microbiology',
						  'Microbiology',
						  'Microbiology',
						  'Microbiology',
						  'Microbiology',
						  'Microbiology',
						  'Microbiology',
						  'Microbiology'],
						 'sample_contact_email': ['jdh9@cornell.edu',
						  'jdh9@cornell.edu',
						  'jdh9@cornell.edu',
						  'jdh9@cornell.edu',
						  'jdh9@cornell.edu',
						  'jdh9@cornell.edu',
						  'jdh9@cornell.edu',
						  'jdh9@cornell.edu'],
						 'sample_contact_fax': ['607 255 3904',
						  '607 255 3904',
						  '607 255 3904',
						  '607 255 3904',
						  '607 255 3904',
						  '607 255 3904',
						  '607 255 3904',
						  '607 255 3904'],
						 'sample_contact_institute': ['Cornell University',
						  'Cornell University',
						  'Cornell University',
						  'Cornell University',
						  'Cornell University',
						  'Cornell University',
						  'Cornell University',
						  'Cornell University'],
						 'sample_contact_name': ['John,D.,Helmann',
						  'John,D.,Helmann',
						  'John,D.,Helmann',
						  'John,D.,Helmann',
						  'John,D.,Helmann',
						  'John,D.,Helmann',
						  'John,D.,Helmann',
						  'John,D.,Helmann'],
						 'sample_contact_phone': ['607 255 6570',
						  '607 255 6570',
						  '607 255 6570',
						  '607 255 6570',
						  '607 255 6570',
						  '607 255 6570',
						  '607 255 6570',
						  '607 255 6570'],
						 'sample_contact_state': ['NY', 'NY', 'NY', 'NY', 'NY', 'NY', 'NY', 'NY'],
						 'sample_contact_zip/postal_code': ['14853',
						  '14853',
						  '14853',
						  '14853',
						  '14853',
						  '14853',
						  '14853',
						  '14853'],
						 'sample_data_processing': ['Red/green fluorescence intensity values were normalized  using the GenePix Pro 6.0 software package such that the ratio of medians of all features was equal to 1. Fold changes equal to average of daptomycin treated samples  (635) / average of untreated samples (532) or average of wild type (532) / average of mutants (635) excluding dye swap experiment which was average of wild type (635) / average of mutant (532). Ave represents the average of medians for duplicate spots (minus median of background).',
						  'Red/green fluorescence intensity values were normalized  using the GenePix Pro 6.0 software package such that the ratio of medians of all features was equal to 1. Fold changes equal to average of daptomycin treated samples  (635) / average of untreated samples (532) or average of wild type (532) / average of mutants (635) excluding dye swap experiment which was average of wild type (635) / average of mutant (532). Ave represents the average of medians for duplicate spots (minus median of background).',
						  'Red/green fluorescence intensity values were normalized  using the GenePix Pro 6.0 software package such that the ratio of medians of all features was equal to 1. Fold changes equal to average of daptomycin treated samples  (635) / average of untreated samples (532) or average of wild type (532) / average of mutants (635) excluding dye swap experiment which was average of wild type (635) / average of mutant (532). Ave represents the average of medians for duplicate spots (minus median of background).',
						  'Red/green fluorescence intensity values were normalized  using the GenePix Pro 6.0 software package such that the ratio of medians of all features was equal to 1. Fold changes equal to average of daptomycin treated samples  (635) / average of untreated samples (532) or average of wild type (532) / average of mutants (635) excluding dye swap experiment which was average of wild type (635) / average of mutant (532). Ave represents the average of medians for duplicate spots (minus median of background).',
						  'Red/green fluorescence intensity values were normalized  using the GenePix Pro 6.0 software package such that the ratio of medians of all features was equal to 1. Fold changes equal to average of daptomycin treated samples  (635) / average of untreated samples (532) or average of wild type (532) / average of mutants (635) excluding dye swap experiment which was average of wild type (635) / average of mutant (532). Ave represents the average of medians for duplicate spots (minus median of background).',
						  'Red/green fluorescence intensity values were normalized  using the GenePix Pro 6.0 software package such that the ratio of medians of all features was equal to 1. Fold changes equal to average of daptomycin treated samples  (635) / average of untreated samples (532) or average of wild type (532) / average of mutants (635) excluding dye swap experiment which was average of wild type (635) / average of mutant (532). Ave represents the average of medians for duplicate spots (minus median of background).',
						  'Red/green fluorescence intensity values were normalized  using the GenePix Pro 6.0 software package such that the ratio of medians of all features was equal to 1. Fold changes equal to average of daptomycin treated samples  (635) / average of untreated samples (532) or average of wild type (532) / average of mutants (635) excluding dye swap experiment which was average of wild type (635) / average of mutant (532). Ave represents the average of medians for duplicate spots (minus median of background).',
						  'Red/green fluorescence intensity values were normalized  using the GenePix Pro 6.0 software package such that the ratio of medians of all features was equal to 1. Fold changes equal to average of daptomycin treated samples  (635) / average of untreated samples (532) or average of wild type (532) / average of mutants (635) excluding dye swap experiment which was average of wild type (635) / average of mutant (532). Ave represents the average of medians for duplicate spots (minus median of background).'],
						 'sample_data_row_count': ['4116',
						  '4116',
						  '4116',
						  '4116',
						  '4116',
						  '4116',
						  '4116',
						  '4116'],
						 'sample_description': ['Biological replicate 1 of 2 of Bacillus subtilis compared to daptomycin resistant mutant DapR1.',
						  'Biological replicate 2 of 2 of Bacillus subtilis compared to daptomycin resistant mutant DapR1.',
						  'Biological replicate 1 of 2 of Bacillus subtilis compared to daptomycin resistant mutant DapR1 with daptomycin treatment.',
						  'Biological replicate 2 of 2 of Bacillus subtilis compared to daptomycin resistant mutant DapR1 with daptomycin treatment.',
						  'Biological replicate 1 of 4 of daptomycin resistant mutant DapR1 with and without daptomycin treatment.',
						  'Biological replicate 2 of 4 of daptomycin resistant mutant DapR1 with and without daptomycin treatment.',
						  'Biological replicate 3 of 4 of daptomycin resistant mutant DapR1 with and without daptomycin treatment.',
						  'Biological replicate 4 of 4 of daptomycin resistant mutant DapR1 with and without daptomycin treatment.'],
						 'sample_extract_protocol_ch1': ['Total RNA was isolated from Bacillus subtilis 168 and DapR1 grown to mid-log phase (OD600 of 0.4) using the RNeasy Mini Kit (Qiagen Sciences, Maryland). After DNase treatment with TURBO DNA-freeTM (Ambion), RNA concentrations were quantified using a NanoDrop spectrophotometer (NanoDrop Tech. Inc., Wilmington, DE). cDNA was synthesized from 20 \xc2\xb5g total RNA and differentially labeled according to manufacturer\xe2\x80\x99s instructions with the SuperScriptTM Plus Indirect cDNA labeling System (Invitrogen). Before and after indirect labeling with Alexa Fluor 555 or Alexa Fluor 647 (at least 3 h at room temperature) cDNA was purified using the Qiagen MinElute PCR Purification Kit (Qiagen, Maryland) and quantified via NanoDrop.',
						  'Total RNA was isolated from Bacillus subtilis 168 and DapR1 grown to mid-log phase (OD600 of 0.4) using the RNeasy Mini Kit (Qiagen Sciences, Maryland). After DNase treatment with TURBO DNA-freeTM (Ambion), RNA concentrations were quantified using a NanoDrop spectrophotometer (NanoDrop Tech. Inc., Wilmington, DE). cDNA was synthesized from 20 \xc2\xb5g total RNA and differentially labeled according to manufacturer\xe2\x80\x99s instructions with the SuperScriptTM Plus Indirect cDNA labeling System (Invitrogen). Before and after indirect labeling with Alexa Fluor 555 or Alexa Fluor 647 (at least 3 h at room temperature) cDNA was purified using the Qiagen MinElute PCR Purification Kit (Qiagen, Maryland) and quantified via NanoDrop.',
						  'Total RNA was isolated from Bacillus subtilis 168 and DapR1 grown to mid-log phase (OD600 of 0.4) using the RNeasy Mini Kit (Qiagen Sciences, Maryland). After DNase treatment with TURBO DNA-freeTM (Ambion), RNA concentrations were quantified using a NanoDrop spectrophotometer (NanoDrop Tech. Inc., Wilmington, DE). cDNA was synthesized from 20 \xc2\xb5g total RNA and differentially labeled according to manufacturer\xe2\x80\x99s instructions with the SuperScriptTM Plus Indirect cDNA labeling System (Invitrogen). Before and after indirect labeling with Alexa Fluor 555 or Alexa Fluor 647 (at least 3 h at room temperature) cDNA was purified using the Qiagen MinElute PCR Purification Kit (Qiagen, Maryland) and quantified via NanoDrop.',
						  'Total RNA was isolated from Bacillus subtilis 168 and DapR1 grown to mid-log phase (OD600 of 0.4) using the RNeasy Mini Kit (Qiagen Sciences, Maryland). After DNase treatment with TURBO DNA-freeTM (Ambion), RNA concentrations were quantified using a NanoDrop spectrophotometer (NanoDrop Tech. Inc., Wilmington, DE). cDNA was synthesized from 20 \xc2\xb5g total RNA and differentially labeled according to manufacturer\xe2\x80\x99s instructions with the SuperScriptTM Plus Indirect cDNA labeling System (Invitrogen). Before and after indirect labeling with Alexa Fluor 555 or Alexa Fluor 647 (at least 3 h at room temperature) cDNA was purified using the Qiagen MinElute PCR Purification Kit (Qiagen, Maryland) and quantified via NanoDrop.',
						  'Total RNA was isolated from Bacillus subtilis 168 and DapR1 grown to mid-log phase (OD600 of 0.4) using the RNeasy Mini Kit (Qiagen Sciences, Maryland). After DNase treatment with TURBO DNA-freeTM (Ambion), RNA concentrations were quantified using a NanoDrop spectrophotometer (NanoDrop Tech. Inc., Wilmington, DE). cDNA was synthesized from 20 \xc2\xb5g total RNA and differentially labeled according to manufacturer\xe2\x80\x99s instructions with the SuperScriptTM Plus Indirect cDNA labeling System (Invitrogen). Before and after indirect labeling with Alexa Fluor 555 or Alexa Fluor 647 (at least 3 h at room temperature) cDNA was purified using the Qiagen MinElute PCR Purification Kit (Qiagen, Maryland) and quantified via NanoDrop.',
						  'Total RNA was isolated from Bacillus subtilis 168 and DapR1 grown to mid-log phase (OD600 of 0.4) using the RNeasy Mini Kit (Qiagen Sciences, Maryland). After DNase treatment with TURBO DNA-freeTM (Ambion), RNA concentrations were quantified using a NanoDrop spectrophotometer (NanoDrop Tech. Inc., Wilmington, DE). cDNA was synthesized from 20 \xc2\xb5g total RNA and differentially labeled according to manufacturer\xe2\x80\x99s instructions with the SuperScriptTM Plus Indirect cDNA labeling System (Invitrogen). Before and after indirect labeling with Alexa Fluor 555 or Alexa Fluor 647 (at least 3 h at room temperature) cDNA was purified using the Qiagen MinElute PCR Purification Kit (Qiagen, Maryland) and quantified via NanoDrop.',
						  'Total RNA was isolated from Bacillus subtilis 168 and DapR1 grown to mid-log phase (OD600 of 0.4) using the RNeasy Mini Kit (Qiagen Sciences, Maryland). After DNase treatment with TURBO DNA-freeTM (Ambion), RNA concentrations were quantified using a NanoDrop spectrophotometer (NanoDrop Tech. Inc., Wilmington, DE). cDNA was synthesized from 20 \xc2\xb5g total RNA and differentially labeled according to manufacturer\xe2\x80\x99s instructions with the SuperScriptTM Plus Indirect cDNA labeling System (Invitrogen). Before and after indirect labeling with Alexa Fluor 555 or Alexa Fluor 647 (at least 3 h at room temperature) cDNA was purified using the Qiagen MinElute PCR Purification Kit (Qiagen, Maryland) and quantified via NanoDrop.',
						  'Total RNA was isolated from Bacillus subtilis 168 and DapR1 grown to mid-log phase (OD600 of 0.4) using the RNeasy Mini Kit (Qiagen Sciences, Maryland). After DNase treatment with TURBO DNA-freeTM (Ambion), RNA concentrations were quantified using a NanoDrop spectrophotometer (NanoDrop Tech. Inc., Wilmington, DE). cDNA was synthesized from 20 \xc2\xb5g total RNA and differentially labeled according to manufacturer\xe2\x80\x99s instructions with the SuperScriptTM Plus Indirect cDNA labeling System (Invitrogen). Before and after indirect labeling with Alexa Fluor 555 or Alexa Fluor 647 (at least 3 h at room temperature) cDNA was purified using the Qiagen MinElute PCR Purification Kit (Qiagen, Maryland) and quantified via NanoDrop.'],
						 'sample_extract_protocol_ch2': ['Total RNA was isolated from Bacillus subtilis 168 and DapR1 grown to mid-log phase (OD600 of 0.4) using the RNeasy Mini Kit (Qiagen Sciences, Maryland). After DNase treatment with TURBO DNA-freeTM (Ambion), RNA concentrations were quantified using a NanoDrop spectrophotometer (NanoDrop Tech. Inc., Wilmington, DE). cDNA was synthesized from 20 \xc2\xb5g total RNA and differentially labeled according to manufacturer\xe2\x80\x99s instructions with the SuperScriptTM Plus Indirect cDNA labeling System (Invitrogen). Before and after indirect labeling with Alexa Fluor 555 or Alexa Fluor 647 (at least 3 h at room temperature) cDNA was purified using the Qiagen MinElute PCR Purification Kit (Qiagen, Maryland) and quantified via NanoDrop.',
						  'Total RNA was isolated from Bacillus subtilis 168 and DapR1 grown to mid-log phase (OD600 of 0.4) using the RNeasy Mini Kit (Qiagen Sciences, Maryland). After DNase treatment with TURBO DNA-freeTM (Ambion), RNA concentrations were quantified using a NanoDrop spectrophotometer (NanoDrop Tech. Inc., Wilmington, DE). cDNA was synthesized from 20 \xc2\xb5g total RNA and differentially labeled according to manufacturer\xe2\x80\x99s instructions with the SuperScriptTM Plus Indirect cDNA labeling System (Invitrogen). Before and after indirect labeling with Alexa Fluor 555 or Alexa Fluor 647 (at least 3 h at room temperature) cDNA was purified using the Qiagen MinElute PCR Purification Kit (Qiagen, Maryland) and quantified via NanoDrop.',
						  'Total RNA was isolated from Bacillus subtilis 168 and DapR1 grown to mid-log phase (OD600 of 0.4) using the RNeasy Mini Kit (Qiagen Sciences, Maryland). After DNase treatment with TURBO DNA-freeTM (Ambion), RNA concentrations were quantified using a NanoDrop spectrophotometer (NanoDrop Tech. Inc., Wilmington, DE). cDNA was synthesized from 20 \xc2\xb5g total RNA and differentially labeled according to manufacturer\xe2\x80\x99s instructions with the SuperScriptTM Plus Indirect cDNA labeling System (Invitrogen). Before and after indirect labeling with Alexa Fluor 555 or Alexa Fluor 647 (at least 3 h at room temperature) cDNA was purified using the Qiagen MinElute PCR Purification Kit (Qiagen, Maryland) and quantified via NanoDrop.',
						  'Total RNA was isolated from Bacillus subtilis 168 and DapR1 grown to mid-log phase (OD600 of 0.4) using the RNeasy Mini Kit (Qiagen Sciences, Maryland). After DNase treatment with TURBO DNA-freeTM (Ambion), RNA concentrations were quantified using a NanoDrop spectrophotometer (NanoDrop Tech. Inc., Wilmington, DE). cDNA was synthesized from 20 \xc2\xb5g total RNA and differentially labeled according to manufacturer\xe2\x80\x99s instructions with the SuperScriptTM Plus Indirect cDNA labeling System (Invitrogen). Before and after indirect labeling with Alexa Fluor 555 or Alexa Fluor 647 (at least 3 h at room temperature) cDNA was purified using the Qiagen MinElute PCR Purification Kit (Qiagen, Maryland) and quantified via NanoDrop.',
						  'Total RNA was isolated from Bacillus subtilis 168 and DapR1 grown to mid-log phase (OD600 of 0.4) using the RNeasy Mini Kit (Qiagen Sciences, Maryland). After DNase treatment with TURBO DNA-freeTM (Ambion), RNA concentrations were quantified using a NanoDrop spectrophotometer (NanoDrop Tech. Inc., Wilmington, DE). cDNA was synthesized from 20 \xc2\xb5g total RNA and differentially labeled according to manufacturer\xe2\x80\x99s instructions with the SuperScriptTM Plus Indirect cDNA labeling System (Invitrogen). Before and after indirect labeling with Alexa Fluor 555 or Alexa Fluor 647 (at least 3 h at room temperature) cDNA was purified using the Qiagen MinElute PCR Purification Kit (Qiagen, Maryland) and quantified via NanoDrop.',
						  'Total RNA was isolated from Bacillus subtilis 168 and DapR1 grown to mid-log phase (OD600 of 0.4) using the RNeasy Mini Kit (Qiagen Sciences, Maryland). After DNase treatment with TURBO DNA-freeTM (Ambion), RNA concentrations were quantified using a NanoDrop spectrophotometer (NanoDrop Tech. Inc., Wilmington, DE). cDNA was synthesized from 20 \xc2\xb5g total RNA and differentially labeled according to manufacturer\xe2\x80\x99s instructions with the SuperScriptTM Plus Indirect cDNA labeling System (Invitrogen). Before and after indirect labeling with Alexa Fluor 555 or Alexa Fluor 647 (at least 3 h at room temperature) cDNA was purified using the Qiagen MinElute PCR Purification Kit (Qiagen, Maryland) and quantified via NanoDrop.',
						  'Total RNA was isolated from Bacillus subtilis 168 and DapR1 grown to mid-log phase (OD600 of 0.4) using the RNeasy Mini Kit (Qiagen Sciences, Maryland). After DNase treatment with TURBO DNA-freeTM (Ambion), RNA concentrations were quantified using a NanoDrop spectrophotometer (NanoDrop Tech. Inc., Wilmington, DE). cDNA was synthesized from 20 \xc2\xb5g total RNA and differentially labeled according to manufacturer\xe2\x80\x99s instructions with the SuperScriptTM Plus Indirect cDNA labeling System (Invitrogen). Before and after indirect labeling with Alexa Fluor 555 or Alexa Fluor 647 (at least 3 h at room temperature) cDNA was purified using the Qiagen MinElute PCR Purification Kit (Qiagen, Maryland) and quantified via NanoDrop.',
						  'Total RNA was isolated from Bacillus subtilis 168 and DapR1 grown to mid-log phase (OD600 of 0.4) using the RNeasy Mini Kit (Qiagen Sciences, Maryland). After DNase treatment with TURBO DNA-freeTM (Ambion), RNA concentrations were quantified using a NanoDrop spectrophotometer (NanoDrop Tech. Inc., Wilmington, DE). cDNA was synthesized from 20 \xc2\xb5g total RNA and differentially labeled according to manufacturer\xe2\x80\x99s instructions with the SuperScriptTM Plus Indirect cDNA labeling System (Invitrogen). Before and after indirect labeling with Alexa Fluor 555 or Alexa Fluor 647 (at least 3 h at room temperature) cDNA was purified using the Qiagen MinElute PCR Purification Kit (Qiagen, Maryland) and quantified via NanoDrop.'],
						 'sample_geo_accession': ['GSM742494',
						  'GSM742495',
						  'GSM742496',
						  'GSM742497',
						  'GSM742498',
						  'GSM742499',
						  'GSM742500',
						  'GSM742501'],
						 'sample_hyb_protocol': ['Equal amounts (100-150 pmol) of labeled cDNA were combined plus hybridization buffer (2X = 50% formamide, 10X SSC, 0.1% SDS). cDNA mix was denatured at 95oC and hybridized 16-18 hours at 42oC to DNA microarray slides which had been prehybridized for at least 30 min at 42oC in 1% bovine serum albumin, 5X SSC (1X SSC is 0.15 M NaCl and 0.015 M sodium citrate), 0.1% sodium dodecyl sulfate (SDS), washed in water and dried. Following hybridization the slides were washed sequentially in: 2X SSC + 0.1% SDS for 5 min at 42oC, 2X SSC + 0.1% SDS for 5 min at room temperature, 2X SSC for 5 min at room temperature, 0.2X SSC for 5 min at room temperature, and finally dipped in water and spun until dry.',
						  'Equal amounts (100-150 pmol) of labeled cDNA were combined plus hybridization buffer (2X = 50% formamide, 10X SSC, 0.1% SDS). cDNA mix was denatured at 95oC and hybridized 16-18 hours at 42oC to DNA microarray slides which had been prehybridized for at least 30 min at 42oC in 1% bovine serum albumin, 5X SSC (1X SSC is 0.15 M NaCl and 0.015 M sodium citrate), 0.1% sodium dodecyl sulfate (SDS), washed in water and dried. Following hybridization the slides were washed sequentially in: 2X SSC + 0.1% SDS for 5 min at 42oC, 2X SSC + 0.1% SDS for 5 min at room temperature, 2X SSC for 5 min at room temperature, 0.2X SSC for 5 min at room temperature, and finally dipped in water and spun until dry.',
						  'Equal amounts (100-150 pmol) of labeled cDNA were combined plus hybridization buffer (2X = 50% formamide, 10X SSC, 0.1% SDS). cDNA mix was denatured at 95oC and hybridized 16-18 hours at 42oC to DNA microarray slides which had been prehybridized for at least 30 min at 42oC in 1% bovine serum albumin, 5X SSC (1X SSC is 0.15 M NaCl and 0.015 M sodium citrate), 0.1% sodium dodecyl sulfate (SDS), washed in water and dried. Following hybridization the slides were washed sequentially in: 2X SSC + 0.1% SDS for 5 min at 42oC, 2X SSC + 0.1% SDS for 5 min at room temperature, 2X SSC for 5 min at room temperature, 0.2X SSC for 5 min at room temperature, and finally dipped in water and spun until dry.',
						  'Equal amounts (100-150 pmol) of labeled cDNA were combined plus hybridization buffer (2X = 50% formamide, 10X SSC, 0.1% SDS). cDNA mix was denatured at 95oC and hybridized 16-18 hours at 42oC to DNA microarray slides which had been prehybridized for at least 30 min at 42oC in 1% bovine serum albumin, 5X SSC (1X SSC is 0.15 M NaCl and 0.015 M sodium citrate), 0.1% sodium dodecyl sulfate (SDS), washed in water and dried. Following hybridization the slides were washed sequentially in: 2X SSC + 0.1% SDS for 5 min at 42oC, 2X SSC + 0.1% SDS for 5 min at room temperature, 2X SSC for 5 min at room temperature, 0.2X SSC for 5 min at room temperature, and finally dipped in water and spun until dry.',
						  'Equal amounts (100-150 pmol) of labeled cDNA were combined plus hybridization buffer (2X = 50% formamide, 10X SSC, 0.1% SDS). cDNA mix was denatured at 95oC and hybridized 16-18 hours at 42oC to DNA microarray slides which had been prehybridized for at least 30 min at 42oC in 1% bovine serum albumin, 5X SSC (1X SSC is 0.15 M NaCl and 0.015 M sodium citrate), 0.1% sodium dodecyl sulfate (SDS), washed in water and dried. Following hybridization the slides were washed sequentially in: 2X SSC + 0.1% SDS for 5 min at 42oC, 2X SSC + 0.1% SDS for 5 min at room temperature, 2X SSC for 5 min at room temperature, 0.2X SSC for 5 min at room temperature, and finally dipped in water and spun until dry.',
						  'Equal amounts (100-150 pmol) of labeled cDNA were combined plus hybridization buffer (2X = 50% formamide, 10X SSC, 0.1% SDS). cDNA mix was denatured at 95oC and hybridized 16-18 hours at 42oC to DNA microarray slides which had been prehybridized for at least 30 min at 42oC in 1% bovine serum albumin, 5X SSC (1X SSC is 0.15 M NaCl and 0.015 M sodium citrate), 0.1% sodium dodecyl sulfate (SDS), washed in water and dried. Following hybridization the slides were washed sequentially in: 2X SSC + 0.1% SDS for 5 min at 42oC, 2X SSC + 0.1% SDS for 5 min at room temperature, 2X SSC for 5 min at room temperature, 0.2X SSC for 5 min at room temperature, and finally dipped in water and spun until dry.',
						  'Equal amounts (100-150 pmol) of labeled cDNA were combined plus hybridization buffer (2X = 50% formamide, 10X SSC, 0.1% SDS). cDNA mix was denatured at 95oC and hybridized 16-18 hours at 42oC to DNA microarray slides which had been prehybridized for at least 30 min at 42oC in 1% bovine serum albumin, 5X SSC (1X SSC is 0.15 M NaCl and 0.015 M sodium citrate), 0.1% sodium dodecyl sulfate (SDS), washed in water and dried. Following hybridization the slides were washed sequentially in: 2X SSC + 0.1% SDS for 5 min at 42oC, 2X SSC + 0.1% SDS for 5 min at room temperature, 2X SSC for 5 min at room temperature, 0.2X SSC for 5 min at room temperature, and finally dipped in water and spun until dry.',
						  'Equal amounts (100-150 pmol) of labeled cDNA were combined plus hybridization buffer (2X = 50% formamide, 10X SSC, 0.1% SDS). cDNA mix was denatured at 95oC and hybridized 16-18 hours at 42oC to DNA microarray slides which had been prehybridized for at least 30 min at 42oC in 1% bovine serum albumin, 5X SSC (1X SSC is 0.15 M NaCl and 0.015 M sodium citrate), 0.1% sodium dodecyl sulfate (SDS), washed in water and dried. Following hybridization the slides were washed sequentially in: 2X SSC + 0.1% SDS for 5 min at 42oC, 2X SSC + 0.1% SDS for 5 min at room temperature, 2X SSC for 5 min at room temperature, 0.2X SSC for 5 min at room temperature, and finally dipped in water and spun until dry.'],
						 'sample_label_ch1': ['Alexa Fluor 555',
						  'Alexa Fluor 555',
						  'Alexa Fluor 555',
						  'Alexa Fluor 555',
						  'Alexa Fluor 555',
						  'Alexa Fluor 555',
						  'Alexa Fluor 555',
						  'Alexa Fluor 647'],
						 'sample_label_ch2': ['Alexa Fluor 647',
						  'Alexa Fluor 647',
						  'Alexa Fluor 647',
						  'Alexa Fluor 647',
						  'Alexa Fluor 647',
						  'Alexa Fluor 647',
						  'Alexa Fluor 647',
						  'Alexa Fluor 555'],
						 'sample_label_protocol_ch1': ['cDNA synthesis was performed using the SuperScriptTM Plus Indirect cDNA labeling System (Invitrogen) as per the manufacturer\xe2\x80\x99s instructions using 20 microgram of total RNA. Total cDNA was labeled overnight with Alexa Fluor 555 or Alexa Fluor 647 (Invitrogen)',
						  'cDNA synthesis was performed using the SuperScriptTM Plus Indirect cDNA labeling System (Invitrogen) as per the manufacturer\xe2\x80\x99s instructions using 20 microgram of total RNA. Total cDNA was labeled overnight with Alexa Fluor 555 or Alexa Fluor 647 (Invitrogen)',
						  'cDNA synthesis was performed using the SuperScriptTM Plus Indirect cDNA labeling System (Invitrogen) as per the manufacturer\xe2\x80\x99s instructions using 20 microgram of total RNA. Total cDNA was labeled overnight with Alexa Fluor 555 or Alexa Fluor 647 (Invitrogen)',
						  'cDNA synthesis was performed using the SuperScriptTM Plus Indirect cDNA labeling System (Invitrogen) as per the manufacturer\xe2\x80\x99s instructions using 20 microgram of total RNA. Total cDNA was labeled overnight with Alexa Fluor 555 or Alexa Fluor 647 (Invitrogen)',
						  'cDNA synthesis was performed using the SuperScriptTM Plus Indirect cDNA labeling System (Invitrogen) as per the manufacturer\xe2\x80\x99s instructions using 20 microgram of total RNA. Total cDNA was labeled overnight with Alexa Fluor 555 or Alexa Fluor 647 (Invitrogen)',
						  'cDNA synthesis was performed using the SuperScriptTM Plus Indirect cDNA labeling System (Invitrogen) as per the manufacturer\xe2\x80\x99s instructions using 20 microgram of total RNA. Total cDNA was labeled overnight with Alexa Fluor 555 or Alexa Fluor 647 (Invitrogen)',
						  'cDNA synthesis was performed using the SuperScriptTM Plus Indirect cDNA labeling System (Invitrogen) as per the manufacturer\xe2\x80\x99s instructions using 20 microgram of total RNA. Total cDNA was labeled overnight with Alexa Fluor 555 or Alexa Fluor 647 (Invitrogen)',
						  'cDNA synthesis was performed using the SuperScriptTM Plus Indirect cDNA labeling System (Invitrogen) as per the manufacturer\xe2\x80\x99s instructions using 20 microgram of total RNA. Total cDNA was labeled overnight with Alexa Fluor 555 or Alexa Fluor 647 (Invitrogen)'],
						 'sample_label_protocol_ch2': ['cDNA synthesis was performed using the SuperScriptTM Plus Indirect cDNA labeling System (Invitrogen) as per the manufacturer\xe2\x80\x99s instructions using 20 microgram of total RNA. Total cDNA was labeled overnight with Alexa Fluor 555 or Alexa Fluor 647 (Invitrogen)',
						  'cDNA synthesis was performed using the SuperScriptTM Plus Indirect cDNA labeling System (Invitrogen) as per the manufacturer\xe2\x80\x99s instructions using 20 microgram of total RNA. Total cDNA was labeled overnight with Alexa Fluor 555 or Alexa Fluor 647 (Invitrogen)',
						  'cDNA synthesis was performed using the SuperScriptTM Plus Indirect cDNA labeling System (Invitrogen) as per the manufacturer\xe2\x80\x99s instructions using 20 microgram of total RNA. Total cDNA was labeled overnight with Alexa Fluor 555 or Alexa Fluor 647 (Invitrogen)',
						  'cDNA synthesis was performed using the SuperScriptTM Plus Indirect cDNA labeling System (Invitrogen) as per the manufacturer\xe2\x80\x99s instructions using 20 microgram of total RNA. Total cDNA was labeled overnight with Alexa Fluor 555 or Alexa Fluor 647 (Invitrogen)',
						  'cDNA synthesis was performed using the SuperScriptTM Plus Indirect cDNA labeling System (Invitrogen) as per the manufacturer\xe2\x80\x99s instructions using 20 microgram of total RNA. Total cDNA was labeled overnight with Alexa Fluor 555 or Alexa Fluor 647 (Invitrogen)',
						  'cDNA synthesis was performed using the SuperScriptTM Plus Indirect cDNA labeling System (Invitrogen) as per the manufacturer\xe2\x80\x99s instructions using 20 microgram of total RNA. Total cDNA was labeled overnight with Alexa Fluor 555 or Alexa Fluor 647 (Invitrogen)',
						  'cDNA synthesis was performed using the SuperScriptTM Plus Indirect cDNA labeling System (Invitrogen) as per the manufacturer\xe2\x80\x99s instructions using 20 microgram of total RNA. Total cDNA was labeled overnight with Alexa Fluor 555 or Alexa Fluor 647 (Invitrogen)',
						  'cDNA synthesis was performed using the SuperScriptTM Plus Indirect cDNA labeling System (Invitrogen) as per the manufacturer\xe2\x80\x99s instructions using 20 microgram of total RNA. Total cDNA was labeled overnight with Alexa Fluor 555 or Alexa Fluor 647 (Invitrogen)'],
						 'sample_last_update_date': ['Jun 16 2011',
						  'Jun 16 2011',
						  'Jun 16 2011',
						  'Jun 16 2011',
						  'Jun 16 2011',
						  'Jun 16 2011',
						  'Jun 16 2011',
						  'Jun 16 2011'],
						 'sample_molecule_ch1': ['total RNA',
						  'total RNA',
						  'total RNA',
						  'total RNA',
						  'total RNA',
						  'total RNA',
						  'total RNA',
						  'total RNA'],
						 'sample_molecule_ch2': ['total RNA',
						  'total RNA',
						  'total RNA',
						  'total RNA',
						  'total RNA',
						  'total RNA',
						  'total RNA',
						  'total RNA'],
						 'sample_name': ['GSM742494',
						  'GSM742495',
						  'GSM742496',
						  'GSM742497',
						  'GSM742498',
						  'GSM742499',
						  'GSM742500',
						  'GSM742501'],
						 'sample_organism_ch1': ['Bacillus subtilis',
						  'Bacillus subtilis',
						  'Bacillus subtilis',
						  'Bacillus subtilis',
						  'Bacillus subtilis',
						  'Bacillus subtilis',
						  'Bacillus subtilis',
						  'Bacillus subtilis'],
						 'sample_organism_ch2': ['Bacillus subtilis',
						  'Bacillus subtilis',
						  'Bacillus subtilis',
						  'Bacillus subtilis',
						  'Bacillus subtilis',
						  'Bacillus subtilis',
						  'Bacillus subtilis',
						  'Bacillus subtilis'],
						 'sample_platform_id': ['GPL7420',
						  'GPL7420',
						  'GPL7420',
						  'GPL7420',
						  'GPL7420',
						  'GPL7420',
						  'GPL7420',
						  'GPL7420'],
						 'sample_scan_protocol': ['Arrays were scanned using a GenePixTM 4000B array scanner (Axon Instruments, Inc.)',
						  'Arrays were scanned using a GenePixTM 4000B array scanner (Axon Instruments, Inc.)',
						  'Arrays were scanned using a GenePixTM 4000B array scanner (Axon Instruments, Inc.)',
						  'Arrays were scanned using a GenePixTM 4000B array scanner (Axon Instruments, Inc.)',
						  'Arrays were scanned using a GenePixTM 4000B array scanner (Axon Instruments, Inc.)',
						  'Arrays were scanned using a GenePixTM 4000B array scanner (Axon Instruments, Inc.)',
						  'Arrays were scanned using a GenePixTM 4000B array scanner (Axon Instruments, Inc.)',
						  'Arrays were scanned using a GenePixTM 4000B array scanner (Axon Instruments, Inc.)'],
						 'sample_scan_protocol.1': ['Raw data files were produced from the scanned images using the GenePix Pro 6.0 software package (GPR files).',
						  'Raw data files were produced from the scanned images using the GenePix Pro 6.0 software package (GPR files).',
						  'Raw data files were produced from the scanned images using the GenePix Pro 6.0 software package (GPR files).',
						  'Raw data files were produced from the scanned images using the GenePix Pro 6.0 software package (GPR files).',
						  'Raw data files were produced from the scanned images using the GenePix Pro 6.0 software package (GPR files).',
						  'Raw data files were produced from the scanned images using the GenePix Pro 6.0 software package (GPR files).',
						  'Raw data files were produced from the scanned images using the GenePix Pro 6.0 software package (GPR files).',
						  'Raw data files were produced from the scanned images using the GenePix Pro 6.0 software package (GPR files).'],
						 'sample_source_name_ch1': ['WT/-DAP',
						  'WT/-DAP',
						  'WT/+DAP',
						  'WT/+DAP',
						  'DapR1/-DAP',
						  'DapR1/-DAP',
						  'DapR1/-DAP',
						  'DapR1/-DAP'],
						 'sample_source_name_ch2': ['DapR1/-DAP',
						  'DapR1/-DAP',
						  'DapR1/+DAP',
						  'DapR1/+DAP',
						  'DapR1/+DAP',
						  'DapR1/+DAP',
						  'DapR1/+DAP',
						  'DapR1/+DAP'],
						 'sample_status': ['Public on Jun 16 2011',
						  'Public on Jun 16 2011',
						  'Public on Jun 16 2011',
						  'Public on Jun 16 2011',
						  'Public on Jun 16 2011',
						  'Public on Jun 16 2011',
						  'Public on Jun 16 2011',
						  'Public on Jun 16 2011'],
						 'sample_submission_date': ['Jun 15 2011',
						  'Jun 15 2011',
						  'Jun 15 2011',
						  'Jun 15 2011',
						  'Jun 15 2011',
						  'Jun 15 2011',
						  'Jun 15 2011',
						  'Jun 15 2011'],
						 'sample_supplementary_file': ['ftp://ftp.ncbi.nlm.nih.gov/pub/geo/DATA/supplementary/samples/GSM742nnn/GSM742494/GSM742494_WT_vs_DapR1_rep1.gpr.gz',
						  'ftp://ftp.ncbi.nlm.nih.gov/pub/geo/DATA/supplementary/samples/GSM742nnn/GSM742495/GSM742495_WT_vs_DapR1_rep2.gpr.gz',
						  'ftp://ftp.ncbi.nlm.nih.gov/pub/geo/DATA/supplementary/samples/GSM742nnn/GSM742496/GSM742496_WT_vs_DapR1_+DAP_rep1.gpr.gz',
						  'ftp://ftp.ncbi.nlm.nih.gov/pub/geo/DATA/supplementary/samples/GSM742nnn/GSM742497/GSM742497_WT_vs_DapR1_+DAP_rep2.gpr.gz',
						  'ftp://ftp.ncbi.nlm.nih.gov/pub/geo/DATA/supplementary/samples/GSM742nnn/GSM742498/GSM742498_DapR1_+DAP_vs_DapR1_-DAP_rep1.gpr.gz',
						  'ftp://ftp.ncbi.nlm.nih.gov/pub/geo/DATA/supplementary/samples/GSM742nnn/GSM742499/GSM742499_DapR1_+DAP_vs_DapR1_-DAP_rep2.gpr.gz',
						  'ftp://ftp.ncbi.nlm.nih.gov/pub/geo/DATA/supplementary/samples/GSM742nnn/GSM742500/GSM742500_DapR1_+DAP_vs_DapR1_-DAP_rep3.gpr.gz',
						  'ftp://ftp.ncbi.nlm.nih.gov/pub/geo/DATA/supplementary/samples/GSM742nnn/GSM742501/GSM742501_DapR1_+DAP_vs_DapR1_-DAP_rep4.gpr.gz'],
						 'sample_taxid_ch1': ['1423',
						  '1423',
						  '1423',
						  '1423',
						  '1423',
						  '1423',
						  '1423',
						  '1423'],
						 'sample_taxid_ch2': ['1423',
						  '1423',
						  '1423',
						  '1423',
						  '1423',
						  '1423',
						  '1423',
						  '1423'],
						 'sample_title': ['WT(-DAP)vsDapR1(-DAP)_rep1',
						  'WT(-DAP)vsDapR1(-DAP)_rep2',
						  'WT(+DAP)vsDapR1(+DAP)_rep1',
						  'WT(+DAP)vsDapR1(+DAP)_rep2',
						  'DapR1(+DAP)_vs_DapR1(-DAP)_rep1',
						  'DapR1(+DAP)_vs_DapR1(-DAP)_rep2',
						  'DapR1(+DAP)_vs_DapR1(-DAP)_rep3',
						  'DapR1(+DAP)_vs_DapR1(-DAP)_rep4'],
						 'sample_type': ['RNA', 'RNA', 'RNA', 'RNA', 'RNA', 'RNA', 'RNA', 'RNA'],
						 'taxid': '1423',
						 'title': 'Reduction in membrane phosphatidylglycerol content leads to daptomycin resistance in Bacillus subtilis',
						 'type': 'Expression profiling by array'}

c_GSE30000PCL = [['GID',
				  'NAME',
				  'GWEIGHT',
				  'GSM742494: WT(-DAP)vsDapR1(-DAP)_rep1',
				  'GSM742495: WT(-DAP)vsDapR1(-DAP)_rep2',
				  'GSM742496: WT(+DAP)vsDapR1(+DAP)_rep1',
				  'GSM742497: WT(+DAP)vsDapR1(+DAP)_rep2',
				  'GSM742498: DapR1(+DAP)_vs_DapR1(-DAP)_rep1',
				  'GSM742499: DapR1(+DAP)_vs_DapR1(-DAP)_rep2',
				  'GSM742500: DapR1(+DAP)_vs_DapR1(-DAP)_rep3',
				  'GSM742501: DapR1(+DAP)_vs_DapR1(-DAP)_rep4'],
				 ['UniRef90_P42065',
				  'appF',
				  '1',
				  '-2.0307',
				  '-3.6112',
				  '-3.2095',
				  '-2.0844',
				  '-0.0317',
				  '-0.0609',
				  '-0.0346',
				  '-0.0148'],
				 ['UniRef90_P94528',
				  'araN',
				  '1',
				  '-0.1904',
				  '-1.8272',
				  '-2.2069',
				  '0.2261',
				  '-0.102',
				  '2.1699',
				  '-0.1184',
				  '-0.3543'],
				 ['UniRef90_P94530',
				  'araQ',
				  '1',
				  '-0.4491',
				  '-1.543',
				  '-1.9125',
				  '0.046',
				  '-0.7331',
				  '5.1497',
				  '-0.415',
				  '-0.4161'],
				 ['UniRef90_P40739',
				  'bglP',
				  '1',
				  '0.4359',
				  '0.0409',
				  '-1.0871',
				  '0.649',
				  '0.1087',
				  '0.2338',
				  '0.5475',
				  '-0.3036'],
				 ['UniRef90_P33449',
				  'bmr',
				  '1',
				  '1.0599',
				  '0.4354',
				  '0.0673',
				  '1.9039',
				  '0.1588',
				  '-0.2502',
				  '0.018',
				  '-0.1121']]

## Execute 

# test data 

exec_test( c_dirGEO, None, [c_fileGDS2250PCL,c_GDS2250PCL] )
exec_test( c_dirGEO, None, [c_fileGSE12831PCL,c_GSE12831PCL] )
exec_test( c_dirGEO, None, [c_fileGSE30000PCL,c_GSE30000PCL] )

# test metadata 
exec_test( c_dirGEO, lambda f: pickle.load(open(f)), [c_fileGDS2250PKL, c_GDS2250PKL] ) 
exec_test( c_dirGEO, lambda f: pickle.load(open(f)), [c_fileGSE12831PKL,c_GSE12831PKL] )
exec_test( c_dirGEO, lambda f: pickle.load(open(f)), [c_fileGSE30000PKL,c_GSE30000PKL] )


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

c_STRINGtaxidPtmodDat		= [['Mkms_0391', 'Mkms_0470', '0.173'],
				['Mkms_0391', 'Mkms_2458', '0.316'],
				['Mkms_1218', 'Mkms_5095', '0.226'],
				['Mkms_0025', 'Mkms_0023', '0.445'],
				['Mkms_3334', 'Mkms_3333', '0.365'],
				['Mkms_2004', 'Mkms_2003', '0.204']]

## Execute 

#exec_test( c_dirSTRING, None,
#		[c_fileSTRINGtaxidBindingDat, c_STRINGtaxidBindingDat],
#		[c_fileSTRINGtaxidExpressionDat, c_STRINGtaxidExpressionDat],
#		[c_fileSTRINGtaxidPtmodDat, c_STRINGtaxidPtmodDat] )

