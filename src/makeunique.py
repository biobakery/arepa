#!/usr/bin/env python

import argparse
import sets
import itertools 
import sys 
import csv 
import os
import metadata 

def makeunique( istm, ostm, strSplit, iCols, iSkip, ostmLog ):
	'''
	Splits up compressed elements (e.g. a///b c///d) into their cartesian products (e.g. a c, a d, b c, bd);
	then, gets rid of duplicate elements in the set of unordered tuples (equivalence under permutation).
	User can specify how many lines to skip beforehand, and how many columns are to be considered 
	'''
	aastrMatIn = [x for x in csv.reader( istm,csv.excel_tab )]
	aastrHeaders, aastrDataIn = aastrMatIn[:iSkip], aastrMatIn[iSkip:]
	
	#open a blank metadata object 
	pMeta = metadata.open( )
	if strSplit:
		aastrSplit = [] 
		for astrRow in aastrDataIn:
			astrNames, astrVals = astrRow[:iCols], astrRow[iCols:]
			if any(astrVals) and reduce(lambda y,z: y or z, map(lambda x: x.find(strSplit)!=-1,astrNames)):
				astrSplit = map(lambda x: x.split(strSplit),astrNames)
				aastrSplit += map(lambda v: list(v) + astrVals,[x for x in itertools.product(*astrSplit)]) 	
			else:
				aastrSplit.append(astrRow)
	else:
		aastrSplit = aastrDataIn
		
	pNames = set([])
	aastrUnique = [] 
	for astrRow in aastrSplit:
		astrNames, astrVals = astrRow[:iCols], astrRow[iCols:]
		lenNames = len(astrNames)
		if (len(frozenset(astrNames)) == lenNames and not(frozenset(astrNames) in pNames)):
			pNames |= set([frozenset(astrNames)])
			aastrUnique.append(astrRow)
	
	pMeta.set( "mapped", any( aastrUnique ) )
	
	#write output 
	csvw = csv.writer( ostm, csv.excel_tab )
	for row in aastrHeaders + aastrUnique:
        	csvw.writerow( row )		
	
	#save metadata 
	if ostmLog:
		pMeta.save_text( ostmLog )	 	

argp = argparse.ArgumentParser( prog = "makeunique.py",
        description = 	"""Gets rid of duplicate entries from a tab-delimited file of unordered tuples.""" )

argp.add_argument( "istm",              metavar = "input.dat",
        type = argparse.FileType( "r" ),        nargs = "?",    default = sys.stdin,
        help = "Input tab-delimited text file with one or more columns" )
argp.add_argument( "ostm",              metavar = "output.dat",
        type = argparse.FileType( "w" ),        nargs = "?",    default = sys.stdout,
        help = "Input tab-delimited text file with mapped columns" )
argp.add_argument( "-m",                dest = "strSplit",        metavar = "str_split",
        type = str,                    	default = "///",	required = False,
        help = "Ambiguous field element classifier; a or b; e.g. in the case of a///b the value will be ///" )
argp.add_argument( "-c",                dest = "iCols",       metavar = "columns",
        type = int,                     default = "2",
        help = "Number of columns to map" )
argp.add_argument( "-s",                dest = "iSkip",         metavar = "skip_rows",
        type = int,                     default = 0,
        help = "Number of header rows to skip at top of file" )
argp.add_argument( "-l",                dest = "ostmLog",       metavar = "log.txt",
        type = argparse.FileType( "w" ),
        help = "Optional log file containing output mapping status" )

def _main( ):
	args = argp.parse_args()
	makeunique( args.istm, args.ostm, args.strSplit, args.iCols, args.iSkip, args.ostmLog )

if __name__ == "__main__":
	_main()	
