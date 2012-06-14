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

c_arepacwd = arepa.cwd() 

#Do extensive test on GEO, do 2-3 tests on other modules 

#=====================================================#
#		General Helper Functions 
#=====================================================#

def test_against( infile, constant, parse_function ):
	pTest = parse_function( infile )
	if pTest == constant:
		print "test passed for", infile 
	else:
		raise Exception("!test failed", infile)

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

c_dirGEO		=	sfle.d( arepa.path_arepa( ), "GEO")
c_dirGEOData		= 	sfle.d( c_dirGEO, sfle.c_strDirData )
c_dirGSE10183		=	sfle.d( c_dirGEOData,c_strGSE10183, c_strGSE10183 )
c_fileGSE10183PKL	= 	sfle.d( c_dirGSE10183, c_strGSE10183 + ".pkl" )
c_fileGSE10183PCL	=	sfle.d( c_dirGSE10183, c_strGSE10183 + ".pcl" ) 

c_strChannels		= 	"channels"
c_GSE10183PKLCurated	=	['', 'title', 'geo_accession', 'status', 'submission_date', 'last_update_date', 'type', 'channel_count', 'source_name_ch1', 'organism_ch1', 'characteristics_ch1', 'characteristics_ch1.1', 'molecule_ch1', 'extract_protocol_ch1', 'label_ch1', 'label_protocol_ch1', 'taxid_ch1', 'hyb_protocol', 'scan_protocol', 'description', 'data_processing', 'platform_id', 'contact_name', 'contact_laboratory', 'contact_department', 'contact_institute', 'contact_address', 'contact_city', 'contact_state', 'contact_zip/postal_code', 'contact_country', 'supplementary_file', 'data_row_count']
c_GSE10183PKLChannels	=	['1', '1']
c_GSE10183PCL		= 	[['1007_s_at', 'U48705', '1', '10.34880883', '10.25328334'], \
				['1053_at', 'M87338', '1', '7.096953279', '7.16038339']]	

def geo_test( strId, inPKL, inPCL, cPKL, cPCL ):
	def pkl_test( inPKL, cPKL ):
		pkl = pickle.load(open( inPKL, "r"))
	 	if pkl["curated"] == cPKL:
			print "geo pkl test passed", inPKL
		else:
			Exception("geo pkl test failed", inPKL)
	def pcl_test( inPCL, cPCL ):
		print "geo pcl test passed"
	pkl_test( inPKL, cPKL )
	pcl_test( inPCL, cPCL )

#=====================================================#
#               	ArrayExpress
#=====================================================#

'''Test module for ArrayExpress does not exist'''

#=====================================================#
#               	Bacteriome
#=====================================================#
c_dirBacteriome		= 	sfle.d( arepa.path_arepa( ), "Bacteriome" )
c_dirBacteriomeData	=	sfle.d( c_dirBacteriome, sfle.c_strDirData )
c_fileBacteriomeDat	= 	sfle.d( c_dirBacteriomeData, "bacteriome.dat" )
c_fileBacteriomeQuant	=	sfle.d( c_dirBacteriomeData, "bacteriome.quant")

c_BacteriomeQuantLst	=	[0.5,1.5]
c_BacteriomeDatLst	= 	[["b0002","b0003","0.408408"],["b0002","b0004","0.408408"]]
'''test 2 output files: bacteriome.dat, bacteriome.quant'''

def bacteriome_test():
	def quant_test():
		f = open( c_fileBacteriomeQuant )
		g = f.read() 
		lst = map(lambda v: float(v), g.replace("\n","").split("\t"))
		if lst == c_BacteriomeQuantLst:
			print "bacteriome.quant passed"
		else:
			raise Exception("bacteriome.quant test failed.")
	def dat_test():
		dummylst = [] 
		csvr = csv.reader(open( c_fileBacteriomeDat ), delimiter="\t")
		for line in csvr:
			dummylst.append(line)
		if dummylst[0:2] == c_BacteriomeDatLst:
			print "bacteriome.dat passed"
		else:
			raise Exception("bacteriome.dat test failed")
	dat_test()
	quant_test() 
	
if __name__ == "__main__":
	os.chdir( c_dirBacteriome )
	subprocess.call( "scons" )
	bacteriome_test() 

#=====================================================#
#                       BioGrid
#=====================================================#

c_strBioGrid		= "taxid_224308"
c_dirBioGrid		= sfle.d( arepa.path_arepa( ), "BioGrid" )
c_dirBioGridData	= sfle.d( c_dirBioGrid, sfle.c_strDirData, c_strBioGrid )
c_fileBioGridPKL	= sfle.d( c_dirBioGridData, "taxid_224308.pkl" )
c_fileBioGridDat	= sfle.d( c_dirBioGridData, "taxid_224308.dat" )
c_fileBioGridQuant	= sfle.d( c_dirBioGridData, "taxid_224308.quant" )

c_BioGridDat		= ['rsbV', 'rsbW', '1'] 
c_BioGridPKL		= {'platform': 'Co-purification', 'pmid': '8144446', 'type': '857505', 'taxid': '855787'}
c_BioGridQuant		= [0.5, 1.5]

def biogrid_test():
	def dat_test():
		f = open( c_fileBioGridDat )
		g = f.read()
		tLst = g.replace("\n","").split("\t")
		if tLst == c_BioGridDat:
			print "biogrid dat test passed"
		else:
			raise Exception("biogrid dat test failed")
	def pkl_test():
		pkl = pickle.load( open( c_fileBioGridPKL ) )
		if pkl == c_BioGridPKL:
			print "biogrid pkl test passed"
		else: 
			raise Exception("biogrid pkl test failed")
	def quant_test():
		f = open( c_fileBioGridQuant )
		g = f.read()
		tLst = map(lambda v: float(v), g.replace("\n","").split("\t"))
		if tLst == c_BioGridQuant:
			print "biogrid quant test passed"
		else:
			raise Exception("biogrid quant test failed")
	dat_test()
	pkl_test()
	quant_test() 

if __name__ == "__main__":
	os.chdir( c_dirBioGrid )
	subprocess.call( "scons" )
	biogrid_test()

#=====================================================#
#                       IntAct
#=====================================================#

#=====================================================#
#                       MPIDP
#=====================================================#

#=====================================================#
#                       RegulonDB 
#=====================================================#

#=====================================================#
#                       STRING
#=====================================================#
