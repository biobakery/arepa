#!/usr/bin/env python
'''
Genemapping python wrapper for BridgeDB gene mapper

Type "python bridgemapper.py -h" for help
'''

import argparse
import csv
import os
import re
import subprocess
import sys
import tempfile
import metadata 
import sys 

# These are the only genes that we are keeping track of for now 

c_hashGeneNames	= {"HGNC": "H", 
					"UniGene": "U",
					"Uniprot/TrEMBL": "S",
					"Ensembl": "En",
					"Kegg Genes": "Kg",
					"Kegg Compound": "Ck"
					}

#########################################################
# GENE ID MAPPING: Convert Gene Identifiers
#########################################################
def convertGeneIds( setstrGenes, strMap, strFrom, strTo ):
	pFrom, pTo = [tempfile.NamedTemporaryFile( delete=False ) for i in xrange( 2 )]

	pFrom.write( "\n".join( setstrGenes ) + "\n" )
	pFrom.flush()

	strBatchmapperSH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "trunk/batchmapper.sh")
	strMapFlag = "-g" if strMap.endswith( ".bridge" ) else "-t"

	subprocess.check_call( ("sh",strBatchmapperSH, "-i", pFrom.name, "-is", strFrom,\
		"-os", strTo, "-o", pTo.name, strMapFlag, strMap,"-mm") )

	hashMap = {a[1]:a[0] for a in csv.reader( pTo, csv.excel_tab )}
	pTo.flush()
	os.unlink(pFrom.name); os.unlink(pTo.name)
	return hashMap
		
def bridgemapper( istm, ostm, strMap, strCols, strFrom, strTo, ostmLog, iSkip ):

	strCols = strCols[1:-1]
	aiCols = [int(s) for s in re.split( r'\s*,\s*', strCols )] if strCols else []
	
	#Open a blank metadata object and initialize 
	pMeta = metadata.open( )
	pMeta.set( "mapped", False )

	aastrData = []
	setstrIn = set()
	csvr = csv.reader( istm, csv.excel_tab )
	for astrLine in csvr:
		aastrData.append( astrLine )
		if csvr.line_num < iSkip:
			continue
		for iCol in aiCols:
			if iCol < len( astrLine ):
				setstrIn.add( astrLine[iCol] )
			else:
				sys.stderr.write(" +++ ERROR in GeneMapper +++ Number of requested columns to \
					map is larger than the number of columns in the input data file.\n")
	
	hashMap = None
	# Make sure mapping file exists and has nonzero file size
	if strMap and os.path.exists( strMap ) and ( os.stat( strMap )[6] > 0 ):
		hashMap = convertGeneIds( setstrIn, strMap, strFrom, strTo )
	else:
		sys.stderr.write("+++ ERROR in GeneMapper +++ Input file does not exist or is empty. \
			Return empty file. \n")
	
	if hashMap:
		if any(hashMap.values()):
			pMeta.set( "mapped", True )
			for iRow in xrange( iSkip, len( aastrData ) ):
				astrRow = aastrData[iRow]
				for iCol in aiCols:
					if iCol < len( astrRow ):
						strTo = hashMap.get( astrRow[iCol] )
						if strTo:
							astrRow[iCol] = strTo
						else:
							astrRow[iCol] = ""
	else:
		sys.stderr.write("+++Error in GeneMapper +++ Empty mapping. \
			Return original file. \n")      
				
	csvw = csv.writer( ostm, csv.excel_tab )
	#make sure that if the mapping is empty for one of the columns, delete the entire row
	for astrLine in aastrData:
		if all(astrLine): csvw.writerow( astrLine )
	if ostmLog:
		pMeta.save_text( ostmLog )

#TODO: Add Sniffer For Gene Identifiers
#IDEA: do some kind of bootstrapping procedure to make sure you are indeed getting the right identifier


def gene_sniffer( istm, strCols ):
	'''
	takes in input file, outputs gene identifier convention, e.g. HGNC
	'''
	def _sniff( name_list ):
		pass 

	strCols = strCols[1:-1]
	aiCols = [int(s) for s in re.split( r'\s*,\s*', strCols )] if strCols else []
	
	#Open a blank metadata object and initialize 
	aastrData = []
	setstrIn = set()
	csvr = csv.reader( istm, csv.excel_tab )

