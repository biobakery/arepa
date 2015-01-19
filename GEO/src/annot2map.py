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

annot2map.py: 
 
parse mapping files
begins with !platform_table_begin 
ends with !platform_table_end 
"""

import sfle 
import glob
import csv  
import sys 
import re 
import arepa 
import gzip 

c_fileMapping	= sfle.d( arepa.path_repo( ), sfle.c_strDirEtc, "mapping" )
c_hashHead 	= { k:v for (k, v) in [[y.strip() for y in x.split("%")] for x in sfle.readcomment( open( c_fileMapping))] } if sfle.readcomment(open(c_fileMapping))\
		else {	
		"^ID .*? platform"             	: "Affy",
		"Entrez Gene Symbol"       		: "HGNC",
		"Uniprot .*? Symbol"  			: "Uniprot/TrEMBL",
		"^(Entrez)? UniGene Symbol"		: "UniGene",	
		"Entrez Unigene Identifier"     : "UniGene_ID",
		"GenBank Accession"             : "GB_ACC",
		"Entrez Gene identifier"        : "Entrez Gene",
		"GenBank Identifier"            : "GenBank"
		}

iArg			= len(sys.argv)
strFileAnnotGZ	= sys.argv[1] if iArg > 1 else None 
strFileOut 		= sys.argv[2] if iArg > 2 else None 

strAnnotGZ 	= gzip.open( strFileAnnotGZ ).read() if strFileAnnotGZ else sys.stdin.read()
fileOut		= open( strFileOut, "w" ) if strFileOut else sys.stdout

if strAnnotGZ:
	aHead = re.findall(r"^#(.+?)\n", strAnnotGZ, re.MULTILINE )
	aKeys, aDesc = list(zip(*[[w.strip() for w in v.split("=")] for v in aHead])) 
	aOutKeys = [] 
	hOutDict = {}
	for item in list(c_hashHead.keys()):
		for desc in aDesc:
			reLine = re.findall(item, desc, re.M|re.I)
			if reLine:
				aOutKeys.extend( [aKeys[aDesc.index(desc)]] )
				hOutDict[ aKeys[aDesc.index(desc)]  ] = c_hashHead[item] 	
	strTable = re.findall(r"!platform_table_begin(.+)!platform_table_end", strAnnotGZ, re.S )[0].strip()
	dr = csv.DictReader( strTable.split("\n"), delimiter = "\t" ) 
	with fileOut as outputf:
		#write header
		outputf.write( "\t".join( [hOutDict[k] for k in aOutKeys] ) + "\n" )
		#write data
		for item in dr:
			try:
				outputf.write( "\t".join( [item[k] for k in aOutKeys] ) + "\n" )
			except Exception:
				continue 
		outputf.write(" ") 
else:
	with fileOut as outputf: 
		outputf.write(" ") 
