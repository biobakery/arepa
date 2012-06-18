#!/usr/bin/env python 

import sfle 
import glob
import csv  
import sys 
import re 
import arepa 

''' parse mapping files
begins with !platform_table_begin 
ends with !platform_table_end '''

c_fileMapping	= sfle.d( arepa.path_repo( ), sfle.c_strDirEtc, "mapping" )
c_hashHead 	= { k:v for (k,v) in map( lambda x: map(lambda y: y.strip(), x.split(":")),\
			sfle.readcomment( open( c_fileMapping)) ) } 

strAnnotGZ = sys.stdin.read()

if strAnnotGZ:
	aHead = re.findall(r"^#(.+?)\n", strAnnotGZ, re.MULTILINE )
	aKeys, aDesc = zip(*map( lambda v: map(lambda w: w.strip(), v.split("=")), aHead )) 
	aOutKeys = [] 
	hOutDict = {}
	for item in c_hashHead.keys():
		for desc in aDesc:
			reLine = re.findall(item, desc, re.M|re.I)
			if reLine:
				aOutKeys.extend( [aKeys[aDesc.index(desc)]] )
				hOutDict[ aKeys[aDesc.index(desc)]  ] = c_hashHead[item] 	
	sys.stderr.write(str(aOutKeys) + "\n")
	sys.stderr.write(str(hOutDict) + "\n")
	strTable = re.findall(r"!platform_table_begin(.+)!platform_table_end", \
		strAnnotGZ, re.S )[0].strip()
	dr = csv.DictReader( strTable.split("\n"), delimiter = "\t" ) 
	with sys.stdout as outputf:
		"write header"
		outputf.write( "\t".join( [hOutDict[k] for k in aOutKeys] ) + "\n" )
		"write data"
		for item in dr:
			try:
				outputf.write( "\t".join( [item[k] for k in aOutKeys] ) + "\n" )
			except KeyError:
				continue  
else:
	sys.stdout.write("") 
