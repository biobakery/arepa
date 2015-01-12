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

unpickle.py: 

Pickle and unpickle files. 
"""

import os 
import csv
import pickle
import sys
import argparse 

def _unpickle( istm, ostm, strSplit, iCols, iSkip, istmLog, strManKey, fRMeta ):
	hashData = pickle.load( istm )
	csvw = csv.writer( ostm, csv.excel_tab )
	if strManKey: 
		csvw.writerow( [hashData[strManKey]] )			
	else:
		for strKey, pValue in list(hashData.items( )):
			csvw.writerow( (strKey, "%s" % pValue) )

def _pickle( istm, ostm, strSplit, iCols, iSkip, istmLog, strManKey ):
	pMeta = {}
	csvr1 = csv.reader( istm, csv.excel_tab )
	for line in csvr1:
		if line: key, value = line 
		pMeta[key] = value 
	if istmLog:
		csvr2 = csv.reader( istmLog, csv.excel_tab )
		for line in csvr2:
			if line: key, value = line 
			pMeta[key] = value 
	return pickle.dump( pMeta, ostm )

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
		_unpickle( args.istm, args.ostm, args.strSplit, args.iCols, args.iSkip, args.istmLog, args.strManKey, args.fRMeta )
	else:
		_pickle( args.istm, args.ostm, args.strSplit, args.iCols, args.iSkip, args.istmLog, args.strManKey )

if __name__ == "__main__":
        _main()