'''
NOTES 

UniGene - 
This one is easy; it starts with either "UniRef90" or "UniRef100"

Uniprot/TrEMBL -
Always 6 alphanumeric characeters, a lot of them start with P or Q
About 70% of them start with P or Q


Q8TBF5 
Q8TBF4  
P30613  
Q5H9L4  
P20933  
P20936  
Q8IZF2  
Q2T9G7  
P31213  
Q9NXR8  
E9PN47  
Q4VXU2  
Q96N66  
Q00532  
Q96J66  
O00712  
Q9UBM8  
Q96J65  
O00241  
O00716  
Q96KS0  
Q9UBM7  
Q6BEB4  
Q92911  
Q13835  
Q7Z3T1  
P40424  
P40425  
B3KVK0  
B3KVK3  
Q7Z3T8  
Q13838  
        

'''


argp = argparse.ArgumentParser( prog = "bridgemapper.py",
	description = """Maps gene IDs from one or more tab-delimited text columns from and to specified formats.""" )
argp.add_argument( "istm",		metavar = "input.dat",
	type = argparse.FileType( "r" ),	nargs = "?",	default = sys.stdin,
	help = "Input tab-delimited text file with one or more columns" )
argp.add_argument( "ostm",		metavar = "output.dat",
	type = argparse.FileType( "w" ),	nargs = "?",	default = sys.stdout,
	help = "Input tab-delimited text file with mapped columns" )
argp.add_argument( "-m",		dest = "strMap",	metavar = "mapping.txt",
	type = str,					required = False,
	help = "Required mapping file in tab-delimited BridgeMapper format" )
argp.add_argument( "-c",		dest = "strCols",	metavar = "columns",
	type = str,				default = "[]",
	help = "Columns to map, formatted as [1,2,3]" )
argp.add_argument( "-f",		dest = "strFrom",	metavar = "from_format",
	type = str,				default = "X",
	help = "BridgeMapper single-character type code for input format" )
argp.add_argument( "-t",		dest = "strTo",		metavar = "to_format",
	type = str,				default = "H",
	help = "BridgeMapper single-character type code for output format" )
argp.add_argument( "-s",		dest = "iSkip",		metavar = "skip_rows",
	type = int,					default = 0,
	help = "Number of header rows to skip at top of file" )
argp.add_argument( "-l",		dest = "ostmLog",	metavar = "log.txt",
	type = argparse.FileType( "w" ),
	help = "Optional log file containing output mapping status" )
argp.add_argument('-x', 		dest = "fSniffer" ,	action="store_true", default=False, 
	help = "Optional flag turning on/off gene identifier sniffer (automatically decide geneid_from)" )

def _main( ):
	args = argp.parse_args( )
	if args.strFrom == args.strTo:
		#if the two gene identifier types are the same, return the input file 
		pAastrData = csv.reader(args.istm,csv.excel_tab)
		csvw = csv.writer( args.ostm, csv.excel_tab )
		for astrLine in pAastrData:
			csvw.writerow( astrLine )	
		if args.ostmLog:
			pMeta = metadata.open()
			pMeta.set("mapped", True)			
			pMeta.save_text( args.ostmLog )
	elif not(args.strMap) or not(os.stat(str(args.strMap))[6]):
		#if there is no map file specified 
		pAastrData = csv.reader(args.istm,csv.excel_tab)
		csvw = csv.writer( args.ostm, csv.excel_tab )
		for astrLine in pAastrData:
			csvw.writerow( astrLine )	
		if args.ostmLog:
			pMeta = metadata.open()
			pMeta.set("mapped",False)
			pMeta.save_text( args.ostmLog )
	else:
		bridgemapper( args.istm, args.ostm, args.strMap, args.strCols, args.strFrom, args.strTo, args.ostmLog, args.iSkip )

if __name__ == "__main__":
	_main( )
