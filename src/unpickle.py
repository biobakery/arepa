#!/usr/bin/env python
'''pickle and unpickle files'''

import os 
import csv
import pickle
import sys
import argparse 


def unpickle( istm, ostm, strSplit, iCols, iSkip, istmLog, strManKey ):
	hashData = pickle.load( istm )
	csvw = csv.writer( ostm, csv.excel_tab )
	if strManKey: csvw.writerow( [hashData[strManKey]] )
	else:
		for strKey, pValue in hashData.items( ):
			csvw.writerow( (strKey, "%s" % pValue) )
		

def pickle( istm, ostm, strSplit, iCols, iSkip, istmLog, strManKey ):
	pMeta = {}
	csvr1 = csv.reader( istm, csv.excel_tab )
	for line in csvr1:
		if line: key,value = line 
		pMeta[key] = value 
	if istmLog:
		csvr2 = csv.reader( istmLog, csv.excel_tab )
		for line in csvr2:
			if line: key,value = line 
			pMeta[key] = value 
	return pickle.dump( pMeta, ostm )

def 


argp = argparse.ArgumentParser( prog = "unpickle.py",
        description =   """pickle and unpickle files.""" )
argp.add_argument( "istm",              metavar = "input",
        type = argparse.FileType( "r" ),        nargs = "?",    default = sys.stdin,
        help = "input pickle or text file" )
argp.add_argument( "ostm",              metavar = "output",
        type = argparse.FileType( "w" ),        nargs = "?",    default = sys.stdout,
        help = "output pickle or text file" )
argp.add_argument( "-m",                dest = "strSplit",        metavar = "str_split",
        type = str,                     required = False,
        help = "Split between key and value" )
argp.add_argument( "-c",                dest = "iCols",       metavar = "columns",
        type = int,                     default = "2",
        help = "Number of columns to map" )
argp.add_argument( "-s",                dest = "iSkip",         metavar = "skip_rows",
        type = int,                     default = 0,
        help = "Number of header rows to skip at top of file" )
argp.add_argument( "-l",                dest = "istmLog",       metavar = "log.txt",
        type = argparse.FileType( "r" ),
        help = "Optional log file containing status metavariables" )
argp.add_argument( "-r",		dest = "fRev",		action = "store_true",
	help = "Reverse flag" )
argp.add_argument( "-k",		dest = "strManKey",	metavar = "str_man_key",
	help = "Flag to specify output for specific key in the pickle" )
argp.add_argument( "-x",		dest = "fRMeta", 	action = "store_true",
 	help = "Give output in R package metadata format")

def _main( ):
        args = argp.parse_args()
		if not(args.fRev):
        	unpickle( args.istm, args.ostm, args.strSplit, args.iCols, args.iSkip, args.istmLog, args.strManKey )
		else:
			pickle( args.istm, args.ostm, args.strSplit, args.iCols, args.iSkip, args.istmLog, args.strManKey )

if __name__ == "__main__":
        _main()
