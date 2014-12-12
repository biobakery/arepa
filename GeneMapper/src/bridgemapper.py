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

Genemapping python wrapper for BridgeDB gene mapper

Type "python bridgemapper.py -h" for help
"""

import argparse
import operator 
import csv
import os
import re
import subprocess
import sys
import tempfile
import metadata 
import sys 
import sfle 

# These are the only genes that we are keeping track of for now 

c_hashGeneNames		= {"HGNC": "H", 
					"UniGene": "U",
					"Uniprot/TrEMBL": "S",
					"Ensembl": "En",
					"KEGG Genes": "Kg",
					"Kegg Compound": "Ck"
					}
					
c_strDefaultGeneIDFrom	= "KEGG Genes"

#########################################################
# GENE ID MAPPING: Convert Gene Identifiers
#########################################################

def convertGeneIds( setstrGenes, strMap, strFrom, strTo ):
	pFrom, pTo = [tempfile.NamedTemporaryFile( delete=False ) for i in range( 2 )]

	pFrom.write( "\n".join( setstrGenes ) + "\n" )
	pFrom.flush()

	strBatchmapperSH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "trunk/batchmapper.sh")
	strMapFlag = "-g" if strMap.endswith( ".bridge" ) else "-t"

	subprocess.check_call( ("sh", strBatchmapperSH, "-i", pFrom.name, "-is", strFrom,\
		"-os", strTo, "-o", pTo.name, strMapFlag, strMap, "-mm") )

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
			for iRow in range( iSkip, len( aastrData ) ):
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

def gene_sniffer( istm, strCols, pGeneNameHash = c_hashGeneNames, default_standard = c_strDefaultGeneIDFrom ):
	'''
	takes in input file, outputs gene identifier convention, e.g. HGNC
	'''
	def _sniff( name_list ):
		'''
		Input: takes in list of gene identifiers
		Output: name of gene identifier convention; e.g. "HGNC"
		'''
		# Define Standards Here 
		astrUniRef	= ["UniRef" + str(n) for n in [50, 90, 100]]
		strEnsembl = "EN"
		fUniProt	= 0.5 
		astrKeggCompound = ["K0", "K1"]
		
		len_name_list = len(name_list)
		strHead = name_list[0]
		#UniRef --> "UniGene"
		if any([strHead.startswith(x) for x in astrUniRef]):
			return "UniGene"
		elif strHead.startswith( strEnsembl ):
			return "Ensembl"
		elif any([strHead.startswith(x) for x in astrKeggCompound]):
			return "Kegg Compound"
		else: 
			#Uniprot 
			filter_list = [x for x in name_list if len(x) == 6 and (x.startswith("Q") or x.startswith("P"))]
			if float(len(filter_list))/float(len_name_list) >= fUniProt:
				return "Uniprot/TrEMBL"
			else:
				return default_standard 
			
	strCols = strCols[1:-1]
	aiCols = [int(s) for s in re.split( r'\s*,\s*', strCols )] if strCols else []
	setstrIn = set()
	csvr = csv.reader( istm, csv.excel_tab )
	strGeneID = None 
	for i in aiCols:
		if strGeneID: 
			break 
		astrData = [x[i] for x in csvr]
		strGeneID = _sniff( astrData )
	
	return pGeneNameHash[(strGeneID or default_standard)]

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
argp.add_argument( "-u",		dest = "iMaxLines",	metavar = "max_lines",
	type = int,					default = 100000,
	help = "Maximum lines in input file; this is done for memory reasons" )
argp.add_argument( "-s",		dest = "iSkip",		metavar = "skip_rows",
	type = int,					default = 0,
	help = "Number of header rows to skip at top of file" )
argp.add_argument( "-l",		dest = "ostmLog",	metavar = "log.txt",
	type = argparse.FileType( "w" ),
	help = "Optional log file containing output mapping status" )
argp.add_argument('-x', 		dest = "fSniffer",	action="store_true", default=False, 
	help = "Optional flag turning on/off gene identifier sniffer (automatically decide geneid_from)" )

def _main( ):
	args = argp.parse_args( )
	iLC = sfle.lc( args.istm.name )
 
	if (args.strFrom == args.strTo) or (iLC >= args.iMaxLines):
		#if the two gene identifier types are the same, or if the line count exceeds iMaxLines, 
		#return the input file 
		
		pAastrData = csv.reader(args.istm, csv.excel_tab)
		csvw = csv.writer( args.ostm, csv.excel_tab )
		for astrLine in pAastrData:
			csvw.writerow( astrLine )	
		if args.ostmLog:
			pMeta = metadata.open()
			pMeta.set("mapped", True)			
			pMeta.save_text( args.ostmLog )
	elif not(args.strMap) or not(os.stat(str(args.strMap))[6]):
		#if there is no map file specified 
		pAastrData = csv.reader(args.istm, csv.excel_tab)
		csvw = csv.writer( args.ostm, csv.excel_tab )
		for astrLine in pAastrData:
			csvw.writerow( astrLine )	
		if args.ostmLog:
			pMeta = metadata.open()
			pMeta.set("mapped", False)
			pMeta.save_text( args.ostmLog )
	else:
		#if gene sniffer flag is on, try to guess the best possible gene identifier 
		if args.fSniffer:
			args.strFrom = gene_sniffer( args.istm, args.strCols )
		
		bridgemapper( args.istm, args.ostm, args.strMap, args.strCols, args.strFrom, args.strTo, args.ostmLog, args.iSkip )

if __name__ == "__main__":
	_main( )
